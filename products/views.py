import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from userauth.models import StripeCustomer
from django.db.models import F
from products.models import Product, Cart, Order, OrderItem, Address, StripeOrderObject
from follow.models import Follow
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from products.forms import ProductForm, QuantityForm, AddressForm
from django.views.generic import CreateView, ListView, UpdateView


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/add_product.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.product_seller = self.request.user
        user.save()

        return super().form_valid(form)

class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/update.html"


class MyProductsView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Product
    template_name = "products/my_products.html"
    context_object_name = "my_products"

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(product_seller=user)


@login_required
def add_to_cart_action(request, pk):
    form = QuantityForm(request.POST)
    if request.method == "POST":
        cart_data = Cart.objects.filter(product__pk=pk, customer=request.user).first()
        if not cart_data:
            user = request.user
            item = Product.objects.filter(pk=pk).first()
            if int(form.data["quantity"]) <= item.stock and int(form.data["quantity"]) != 0:
                Cart.objects.create(seller=item.product_seller, customer=user, product=item, quantity=form.data["quantity"])
                product = Product.objects.get(pk=item.pk)
                product.stock = F("stock") - int(form.data["quantity"])
                product.save()
                messages.success(request, message="Product added to Cart")
                return redirect(reverse("TimelineView"))
            elif int(form.data["quantity"]) == 0:
                messages.error(request, message="Please increase the quantity to add products")
                return redirect(reverse("TimelineView"))
            else:
                messages.error(request, message="Quantity out of range")
                return redirect(reverse("TimelineView"))
    messages.info(request, message="Product already in cart")
    return redirect(reverse("TimelineView"))


