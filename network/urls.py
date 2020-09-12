
from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from .views import LikeView, LikeHandlerView, UnlikeHandlerView, TotalLikeView

from . import views

router = routers.DefaultRouter()
router.register('likes', views.LikeView, basename="likes")
router.register('likes/<int:id>', LikeView, basename="get_likes"),

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile_view, name="profile_view"),
    path("profile/<int:id>", views.click_profile, name="click_profile"),
    path('follow', views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path('following', views.following, name="following"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>', views.delete_post, name="delete_post"),
    path('comment', views.comment, name="comment"),
    path('like', LikeHandlerView.as_view()),
    path('unlike', UnlikeHandlerView.as_view()),
    path('total', TotalLikeView.as_view()),

    # API Routes
    path('', include(router.urls)),
]
