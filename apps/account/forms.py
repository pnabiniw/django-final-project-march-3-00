from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=20)
    middle_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20)
    address = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=14)
    bio = forms.CharField(widget=forms.Textarea())
