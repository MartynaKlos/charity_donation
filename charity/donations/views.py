from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

from .models import Donation, Institution, User


class LandingPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = Donation.objects.all().count()
        context['institutions'] = Donation.objects.all().values_list('institution').distinct().count()
        context['foundations'] = Institution.objects.filter(type=1)
        context['organisations'] = Institution.objects.filter(type=2)
        context['locals'] = Institution.objects.filter(type=3)
        return context


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'form.html')


class Login(FormView):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class Register(FormView):
    template_name = 'form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        cd = super().form_valid(form)
        User.objects.create_user(email=cd['email'],
                                 password=cd['password1'])
        return cd


