from django.conf.urls import url,include
from . import views
from django.contrib.auth.views import \
    LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

app_name = 'stud_app'

urlpatterns = [
    url('login/', LoginView.as_view(template_name='stud_app/login.html'), name="login"),
    url('logout/', LogoutView.as_view(template_name='stud_app/logout.html'), name="logout"),
    url('home/', views.home, name="home"),
]