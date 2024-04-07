from django.shortcuts import redirect
from apps.account.models import UserProfile
from .forms import LoginForm, RegisterForm
from django.views.generic import FormView
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            password = form.cleaned_data.pop("password")
            confirm_password = form.cleaned_data.pop('confirm_password')
            if password != confirm_password:
                return redirect("user_register")

            address = form.cleaned_data.pop('address')
            bio = form.cleaned_data.pop('bio')
            phone = form.cleaned_data.pop('phone')

            user = User.objects.create(is_active=True, **form.cleaned_data)
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user, address=address, bio=bio, phone=phone)
            return redirect("home")
        else:
            return self.form_invalid(form)
