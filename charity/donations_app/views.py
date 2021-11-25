from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm
from .models import Donation, Institution

User = get_user_model()


class LandingPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations_app'] = Donation.objects.all().count()
        context['institutions'] = Donation.objects.all().values_list('institution').distinct().count()
        context['foundations'] = Institution.objects.filter(type=1)
        context['organisations'] = Institution.objects.filter(type=2)
        context['locals'] = Institution.objects.filter(type=3)
        return context


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'form.html')


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.user)
        return response


class Logout(RedirectView):
    url = reverse_lazy('landing-page')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        cd = form.cleaned_data
        User.objects.create_user(email=cd['email'],
                                 password=cd['password'],
                                 first_name=cd['first_name'],
                                 last_name=cd['last_name'])
        return super().form_valid(form)



