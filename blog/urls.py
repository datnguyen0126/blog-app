from django.urls import path, re_path
from . import views

urlpatterns = [
    path("register/", views.register, name="blog-register"),    
    path('login/', views.login, name='blog-login'),
    path('logout/', views.logout, name='blog-logout'),
    path('blog/create/', views.blog_create, name='blog-create-post'),
    path('blog/edit/<int:id>/', views.blog_create, name='blog-update-post'),
    path('blog/delete/<int:id>/', views.blog_delete, name='blog-delete-post'),
    path('about/', views.about, name='blog-about'),
    path('', views.home, name='blog-home'),
]