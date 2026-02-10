from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.models import Blog
from follow.models import Follow


class FollowerView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "follow/followers.html"
    context_object_name = "followers"

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(following=user).only("follower")


class FollowingView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "follow/followings.html"
    context_object_name = "followings"

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(follower=user).only("following")


class FollowerBlogsView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "follow/user_info.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.kwargs["username"]
        context["user"] = user

        blogs = Blog.objects.filter(user__username=user)
        context["follower_blogs"] = blogs
        return context


class FollowingBlogsView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "follow/user_info1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.kwargs["username"]
        print(user)
        context["user"] = user
            
        blogs = Blog.objects.filter(user=user)
        context["following_blogs"] = blogs

        return context