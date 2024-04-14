from django.shortcuts import redirect
from apps.account.models import UserProfile
from .forms import LoginForm, RegisterForm, UserProfileForm
from django.views.generic import FormView, DetailView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

User = get_user_model()


class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                messages.success(request, "Logged in successfully !")
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials !")
                return redirect("user_login")
        else:
            messages.error(request, "Invalid credentials !")
            return redirect("user_login")


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


def user_logout(request):
    logout(request)
    return redirect("home")


class UserProfileView(DetailView):
    queryset = User.objects.all()
    template_name = "account/user_profile.html"
    context_object_name = "user"


class UserProfileUpdateView(DetailView, FormView):
    form_class = UserProfileForm
    queryset = User.objects.all()
    template_name = "account/profile_update.html"
    context_object_name = "user"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user = self.request.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            phone_number = form.cleaned_data.get("phone_number")
            profile_picture = form.cleaned_data.get("profile_picture")
            address = form.cleaned_data.get("address")
            bio = form.cleaned_data.get("bio")
            resume = form.cleaned_data.get("resume")

            up, _ = UserProfile.objects.update_or_create(user=user,
                                                         defaults=dict(phone_number=phone_number,
                                                                       address=address,
                                                                       bio=bio))
            up.profile_picture = profile_picture
            up.resume = resume
            up.save()
            messages.success(request, "Profile updated successfully !")
            return redirect("user_profile", request.user.id)
        else:
            messages.error(request, "Couldn't update the user profile !")
            return redirect("profile_update", request.user.id)
