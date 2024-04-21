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


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=14)
    profile_picture = forms.FileField(required=False)
    address = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea())
    resume = forms.FileField(required=False)

    def validate(self):
        print("In resume")
        cleaned_data = self.cleaned_data
        resume = self.cleaned_data.get("resume")
        if resume:
            extension = resume.name.split(".")[-1]  # resume.pdf  ["resume", "pdf"]
            if extension not in ["pdf", "PDF"]:
                raise forms.ValidationError("Please upload resume in pdf !")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            try:
                profile = user.userprofile
            except:
                pass
            else:
                self.fields["phone_number"].initial = profile.phone
                self.fields["profile_picture"].initial = profile.profile_picture
                self.fields["address"].initial = profile.address
                self.fields["bio"].initial = profile.bio
                self.fields["resume"].initial = profile.resume
