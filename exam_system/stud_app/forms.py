from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

from django import forms


class StudentLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(StudentLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'})
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ('is_correct',)

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('choice',)

# class ChoiceForm(forms.ModelForm):
#     class Meta:
#         model = Choice
#         fields = ['choice_text',]