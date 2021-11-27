from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.models import ModelMultipleChoiceField, BaseModelForm

from .models import Category, Institution, User


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=64, widget=widgets.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, widget=widgets.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2


class UserChangeForm(BaseModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))


class DonationForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), widget=widgets.CheckboxSelectMultiple())
    quantity = forms.IntegerField()
    institution = forms.ModelChoiceField(Institution.objects.all())
    address = forms.CharField()
    phone_number = forms.IntegerField()
    city = forms.CharField(max_length=120)
    zip_code = forms.CharField()
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.Textarea()


