from django.contrib.auth.models import User
from userauth.forms import SignupForm
from blogs.models import Interest
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy



class SignUpView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "userauth/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        Interest.objects.create(user=user, category=form.cleaned_data["category"])

        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = "userauth/login.html"
    redirect_authenticated_user = True