from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import widgets


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=64, widget=widgets.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, widget=widgets.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        cd = super().clean()
        email = cd['email']
        password = cd['password']
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise ValidationError('Niepoprawny email lub hasło!')