from django.shortcuts import render, redirect
from follow.models import Follow
from blogs.models import Blog
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
    context = {"blog_count": blog_count, "follower_count": follower_count, "following_count": following_count}
    return render(request, "blogs/home.html", context)


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
        user_interests = user.user_interests.only("category")
        user_followings = user.followers.only("following")

        following_list = []
        for following in user_followings:
            following_list.append(following)

        blog_list = []
        for interest in user_interests:
            blog_list.append(interest.category)

        return Blog.objects.filter(
            Q(category__in=blog_list) | Q(user__followings__in=following_list)
        ).order_by("-published_at").distinct()


@login_required
def unfavourite_action(request, title):
    user = request.user
    favourite = Blog.objects.get(user=user, title=title)
    updated_favourite = favourite.favourite = False
    favourite.save()
    print(updated_favourite)
    return redirect(reverse('favourites'))