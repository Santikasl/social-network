from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Posts
from django import forms


class AuthForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин','class': 'js-input'}), max_length=12)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'js-input'}), max_length=60)


class NewPosts(forms.ModelForm):
    postImg = forms.ImageField(required=True, widget=forms.FileInput(
        attrs={'class': 'input-file', 'id': 'file', 'type': 'file', 'name': 'file', 'accept': 'image/jpeg, image/png, '
                                                                                              'image/jpg '}))
    description = forms.Textarea()

    class Meta:
        model = Posts
        fields = ['postImg', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Описание', 'maxlength': '2000','class': 'description-input'}),
        }


class ExtendedRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта', 'class': 'js-input js-input-email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'js-input js-input-password1'}), max_length=60)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'js-input js-input-password2'}), max_length=60,)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'js-input js-input-name','oninput':'this.value=this.value.toLowerCase()'}), max_length=12)

    def clean(self):
        # Определяем правило валидации
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            # Выбрасываем ошибку, если пароли не совпали
            raise forms.ValidationError('Пароли должны совпадать!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class Imgform(forms.ModelForm):
    img = forms.ImageField(required=False, widget=forms.FileInput(attrs={'onchange': 'this.form.submit()'}))

    class Meta:
        model = Profile
        fields = ['img']


