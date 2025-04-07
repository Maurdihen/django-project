from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import uuid
import random
import string

from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserPasswordResetForm

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.verification_token = str(uuid.uuid4())
        user.save()

        verification_url = self.request.build_absolute_uri(
            f'/users/verify/{user.verification_token}/'
        )
        
        send_mail(
            'Подтверждение регистрации',
            f'Для подтверждения регистрации перейдите по ссылке: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return super().form_valid(form)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.email_verified = True
        user.verification_token = None
        user.save()
        return render(request, 'users/verification_success.html')
    except User.DoesNotExist:
        return render(request, 'users/verification_failed.html')

def logout_view(request):
    if request.method == 'GET':
        return render(request, 'users/logout.html')
    elif request.method == 'POST':
        logout(request)
        return redirect('index')

class PasswordResetView(FormView):
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            # Генерация случайного пароля
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            user.password = make_password(new_password)
            user.save()

            # Отправка нового пароля на email
            send_mail(
                'Восстановление пароля',
                f'Ваш новый пароль: {new_password}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
        except User.DoesNotExist:
            pass  # Не сообщаем пользователю, что email не существует

        return super().form_valid(form)
