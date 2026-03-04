from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("create_weekly_log/", views.create_weekly_log, name="create_weekly_log"),
    path("approve_weekly_log/<int:log_id>/", views.approve_weekly_log, name="approve_weekly_log"),
    path("award_mark/<int:log_id>/", views.award_mark, name="award_mark"),
    path("create_user_account/", views.create_user_account, name="create_user_account"),
 
]