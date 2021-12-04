from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, TemplateView, RedirectView, DetailView
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
    success_url = '/confirmation/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {'form': self.form_class}
            return render(request, self.template_name, context)
        else:
            return redirect('login')


class ConfirmationPage(FormView):
    template_name = 'form-confirmation.html'
    form_class = DonationForm
    success_url = reverse_lazy('confirmation-page')

    def post(self, request, *args, **kwargs):
        cd = request.POST
        breakpoint()
        institution = Institution.objects.get(name=cd['organization'])
        donation = Donation.objects.create(quantity=int(cd['quantity']),
                                           institution=institution,
                                           address=cd['address'],
                                           phone_number=cd['phone_number'],
                                           city=cd['city'],
                                           zip_code=cd['zip_code'],
                                           pick_up_date=cd['pick_up_date'],
                                           pick_up_time=cd['pick_up_time'],
                                           pick_up_comment=cd['pick_up_comment'],
                                           user=request.user)
        for category in cd.getlist('categories'):
            cat = Category.objects.get(name=category)
            donation.categories.add(cat)
        donation.save()
        return render(request, 'form-confirmation.html')


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


class UserPage(DetailView):
    template_name = 'user_page.html'
    model = User
    pk_url_kwarg = 'user_pk'

    def get(self, request, *args, **kwargs):
        if not self.request.user.pk == kwargs['user_pk'] or not self.request.user.is_authenticated:
            return redirect('login')
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = Donation.objects.all().filter(user=self.request.user.pk)
        return context
