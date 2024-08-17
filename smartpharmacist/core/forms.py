from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username','email','phone','account_type', 'national_id','is_staff', 'is_superuser', 'password1', 'password2','is_doctor','is_patient','is_pharmacist',]

    account_type = forms.ChoiceField(
        label='Account Type',
        widget=forms.Select(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        }),
        choices=User.ACCOUNT_TYPE_CHOICES,
        required=True,
    )

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

    phone = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

    password2 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )


    is_staff = forms.BooleanField(
        label='Create as Staff',
        required=False,
    )

    is_superuser = forms.BooleanField(
        label='Create as Superuser',
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.account_type = self.cleaned_data['account_type']

        user.is_staff = self.cleaned_data.get('is_staff')

        
        if self.cleaned_data.get('is_superuser'):
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()
        return user
    

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-zinc-500 focus:border-zinc-500 block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500'
        })
    )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email','phone','account_type']

    account_type = forms.ChoiceField(
        label='Account Type',
        widget=forms.Select,
        choices=User.ACCOUNT_TYPE_CHOICES,
        required=True,
    )


    is_staff = forms.BooleanField(
        label='Is Staff',
        required=False,
    )

    is_superuser = forms.BooleanField(
        label='Is Superuser',
        required=False,
    )