class TimelineView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Product
    template_name = "products/timeline.html"
    context_object_name = "following_user_products"

    def get_queryset(self, *args, **kwargs):
        followings = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        return Product.objects.filter(product_seller__pk__in=followings)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = QuantityForm()
        context["form"] = form

        return context


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = "products/cart.html"
    context_object_name = "cartitems"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Cart.objects.filter(customer=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartitems = Cart.objects.filter(customer=self.request.user)
        bill = 0
        for item in cartitems:
            bill += item.total_amount

        context["bill"] = bill
        return context


@login_required
def remove_from_cart_action(request, pk):
    user = request.user
    cart_item = Cart.objects.filter(customer=user, product_id=pk).first()
    cart_item.delete()
    cart_product = Product.objects.get(pk=pk)
    cart_product.stock = F("stock") + int(cart_item.quantity)
    cart_product.save()
    messages.success(request, message="Item Removed from cart")
    return redirect(reverse("CartView"))


class OrderItemsView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "products/order_items.html"
    context_object_name = "myorders"

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(order__owner=user)


class MyOrders(LoginRequiredMixin, ListView):
    model = Order
    template_name = "products/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user).order_by("-created_at")


class CustomerProductsView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "products/customer_products.html"
    context_object_name = "orders"

    def get_queryset(self):
        user = self.request.user
        ordered_items = OrderItem.objects.all().only("item")
        queryset = OrderItem.objects.filter(item__product_seller=user).exclude(order__owner=user)
        return queryset


@login_required
def confirm_order(request):
    cart_items = Cart.objects.filter(customer=request.user)
    order, created = Order.objects.get_or_create(owner=request.user, status="PENDING")

    total_bill = 0

    for cart_item in cart_items:
        order_item, item_created = OrderItem.objects.get_or_create(order=order, item=cart_item.product, defaults={"quantity": cart_item.quantity, "total_price": cart_item.total_amount})

        if not item_created:
            order_item.quantity += cart_item.quantity
            order_item.total_price = order_item.quantity * order_item.item.discounted_price
            order_item.save()

    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        total_bill += item.total_price
    order.bill = total_bill
    order.save()

    cart_items.delete()

    messages.success(request, "Order confirmed successfully.")
    return redirect("MyOrders")


class AddAddress(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "products/addresses.html"
    success_url = reverse_lazy("payment_page")

    def form_valid(self, form):
        delivery_address = form.save(commit=False)
        delivery_address.user = self.request.user
        delivery_address.save()
        Order.objects.filter(owner=self.request.user, status="PENDING").update(address=delivery_address.pk)
        messages.success(self.request, message="Address Added")
        return super().form_valid(form)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "products/update_address.html"
    success_url =  reverse_lazy("MyOrders")

    def form_valid(self, form):
        updated_address = form.save(commit=False)
        updated_address.user = self.request.user
        updated_address.save()
        messages.success(self.request, message="Address Changes")
        return super().form_valid(form)

@login_required
def save_choosen_address(request, order_id):
    Order.objects.filter(owner=request.user, status="PENDING").update(address=order_id)
    messages.success(request, message="Address Added")
    return redirect(reverse("payment_page"))


class ChooseAddressView(LoginRequiredMixin, ListView):
    model = Address
    template_name = "products/choose_address.html"
    context_object_name = "addresses"

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset


stripe.api_key=settings.STRIPE_SECRET_KEY

@login_required
def payment_page(request):
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    try:
        order = Order.objects.get(owner=request.user, status="PENDING")
    except Exception as e:
        print(e)
        messages.error(request, message="You haven't any unpaid orders")
        return redirect(reverse("MyOrders"))
    context = {
        "stripe_publishable_key": stripe_publishable_key,
        "amount": order.bill,
        "currency": 'USD',
        "email": request.user.email,
        "order_items": order.OrderItems.all(),
        "order":     order
    }
    return render(request, "products/payment.html", context)


@csrf_exempt
def create_payment_intent(request, order_id):
    existing_paid_order = Order.objects.get(pk=order_id)
    if not existing_paid_order.is_paid:
        if request.method == "POST":
            data = json.loads(request.body)
            customer_name = request.user.username
            customer_amount = data.get("amount")
            customer_currency = data.get("currency")
            customer_email = data.get("email")

            try:
                stripe_customer = StripeCustomer.objects.get(user=request.user)

            except StripeCustomer.DoesNotExist:
                delivery_order = Order.objects.get(id=order_id, owner=request.user.id)
                customer = stripe.Customer.create(
                    name=customer_name,
                    email=customer_email,
                    address={"country":delivery_order.address.country}
                    )
                stripe_customer = StripeCustomer.objects.create(user=request.user, stripe_customer_id=customer.id)

            except Exception as e:
                messages.error(request, message=e)

            intent = stripe.PaymentIntent.create(
                amount=int(customer_amount) * 100,
                currency=customer_currency,
                customer=stripe_customer.stripe_customer_id,
                payment_method_types=["card"]
            )
            paid_order = Order.objects.get(id=order_id, owner=request.user.id)
            StripeOrderObject.objects.create(order=paid_order, payment_intent_id=intent.id)
            paid_order.status = "CONFIRMED"
            paid_order.is_paid = True
            paid_order.save()
            return JsonResponse({"client_secret": intent.client_secret})
    else:
        messages.error(request, message="Order already paid")
        return JsonResponse({"message": "Already Paid!"})


@csrf_exempt
def refund_payment(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id, owner=request.user, status="CONFIRMED")
            stripe_order_object = StripeOrderObject.objects.get(order__id=order_id, order__owner=request.user, order__status="CONFIRMED")
        except Order.DoesNotExist:
            messages.error(request, message="Order not Found")
            return redirect(reverse("MyOrders"))
        except StripeOrderObject.DoesNotExist:
            messages.error(request, message="Please make sure that your order is paid")
            return redirect(reverse("MyOrders"))
        except Exception as e:
            messages.error(request, message="Refund failed due to some errors")
            return redirect(reverse("MyOrders"))
        
        if order.is_paid == False:
            messages.error(request, message="Order is not paid")
            return redirect(reverse("MyOrders"))
        
        if stripe_order_object.is_refunded:
            messages.error(request, message="Order already refunded")
            return redirect(reverse("MyOrders"))
        else:
            refund = stripe.Refund.create(
                payment_intent=stripe_order_object.payment_intent_id
            )
            stripe_order_object.is_refunded = True
            stripe_order_object.save()
            messages.success(request, message="Order Refunded Successfully")
            return redirect(reverse("MyOrders"))


def success(request):
    messages.success(request, message="Your payment is successfully submitted")
    return redirect(reverse("MyOrders"))


def failed(request):
    messages.error(request, message="Payment Failed due to some issues")
    return redirect(reverse("MyOrders"))