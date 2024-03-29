from django.urls import include, path

from api import views

urlpatterns = [
    path('', views.ApiHome.as_view(), name='api_home'),
    path('posts/', views.ListCreatePosts.as_view(), name='api_posts'),
    path('posts/<int:pk>/', views.SinglePost.as_view(), name='api_singlepost'),
    path('tags/', views.ListCreateTags.as_view(), name='api_tags'),
    path('tags/<int:pk>/', views.SingleTag.as_view(), name='api_singletag'),
    path('api-auth/', include('rest_framework.urls')),
]
