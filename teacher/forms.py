from django import forms
from django.contrib.auth.models import User

from .models import Teacher


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, label='Имя', widget=forms.TextInput(attrs={'class':
                                                                                                               'form-control',
                                                                                                           'placeholder': 'Иван '}))
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия', widget=forms.TextInput(attrs={'class':
                                                                                                                  'form-control',
                                                                                                              'placeholder': 'Иванов '}))
    username = forms.CharField(max_length=25, required=True, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class':
                                                                 'form-control',
                                                             'placeholder': 'login'}))
    password = forms.CharField(min_length=8, max_length=25, label='Пароль', widget=forms.PasswordInput(attrs={'class':
                                                                                                                  'form-control',
                                                                                                              'placeholder': 'password'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class':
                                                                                               'form-control',
                                                                                           'placeholder': 'user@email.com'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class TeacherForm(forms.ModelForm):
    address = forms.CharField(max_length=500, required=False, label='Адрес', widget=forms.TextInput(attrs={'class':
                                                                                                               'form-control',
                                                                                                           'placeholder': '190000, СПб, Дворцовая пл., д.1'}))
    mobile = forms.CharField(min_length=7, max_length=15, required=True, label='Контактный телефон',
                             widget=forms.TextInput(attrs={'class':
                                                               'form-control',
                                                           'placeholder': '+79111112233'}))
    profile_pic = forms.ImageField(required=False, label='Фото профиля')

    class Meta:
        model = Teacher
        fields = ['address', 'mobile', 'profile_pic']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, label='Имя', widget=forms.TextInput(attrs={'class':
                                                                                                               'form-control',
                                                                                                           'placeholder': 'Иван '}))
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия', widget=forms.TextInput(attrs={'class':
                                                                                                                  'form-control',
                                                                                                              'placeholder': 'Иванов '}))
    username = forms.CharField(max_length=25, required=True, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class':
                                                                 'form-control',
                                                             'placeholder': 'login'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class':
                                                                                               'form-control',
                                                                                           'placeholder': 'user@email.com'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserAdminChangePassword(forms.ModelForm):
    password = forms.CharField(min_length=8, max_length=25, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ['password']
