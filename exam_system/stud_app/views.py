from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.urls import reverse
# from django.views import generic

# from django.contrib import messages
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import *
# from .forms import *
# from django.views.generic.edit import FormView

# @login_required    #(login_url=reverse('stud_app:login'))
def home(request, username):
    return render(request, 'stud_app/home.html', context={
        'username' : username,
    })

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            student = Student.objects.get(user__username = username)
        except Student.DoesNotExist:
            context = { 
                'no_user' : True,
                'first_render' : False,
                'wrong_password' : False,
            } 
            return render(request, 'stud_app/login.html', context)
        else:
            if student.user.check_password(password):
                # return HttpResponse("HOME")
                # return HttpResponseRedirect('students/home/')
                return HttpResponseRedirect(reverse('stud_app:home', args=[username,]))
            else:
                context = { 
                'wrong_password' : True,
                'no_user' : False,
                'first_render' : False,
                } 
                return render(request, 'stud_app/login.html', context)
    else:
        context = { 
                'first_render' : True,
                'wrong_password' : False,
                'no_user' : False,
            } 
        return render(request, 'stud_app/login.html', context)

# class StudentView(FormView):
#     template_name = 'stud_app/login.html'
#     form_class = StudentForm
#     success_url = 'home/'

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     form.send_email()
    #     return super().form_valid(form)