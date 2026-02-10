from django.urls import path
from userauth.views import SignUpView, UserLoginView



urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', UserLoginView.as_view(), name="login"),
]