from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
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


@login_required
def follow_button(request, username):
    user = request.user.username
    feed_user = User.objects.get(username=username)
    following_user = Follow.objects.filter(follower=request.user.pk, following=feed_user.pk)

    user = User.objects.get(username=username)

    if username != request.user.username:
        if not following_user:
            Follow.objects.create(follower=request.user, following=user)
            messages.success(request, message=f"{user} Followed")
            return redirect(reverse('feed_list'))
        else:
            follow_object = Follow.objects.get(follower=request.user.pk, following=user.pk)
            follow_object.delete()
            messages.success(request, message=f"{user} Unfollowed")
            return redirect(reverse('feed_list'))

    return redirect(reverse('feed_list'))