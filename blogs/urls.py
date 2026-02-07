from django.urls import path
from django.contrib.auth.views import LogoutView
from blogs.views import (
    Home,
    CreateBlog,
    UpdateBlog,
    DeleteBlog,
    BlogList,
    BlogDetail,
    favourites,
    SignUpView,
    UserLoginView,
    RecommendationView,
    FollowerView,
    FollowingView,
)


urlpatterns = [
    path('home/', Home, name="home"),
    path('create/', CreateBlog.as_view(), name="create"),
    path('update/<slug:slug>/', UpdateBlog.as_view(), name="update"),
    path('delete/<slug:slug>/', DeleteBlog.as_view(), name="delete"),
    path('all/', BlogList.as_view(), name="blog_list"),
    path('detail/<slug:slug>', BlogDetail.as_view(), name="blog_detail"),
    path('favourites/', favourites.as_view(), name="favourites"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('recommendation/', RecommendationView.as_view(), name="recomended"),
    path('follower/', FollowerView.as_view(), name="follower"),
    path('following/', FollowingView.as_view(), name="following"),
]