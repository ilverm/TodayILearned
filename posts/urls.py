from django.urls import path, include

from posts import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('create/', views.create_post, name='create'),
]