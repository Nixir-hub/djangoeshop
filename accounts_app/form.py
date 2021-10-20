from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from eshopp_app.models import Profile


class SignUpForm(UserCreationForm):
    error_messages = {

        'password_mismatch': ('Hasła nie są takie same.'),
    }
    username = forms.CharField()
    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)
    class Meta:
        model = User
        form = "signup.html"
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        labels = {
            "username": "Nazwa użytkownika",
            "first_name": "Imię",
            "last_name":"Nazwisko",
            "email":"Adres email",
            "password1": "Hasło",
            "password2": "Powtórz hasło"
        }


class PasswordChangeForm(SetPasswordForm):
    class Meta:
        model = User
        form = "password_change_form.html"
        # fields = ('old_password', 'new_password1', 'new_password2')
        labels = {
            "old_password": "Stare hasło",
            "new_password1": "Nowe hasło",
            "new_password2": "Powtórz nowe hasło"
        }


class EditProfilForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("adres", "company_adres", "phone")
        labels = {
            "company_adres": "Adres firmy",
            "phone": "Telefon"
        }
