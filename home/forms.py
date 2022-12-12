from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

from django.contrib.auth import get_user_model


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']

class EditProfile(ModelForm):
    class Meta:
        model = CustomUser
        fields= ['first_name',
        'last_name',
        'password'
        ]

class SearchLab(ModelForm):
    class Meta:
        model = Lab_Manual
        fields = ['lab_name',
        'instructor',
        'course',
        'activity_name',
        ]
        

class NewCourse(ModelForm):
    class Meta:
        model = CourseInstructor
        fields = '__all__'

        

class NewLab(ModelForm):
    class Meta:
        model = Lab_Manual
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"createlabinput"})

    
class ShareLab(ModelForm):
    class Meta:
        model = Sharing
        fields = '__all__'
        