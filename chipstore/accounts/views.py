from django import forms
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.views import (
    LoginView,
    SignupView,
    PasswordChangeView,
    PasswordSetView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    LogoutView,
    EmailVerificationSentView,
    AccountInactiveView,
    EmailView,
    ConfirmEmailView,
)
from allauth.account.forms import ChangePasswordForm, SetPasswordForm
from .forms import _SignupForm

User = get_user_model()


class _SignupView(SignupView):
    form_class = _SignupForm


class _LoginView(LoginView):
    pass


class _LogoutView(LogoutView):
    pass


class _PasswordChangeView(PasswordChangeView):
    pass


class _PasswordSetView(PasswordSetView):
    pass


class _PasswordResetView(PasswordResetView):
    pass


class _PasswordResetDoneView(PasswordResetDoneView):
    pass


class _PasswordResetFromKeyView(PasswordResetFromKeyView):
    pass


class _PasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    pass


class _AccountInactiveView(AccountInactiveView):
    pass


class _EmailView(EmailView):
    pass


class _EmailVerificationSentView(EmailVerificationSentView):
    pass


class _ConfirmEmailView(ConfirmEmailView):
    pass
