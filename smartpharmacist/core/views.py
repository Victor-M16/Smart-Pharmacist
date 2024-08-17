from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import *
from .forms import CustomAuthenticationForm
from .models import *


class CustomRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        context = {
            'form': form,
            'title': 'register',
        }
        return render(request, 'auth/register.html', context)
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username} !")    
            return redirect('login')
        else:
            messages.warning(request, "Registration failed. Please correct the errors below.")
            
        context = {
            'form': form,
            'title': 'register',
        }
        return render(request, 'auth/register.html', context)
    


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'login'
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(self.get_context_data(form=form))

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        user = request.user
        context = {'title': 'home', 'form': form}

        if user.account_type == 'Doctor':
            return render(request, 'core/doc-home.html', context)
        elif user.account_type == 'Patient':
            return render(request, 'core/pat-home.html', context)
        else:
            return render(request, 'core/pharm-home.html', context)
    

#CRUD for Users
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = 'users'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User 
    template_name = "users/user_form.html"
    success_url = reverse_lazy('user_list')
    form_class = CustomUserChangeForm
        
    def form_valid(self, form):
        if form.instance.username == self.request.user.username:
            form.instance.username = None
        if form.instance.first_name == self.request.user.first_name:
            form.instance.first_name = None
        if form.instance.email== self.request.user.email:
            form.instance.femail = None
        if form.instance.last_name == self.request.user.last_name:
            form.instance.last_name = None
        if form.instance.phone == self.request.user.phone:
            form.instance.phone = None
        if form.instance.account_type == self.request.user.account_type:
            form.instance.account_type = None

        return super().form_valid(form)
       
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User 
    form_class = CustomUserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy('user_list')

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')



def doc_prescription(request):
    return render(request, "core/doc-presc.html", {'title': 'prescriptions'})

def create_patient(request):
    return render(request, "core/new-patient.html", {'title': 'new patient'})

def create_prescription(request):
    return render(request, "core/new-prescription.html", {'title': 'new prescription'})


def create_medication(request):
    return render(request, "core/new-medication.html", {'title': 'new medication'})


