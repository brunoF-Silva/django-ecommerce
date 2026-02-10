
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from . import models
from . import forms

class BaseProfileView(View):
    template_name = 'profile/create.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        
        self.profile = None
        
        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(user=self.request.user).first()
            
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance = self.request.user
                    ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile
                )
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None                
                    ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None
                )
            }

        self.userform =  self.context['userform']
        self.profileform = self.context['profileform']
        
        if self.request.user.is_authenticated:
            self.template_name = 'profile/update.html'
        
        self.rendering = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.rendering
    
class CreateProfileView(BaseProfileView):
    """View to handle new user registration."""
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request,
                'There are errors in the registration form. Please check that all fields have been filled in correctly.'
            )
            return self.rendering
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        
        # Logged-in users
        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User, username=self.request.user.username)
            
            user.username = username
            
            if password:
                user.set_password(password)
                
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                print(self.profileform.cleaned_data)
                profile = models.UserProfile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()
        
        #Unlogged-in users (new)
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()
            
            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
            
            if password:
                authenticated_user = authenticate(
                    self.request,
                    username=user,
                    password=password
                )
                
                if authenticated_user:
                    login(self.request, user=user)
            
        self.request.session['cart'] = self.cart
        self.request.session.save()
        
        messages.success(
            self.request,
            'Your registration has been successfully created or updated.'
        )
        
        messages.success(
            self.request,
            'You are logged in and can complete your purchase.'
        )
        
        return redirect("product:cart")    


class UpdateProfileView(BaseProfileView):
    """
    View to handle updating an existing user's profile.
    This view inherits all logic from BaseProfileView.
    """
    pass


class LoginView(View):
    """View to handle user login."""

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        
        if not username or not password:
            messages.error(
                self.request,
                'Invalid username or password.'
            )
            return redirect('profile:create')
        
        user = authenticate(
            self.request, username=username, password=password
        )
        
        if not user:
            messages.error(
                self.request,
                'Invalid username or password.'
            )
            
        login(self.request, user=user)
        
        messages.success(
            self.request,
            'You\'re logged in and can now complete your purchase.'
        )
        
        return redirect('product:cart')


class LogoutView(View):
    """View to handle user logout."""

    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        
        logout(self.request)
        
        self.request.session['cart'] = cart
        self.request.session.save()
        
        return redirect("product:list")
