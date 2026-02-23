from django.shortcuts import render, redirect
from follow.models import Follow
from django.contrib import messages
from userauth.models import Interest
from blogs.models import Blog, Category
from products.models import Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.forms import BlogForm
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)

@login_required
def Home(request):
    user = request.user
    blog_count = Blog.objects.filter(user=user).count()
    follower_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    cart_items_count = Cart.objects.filter(customer=user).count()
    context = {"blog_count": blog_count, "follower_count": follower_count, "following_count": following_count, "cart_items_count": cart_items_count}
    return render(request, "blogs/home.html", context)


class CreateBlog(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = "blogs/blog_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, message="blog created successfully")
        return super().form_valid(form)


class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/blog_update.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, message="blog updated successfully")
        return super().form_valid(form)


class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "blogs/delete_blog.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        messages.success(self.request, message="Blog Deleted")
        return super().form_valid(form)
    


class BlogList(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Blog
    context_object_name = "blogs"

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user)


class BlogDetail(LoginRequiredMixin, DetailView):
    model = Blog
    context_object_name = "blog_details"


class favourites(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Blog
    template_name = "blogs/favourites.html"
    context_object_name = "favourites"

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user, favourite=True)


class FeedView(ListView):
    paginate_by = 5
    model = Blog
    template_name = "blogs/feed.html"
    context_object_name = "feed_blogs"

    def get_queryset(self):
            user = self.request.user
            user_followings = user.followers.only("following")

            user_interests = Interest.objects.filter(user=user).values_list("category", flat=True)
            categories = Category.objects.filter(pk__in=user_interests).only("name")
            following_list = []
            for following in user_followings:
                following_list.append(following)

            return Blog.objects.filter(
                Q(category__in=categories) | Q(user__followings__in=following_list)
            ).order_by("-published_at").distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        followings = Follow.objects.filter(follower=user).values_list('following', flat=True)

        context['following_list'] = followings
        return context


@login_required
def unfavourite_action(request, title):
    user = request.user
    favourite = Blog.objects.get(user=user, title=title)
    favourite.favourite = False
    favourite.save()
    messages.success(request, message="removed from favourites")
    return redirect(reverse('favourites'))