from django.urls import path
from django.contrib.auth import views as auth_views

from user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', views.UserPasswordChangeView.as_view(), name='change_password'),
]
