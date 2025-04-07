from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
] 