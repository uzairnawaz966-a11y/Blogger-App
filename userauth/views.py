from django.contrib.auth.models import User
from userauth.forms import SignupForm
from django.contrib import messages
from userauth.models import Interest
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from userauth.forms import InterestForm


class SignUpView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, message="User Created Successfully, Login to visit site")
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class InterestView(CreateView):
    model = Interest
    form_class = InterestForm
    template_name = "accounts/user_interest.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        form.instance.user = self.request.user
        user.save()
        messages.success(self.request, message="We will keep in mind your interests")
        return super().form_valid(form)