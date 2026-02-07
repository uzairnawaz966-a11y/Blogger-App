from django.shortcuts import render
from blogs.models import Blog, Interest, Follow
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.forms import BlogForm, SignupForm
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)

@login_required
def Home(request):
    return render(request, "blogs/home.html")


class CreateBlog(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = "blogs/blog_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/blog_update.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "blogs/delete_blog.html"
    success_url = reverse_lazy("blog_list")


class BlogList(LoginRequiredMixin, ListView):
    model = Blog
    context_object_name = "blogs"

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user)


class BlogDetail(LoginRequiredMixin, DetailView):
    model = Blog
    context_object_name = "blog_details"


class favourites(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "blogs/favourites.html"
    context_object_name = "favourites"

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user, favourite=True)
    

class SignUpView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "blogs/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        Interest.objects.create(user=user, category=form.cleaned_data["category"])

        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = "blogs/login.html"
    redirect_authenticated_user = True


class RecommendationView(LoginRequiredMixin, ListView):
    template_name = "blogs/recommended.html"
    context_object_name = "recommendations"

    def get_queryset(self):
        user = self.request.user
        fav = user.interest.category
        return Blog.objects.filter(category=fav)


class FollowerView(ListView):
    model = Follow
    template_name = "blogs/followers.html"
    context_object_name = "followers"

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(following=user).only("follower")


class FollowingView(ListView):
    model = Follow
    template_name = "blogs/followings.html"
    context_object_name = "followings"

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(follower=user).only("following")