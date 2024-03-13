from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm

from posts import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('create/', views.create_post, name='create'),
    path('search/', views.search, name='search'),
    path('<int:post_pk>/', views.single_post_view, name='single_post'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), 
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        form_class=PasswordChangeForm,
        success_url='/'),
        name='password_change'
    ),
    path('accounts/create/', views.create_account, name='create_account'),

    path('api/', include('api.urls')),
    
]