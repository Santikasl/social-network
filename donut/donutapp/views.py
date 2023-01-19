from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.views.generic import ListView, View
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import *
import random


class Index(ListView):
    queryset = Profile
    template_name = 'donutapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        form = AuthForm()
        register_form = ExtendedRegisterForm()
        context = {
            'form': form,
            'register_form': register_form,
        }
        return context

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')
        return super().get(request)


class SignIn(View):
    def post(self, request):
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            name = auth_form.cleaned_data['name']
            password = auth_form.cleaned_data['password']
            user = User.objects.filter(username=name).first()
            if not user:
                messages.error(request, "Пользователь не найден, пожалуйста зарегистрируйтесь")
                return redirect(request.META.get('HTTP_REFERER') + '#3')
            elif not check_password(password, user.password):
                messages.error(request, "Проверьте правильность пароля")
                return redirect(request.META.get('HTTP_REFERER') + '#3')
            else:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main')


class SignUp(View):
    def post(self, request):
        register_form = ExtendedRegisterForm(request.POST)
        if register_form.is_valid():
            password = request.POST.get("password1")
            password2 = request.POST.get("password2")
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            if User.objects.filter(username=username).first():
                messages.error(request, "Пользователь с таким ником уже существует. Войдите в аккаунт")
                return redirect(request.META.get('HTTP_REFERER') + '#3')
            elif User.objects.filter(email=email).first():
                messages.error(request, "Пользователь с таким e-mail уже существует. Войдите в аккаунт")
                return redirect(request.META.get('HTTP_REFERER') + '#3')
            elif password == password2:
                profile = Profile()
                profile.name = request.POST.get("username")
                profile.male = request.POST.get("male")
                profile.email = request.POST.get("email")
                profile.password = request.POST.get("password1")
                profile.user = register_form.save()
                profile.save()
                username = register_form.cleaned_data.get('username')
                raw_password = register_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('main')
            else:
                return redirect(request.META.get('HTTP_REFERER') + '#3')
        else:
            return redirect(request.META.get('HTTP_REFERER') + '#3')


def logout_user(request):
    logout(request)
    return redirect('index')


class Main(ListView):
    queryset = Profile
    template_name = 'donutapp/main.html'
    context_object_name = 'profile'

    def get(self, request):
        super().get(request)
        profile = Profile.objects.get(user=request.user)
        facts = Facts.objects.all()
        random_pk = random.randint(1, 46)
        random_facts = facts[random_pk]
        context = self.get_context_data()
        context = {
            'profile': profile,
            'random_facts': random_facts,
        }

        return self.render_to_response(context)


class UserProfile(ListView):
    queryset = Profile
    template_name = 'donutapp/profile.html'
    context_object_name = 'profile'

    def get(self, request):
        super().get(request)
        profile = Profile.objects.get(user=request.user)
        count_follow = profile.following.all().count()
        context = self.get_context_data()
        context = {
            'profile': profile,
            'count_follow': count_follow,
        }

        return self.render_to_response(context)
