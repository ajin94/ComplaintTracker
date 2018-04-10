from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_tracker, name="main_tracker"),
    path('login/', views.make_login, name="make_login"),
    path('logout/', views.logout_user, name="logout_user")
]
