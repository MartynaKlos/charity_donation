from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, DonationForm
from .models import Donation, Institution, Category

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


class AddDonation(FormView):
    template_name = 'form.html'
    form_class = DonationForm
    success_url = 'landing-page'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {'form': self.form_class}
            return render(request, 'form.html', context)
        else:
            return redirect('login')


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        cd = form.cleaned_data
        if User.objects.filter(email=cd['email']).count() == 1:
            response = super().form_valid(form)
            user = User.objects.get(email=cd['email'])
            login(self.request, user)
            return response
        else:
            return redirect('register')


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



