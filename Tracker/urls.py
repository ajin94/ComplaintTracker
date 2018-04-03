from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_tracker, name = "main_tracker"),
]
