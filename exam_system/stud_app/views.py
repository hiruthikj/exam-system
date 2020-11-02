from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import *
# from .forms import MyForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'stud_app/home.html')
# class HomeView(generic.DetailView):
#     model = Student
#     template_name = 'exam_system/home.html'
