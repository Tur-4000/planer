from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView
# from django.contrib.auth.decorators import user_passes_test
from datetime import date


class RegisterView(UserPassesTestMixin, CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['today'] = date.today()
        return context


class UserLoginView(LoginView):
    template_name = 'user/login.html'


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    today = date.today()
    template_name = 'user/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('todo_list')

    def get_context_data(self, **kwargs):
        context = super(UserPasswordChangeView, self).get_context_data(**kwargs)
        context['today'] = date.today()
        return context

