from django.conf.urls import url,include
from django.urls import path
from . import views
from .forms import StudentLoginForm
from django.contrib.auth.views import *
    #LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

app_name = 'stud_app'

urlpatterns = [

    # path('', LoginView.as_view(template_name='stud_app/login.html',authentication_form=StudentLoginForm), name="login"),
    # url('login/',  views.StudentView.as_view(), name="login"),

    path('', views.blank_page),
    path('login/',  views.login_view, name="login"),
    path('logout/', LogoutView.as_view(template_name='stud_app/logout.html'), name="logout"),
    path('<username>/home/', views.home_view, name="home"),
    path('<username>/courses/', views.courses_view, name="courses"),
    path('<username>/exams/', views.exam_list_view, name="exams"),

]