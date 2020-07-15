from django.urls import path, re_path
from . import views

urlpatterns = [
    path("register/", views.register, name="blog-register"),    
    path('login/', views.login, name='blog-login'),
    path('logout/', views.logout, name='blog-logout'),
    path('', views.home, name='blog-home'),
]

