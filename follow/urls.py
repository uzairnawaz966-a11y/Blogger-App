from django.urls import path
from follow.views import (
    FollowerView,
    FollowingView,
    FollowerBlogsView,
    FollowingBlogsView,
    follow_button
)


urlpatterns = [
    path('follower/', FollowerView.as_view(), name="follower"),
    path('following/', FollowingView.as_view(), name="following"),
    path('<str:username>/data/', FollowerBlogsView.as_view(), name="follower_blogs"),
    path('<str:username>/data/', FollowingBlogsView.as_view(), name="following_blogs"),
    path('follow/<str:username>/', follow_button, name="follow_button")
]