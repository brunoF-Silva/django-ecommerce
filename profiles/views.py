
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import HttpResponse

from . import models
from . import forms


class BaseProfileView(View):
    template_name = 'profile/create.html'
    
    def setup(self, *args, **kwargs):
    
        super().setup(*args, **kwargs)
        
        if self.request.user.is_authenticated:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance = self.request.user
                    ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None
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

        self.rendering = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.rendering

'''

class BaseProfileView(View):
    template_name = 'profile/create.html'

    def get(self, request, *args, **kwargs):
        """Displays the profile forms."""
        # For authenticated users, pass the user instance to the form
        if request.user.is_authenticated:
            user_form = forms.UserForm(
                instance=request.user, user=request.user)
            # Make sure a profile exists before trying to get an instance
            profile, created = models.UserProfile.objects.get_or_create(
                user=request.user)
            profile_form = forms.ProfileForm(instance=profile)
        else:
            user_form = forms.UserForm()
            profile_form = forms.ProfileForm()

        context = {
            'userform': user_form,
            'profileform': profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Processes the submitted profile forms."""
        if request.user.is_authenticated:
            profile, created = models.UserProfile.objects.get_or_create(
                user=request.user)
            user_form = forms.UserForm(
                request.POST, instance=request.user, user=request.user)
            profile_form = forms.ProfileForm(
                request.POST,
                request.FILES or None,
                instance=profile
            )
        else:
            user_form = forms.UserForm(request.POST)
            profile_form = forms.ProfileForm(
                request.POST, request.FILES or None)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)

            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect(reverse('profiles:create'))

        context = {
            'userform': user_form,
class CreateProfileView(BaseProfileView):
    pass

class UpdateProfileView(BaseProfileView):
    def get(self, *args, **kwargs):
        return HttpResponse("UpdateProfile")

class LoginView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Login")

class LogoutView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Logout")
'''
from django.shortcuts import render, redirect, reverse
from django.contrib import messages, auth
from django.views import View
from django.http import HttpResponse
from . import models, forms


# class BaseProfileView(View):
#     """
#     A base view for creating (registration) and updating user profiles.

#     Handles displaying the user/profile forms and processing the
#     submitted data, distinguishing between new and existing users.
#     """
#     template_name = 'profile/create.html'
    

#     def get(self, request, *args, **kwargs):
#         """
#         Handles the GET request to display the profile forms.

#         If a user is logged in, it pre-populates the forms with their
#         existing data. Otherwise, it displays empty forms for registration.
#         """
#         if request.user.is_authenticated:
#             # For an authenticated user, pass their instance AND the user object
#             user_form = forms.UserForm(
#                 instance=request.user, user=request.user)

#             # Ensure a profile exists for the user before getting an instance
#             profile, created = models.UserProfile.objects.get_or_create(
#                 user=request.user)
#             profile_form = forms.ProfileForm(instance=profile)
#         else:
#             # For a new user, show empty forms
#             user_form = forms.UserForm()
#             profile_form = forms.ProfileForm()

#         context = {
#             'userform': user_form,
#             'profileform': profile_form,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         """
#         Handles the POST request to validate and save the submitted form data.

#         If valid, it saves the user/profile and redirects.
#         If invalid, it re-renders the page with the forms containing error messages.
#         """
#         if request.user.is_authenticated:
#             # For an existing user, pass the instance to update it
#             profile, created = models.UserProfile.objects.get_or_create(
#                 user=request.user)

#             # Use data=request.POST to avoid the positional argument conflict
#             user_form = forms.UserForm(
#                 data=request.POST, instance=request.user, user=request.user)
#             profile_form = forms.ProfileForm(
#                 request.POST,
#                 request.FILES or None,
#                 instance=profile
#             )
#         else:
#             # For a new user, process the new data
#             # Use data=request.POST here as well
#             user_form = forms.UserForm(data=request.POST)
#             profile_form = forms.ProfileForm(
#                 request.POST, request.FILES or None)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)

#             password = user_form.cleaned_data.get('password')
#             if password:
#                 user.set_password(password)

#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()

#             if request.user.is_authenticated:
#                 messages.success(request, 'Profile updated successfully!')
#             else:
#                 messages.success(
#                     request, 'User created successfully! Please log in.')
#                 # Log the new user in automatically after registration
#                 # auth.login(request, user)

#             return redirect('profiles:create')

#         # If forms are invalid, re-render the page with errors
#         context = {
#             'userform': user_form,
#             'profileform': profile_form,
#         }

#         return render(request, self.template_name, context)


class CreateProfileView(BaseProfileView):
    """View to handle new user registration."""
    def post(self, request, *args, **kwargs):
        print(request.user)
        return self.rendering


class UpdateProfileView(BaseProfileView):
    """
    View to handle updating an existing user's profile.
    This view inherits all logic from BaseProfileView.
    """
    pass


class LoginView(View):
    """View to handle user login."""

    def get(self, *args, **kwargs):
        return HttpResponse("Login")


class LogoutView(View):
    """View to handle user logout."""

    def get(self, *args, **kwargs):
        return HttpResponse("Logout")
