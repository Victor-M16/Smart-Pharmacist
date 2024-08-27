from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm

from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import password_validators_help_texts

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'account_type', 'specialty', 'phone', 'national_id', 'dob', 'gender', 'password1', 'password2']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username','email','phone','account_type', 'national_id','is_staff', 'is_superuser', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get help texts from the password validators
        password_help_texts = password_validators_help_texts()
        # Set the help text for the password1 field as a list
        self.fields['password1'].help_text = password_help_texts

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

    def confirm_login_allowed(self, user):
        # This method is inherited from AuthenticationForm and can be used to add extra
        # checks for login permission. Make sure it's not preventing non-superusers.
        pass

    def clean(self):
        # Call the parent class's clean method to get the username and password
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Authenticate the user using Django's built-in authentication system
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password.")
        
        # Optionally, you can add additional checks here (e.g., if the user is active)

        return cleaned_data

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





