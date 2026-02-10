from django.urls import path
from blogs.views import (
    Home,
    CreateBlog,
    UpdateBlog,
    DeleteBlog,
    BlogList,
    BlogDetail,
    favourites,
    FeedView,
    unfavourite_action
)


urlpatterns = [
    path('home/', Home, name="home"),
    path('create/', CreateBlog.as_view(), name="create"),
    path('update/<slug:slug>/', UpdateBlog.as_view(), name="update"),
    path('delete/<slug:slug>/', DeleteBlog.as_view(), name="delete"),
    path('all/', BlogList.as_view(), name="blog_list"),
    path('feed/', FeedView.as_view(), name="feed_list"),
    path('detail/<slug:slug>', BlogDetail.as_view(), name="blog_detail"),
    path('favourites/', favourites.as_view(), name="favourites"),
    path('unfavourite/<str:title>/', unfavourite_action, name="unfavourite_action"),
]