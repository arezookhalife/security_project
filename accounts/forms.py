from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور اشتباه است.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }

    username = forms.CharField(label='Username', max_length=150,
                               widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user