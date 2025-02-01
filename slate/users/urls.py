from django.urls import path
from .views import  LoginView,StudentAchievementView, RegisterView


urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("student/achievements/", StudentAchievementView.as_view(), name="student-achievements"),
    path("register/", RegisterView.as_view(), name="register"),
]

