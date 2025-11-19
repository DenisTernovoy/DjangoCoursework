import secrets

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from config import settings
from users.forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserUpdateForm,
)
from users.models import CustomUser


# Create your views here.
class RegisterView(CreateView):
    template_name = "users/customuser_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mailing:main")

    def form_valid(self, form):
        user = form.save(commit=False)
        token = secrets.token_hex(16)
        user.token = token
        user.is_active = False
        user.save()

        host = self.request.get_host()

        url = f"http://{host}/users/confirm-email/{token}"

        self.send_welcome_email(user.email, url)

        return super().form_valid(form)

    @staticmethod
    def send_welcome_email(user_email, confirm_url):
        subject = "Регистрация в сервисе рассылок"
        message = f"Подтвердите регистрацию в сервисе. Для этого перейдите по ссылке {confirm_url}"
        from_email = settings.EMAIL_HOST_USER

        recipient_list = [
            user_email,
        ]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )


def confirm_email(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()

    return redirect("users:login")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("mailing:main")


class CustomUserDetailView(DetailView):
    model = CustomUser


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["change_flag"] = True

        return context

    success_url = reverse_lazy("mailing:main")


class CustomPasswordResetView(PasswordResetView):
    model = CustomUser
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    model = CustomUser
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    model = CustomUser
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    model = CustomUser
    template_name = "users/password_reset_complete.html"


class UserListView(ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"


def block_user(request, pk):
    user = CustomUser.objects.get(pk=pk)
    user.is_active = False
    user.save()

    return redirect("users:users")


def unblock_user(request, pk):
    user = CustomUser.objects.get(pk=pk)
    user.is_active = True
    user.save()

    return redirect("users:users")
