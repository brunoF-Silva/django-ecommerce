from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.http import HttpResponse

class UserProfileCreateView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("CreateProfile")

class UserProfileUpdateView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("UpdateProfile")

class LoginView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Login")

class LogoutView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Logout")
