from tkinter import CASCADE
from tokenize import Name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User, Group
from ckeditor.fields import RichTextField

# Custom Authentication
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")

# Create your models here.
# class user_info(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.AutoField(primary_key=True)
#     email = models.EmailField(null=True, blank=True, max_length=255)
#     
#     def __str__(self):
#         return f"User {self.id} is {self.name}"

class Courses(models.Model):
    
    course_code = models.CharField(max_length=255, primary_key=True)
    course_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"

class CourseInstructor(models.Model):
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="CourseInstructor")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="CourseInformation")

    def __str__(self):
        return f"{self.course}"
class Lab_Manual(models.Model):
    lab_name = models.CharField(max_length=255)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="LabInstructor")
    course = models.ForeignKey(CourseInstructor, on_delete=models.CASCADE, related_name="Courseinformation")
    activity_name = models.CharField(max_length=255)
    activity_no = models.FloatField()
    objectives = RichTextField(blank=True, null=True)
    ilo = RichTextField(blank=True, null=True)
    discussion = RichTextField(blank=True, null=True)
    resources = RichTextField(blank=True, null=True)
    procedure =RichTextField(blank=True, null=True)
    results = RichTextField(blank=True, null=True)
    supplementary = RichTextField(blank=True, null=True)
    observation = RichTextField(blank=True, null=True)
    conclusion = RichTextField(blank=True, null=True)

    def __str__(self):
        return f"Activity {self.activity_no} entitled {self.activity_name}"

class Sharing(models.Model):
    LabManual = models.ForeignKey(Lab_Manual, on_delete=models.CASCADE, related_name="LabInformation")
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="SharedTo")

    def __str__(self):
        return f"{self.LabManual.activity_name} is shared to {self.instructor.user}"