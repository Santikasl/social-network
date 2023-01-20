from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.views.generic import ListView, View
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from .models import *
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
            user = User.objects.filter(username=name.lower()).first()
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
            username = register_form.cleaned_data.get('username').lower()
            email = register_form.cleaned_data.get('email')
            if User.objects.filter(username=username).first():
                messages.error(request, "Пользователь с таким ником уже существует. Войдите в аккаунт")
                return redirect(request.META.get('HTTP_REFERER') + '#3')
            elif User.objects.filter(email=email).first():
                messages.error(request, "Пользователь с таким e-mail уже существует. Войдите в аккаунт")
                return redirect(request.META.get('HTTP_REFERER') + '#3')
            elif password == password2:
                profile = Profile()
                profile.name = request.POST.get("username").lower()
                profile.male = request.POST.get("male")
                profile.email = request.POST.get("email")
                profile.password = request.POST.get("password1")
                profile.user = register_form.save()
                profile.save()
                raw_password = register_form.cleaned_data.get('password1')
                user = authenticate(username=username.lower(), password=raw_password)
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
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            super().get(request)
            profile = Profile.objects.get(user=request.user)
            facts = Facts.objects.all()
            random_pk = random.randint(1, 46)
            random_facts = facts[random_pk]
            context = self.get_context_data()
            post = NewPosts()
            context = {
                'profile': profile,
                'post': post,
                'random_facts': random_facts,
            }

            return self.render_to_response(context)


class UserProfile(ListView):
    queryset = Profile
    template_name = 'donutapp/profile.html'
    context_object_name = 'profile'

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        imgForm = Imgform(request.POST, request.FILES)
        if imgForm.is_valid():
            if imgForm.cleaned_data['img'] is not None:
                profile.img = imgForm.cleaned_data['img']
                profile.save()
                return redirect('profile')
        else:
            return redirect('profile')

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            super().get(request)
            profile = Profile.objects.get(user=request.user)
            user_post = Posts.objects.filter(user=profile).order_by('-date')
            context = self.get_context_data()
            follow = profile.user.following.all()
            all_followers = profile.following.all()
            followers = Profile.objects.filter(user__in=all_followers)
            context = {
                'followers': followers,
                'number': user_post.count(),
                'follow': follow,
                'user_post': user_post,
                'imgForm': Imgform(),
                'profile': profile,
                'post': NewPosts(),

            }

            return self.render_to_response(context)


class NewPost(View):
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        post = Posts(user=profile)
        newPost = NewPosts(request.POST, request.FILES)
        if newPost.is_valid():
            post.img = newPost.cleaned_data['postImg']
            post.description = newPost.cleaned_data['description']
            post.save()
            return redirect('profile')


class Like(View):
    def post(self, request):
        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = Posts.objects.get(id=post_id)
        if user in post_obj.liked.all():
            like = 'Like'
            post_obj.liked.remove(user)
        else:
            like = 'Unlike'
            post_obj.liked.add(user)
        data = {
            'like_value': like,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)


def delite(request):
    if request.method == 'POST':
        post_id = request.POST['id']
        post = Posts.objects.get(id=post_id)
        post.delete()
    return redirect('profile')


def edit(request):
    id = request.POST.get('id', None)
    post2 = Posts.objects.get(id=id)
    post2.description = request.POST.get('description', None)
    post2.save()
    data2 = post2.description
    res_post2 = data2
    return JsonResponse({'data': res_post2})
