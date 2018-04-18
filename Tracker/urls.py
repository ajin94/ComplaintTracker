from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_tracker, name="main_tracker"),
    path('outbound/', views.out_bound_complaints, name="out_bound_complaints"),
    path('login/', views.make_login, name="make_login"),
    path('logout/', views.logout_user, name="logout_user"),
    path('ajax_mark_as_resolved/', views.ajax_mark_as_resolved, name="ajax_mark_as_resolved")
]
