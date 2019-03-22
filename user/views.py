from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterView(LoginRequiredMixin, CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo_list')


class UserLoginView(LoginView):
    template_name = 'user/login.html'


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'user/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('todo_list')

