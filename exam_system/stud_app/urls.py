from django.conf.urls import url,include
from django.urls import path
from . import views
from .forms import StudentLoginForm
from django.contrib.auth.views import *
    #LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

app_name = 'stud_app'

urlpatterns = [

    # url('', LoginView.as_view(template_name='stud_app/login.html',authentication_form=StudentLoginForm), name="login"),
    # url('login/',  views.StudentView.as_view(), name="login"),
    path('login/',  views.login_view, name="login"),
    path('logout/', LogoutView.as_view(template_name='stud_app/logout.html'), name="logout"),
    # url(r'^home/(?P<username>[A-Za-z0-9]+)/$', views.home, name="home"),
    path('<username>/home/', views.home, name="home"),
]