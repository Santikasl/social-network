from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.views.generic import ListView, View
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from itertools import chain
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
    port = request.META.get('SERVER_PORT')
    host = request.META.get('REMOTE_ADDR')
    return redirect('http://' + host + ':' + port + '/' + '#3')


class Main(ListView):
    queryset = Profile
    template_name = 'donutapp/main.html'
    context_object_name = 'profile'

    def get(self, request):
        if not request.user.is_authenticated:
            port = request.META.get('SERVER_PORT')
            host = request.META.get('REMOTE_ADDR')
            return redirect('http://' + host + ':' + port + '/' + '#3')
        else:
            super().get(request)
            profile = Profile.objects.get(user=request.user)
            facts = Facts.objects.all()
            random_pk = random.randint(1, 46)
            random_facts = facts[random_pk]
            #
            follows = profile.user.following.all()
            users = [user for user in follows]
            post_follow = []
            for u in users:
                posts = Posts.objects.filter(user=u).first()

                if posts is not None:
                    post_follow.append(posts)

            context = self.get_context_data()
            post = NewPosts()
            context = {
                'profile': profile,
                'post': post,
                'random_facts': random_facts,
                'post_follow':post_follow,
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
            port = request.META.get('SERVER_PORT')
            host = request.META.get('REMOTE_ADDR')
            return redirect('http://' + host + ':' + port + '/' + '#3')
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


class Search(View):

    def post(self, request):
        res = None
        dataName = request.POST.get('dataName')
        qs = Profile.objects.filter(name__icontains=dataName)[:4]
        if len(qs) > 0 and len(dataName) > 0:
            data = []
            for pos in qs:
                item = {
                    'pk': pos.pk,
                    'name': pos.name,
                    'img': pos.img.url,
                }
                data.append(item)
            res = data
        else:
            res = 'Пользователь не найден'
        return JsonResponse({'data': res})


class SearchProfile(ListView):
    queryset = Profile
    template_name = 'donutapp/search_profile.html'
    context_object_name = 'searchProfile'

    def get(self, request, pk):
        anonim = False
        if not request.user.is_authenticated:
            anonim = True
            is_follow = False
        new_post = NewPosts()
        search_user = Profile.objects.get(pk=pk)
        profile = Profile.objects.filter(pk=pk).first()
        userFollowers = profile.following.all()
        followers = Profile.objects.filter(user__in=userFollowers)
        follow = profile.user.following.all()
        posts = Posts.objects.filter(user=search_user)
        try:
            user = Profile.objects.get(user=request.user)
            if profile == user:
                return redirect('profile')
            if user.user in profile.following.all():
                is_follow = True
            else:
                is_follow = False
        except Exception:
            user = None
            is_follow = False
        context = {
            'pk': pk,
            'is_follow': is_follow,
            'profile': profile,
            'posts': posts,
            'followers': followers,
            'follow': follow,
            'post': new_post,
            'anonim': anonim,
        }
        return render(request, 'donutapp/search_profile.html', context)


class Follow(View):
    def post(self, request):
        if not request.user.is_authenticated:
            port = request.META.get('SERVER_PORT')
            host = request.META.get('REMOTE_ADDR')
            return redirect('http://' + host + ':' + port + '/' + '#3')
        else:
            if request.method == 'POST':
                my_profile = Profile.objects.get(user=request.user)
                pk = request.POST.get('profile_pk')
                obj = Profile.objects.get(pk=pk)
                if my_profile.user in obj.following.all():
                    obj.following.remove(my_profile.user)
                else:
                    obj.following.add(my_profile.user)
                return redirect(request.META.get('HTTP_REFERER'))


class Statistics(ListView):
    queryset = Profile
    template_name = 'donutapp/statistics.html'

    def get(self, request):
        if not request.user.is_authenticated:
            port = request.META.get('SERVER_PORT')
            host = request.META.get('REMOTE_ADDR')
            return redirect('http://' + host + ':' + port + '/' + '#3')
        else:
            profile = Profile.objects.get(user=request.user)
            user_posts = Posts.objects.filter(user=profile)
            n = 0
            items = []
            all_post = []
            for post in user_posts:
                posts = {
                    'post': post,
                    'like': post.liked.all().count(),
                }
                all_post.append(posts)
                if post.liked.all().count() >= n:
                    items = {
                        'post': post,
                        'pk': post.pk,
                        'descriptions': post.description,
                        'img': post.img.url,
                        'like': post.liked.all().count(),
                        'user': post.user.id,
                        'imgUrl': post.user.img.url,
                        'name': post.user.name,
                    }
                    n = post.liked.all().count()
            followersUser = profile.following.all()
            followers = Profile.objects.filter(user__in=followersUser)
            count_male = 0
            count_female = 0
            for male in followers:
                if male.male == 'male':
                    count_male += 1
                else:
                    count_female += 1
            post = NewPosts()
            context = {
                'bestPost': items,
                'post': post,
                'count_male': count_male,
                'count_female': count_female,
                'all_post': all_post,
            }

            return render(request, 'donutapp/statistics.html', context)