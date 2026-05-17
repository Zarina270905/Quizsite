from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginUserForm
from .forms import RegisterUserForm
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import ProfileUserForm
from .forms import UserPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

User = get_user_model()

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Изменение пароля'}

