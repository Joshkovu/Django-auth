from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("create_comment/", views.create_comment, name="create_comment"),
 
]