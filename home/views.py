# Imports
from multiprocessing import context
from tkinter import Widget
from xml.dom.minidom import Document
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import *
from .filters import LabFilter
from .forms import *

from docx import *
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from mailmerge import MailMerge


# Create your views here.
# ----------------- Document Download ----------------- #
def TeacherDocument(request, pk):
    user = request.user
    labmanual = Lab_Manual.objects.get(id=pk)

    template = os.path.join(settings.TEMPLATE_ROOT, 'labtemplate.docx')
    document = MailMerge(template)

    document.merge(
    title=f'{labmanual.activity_name}',
    actno=f'{labmanual.activity_no}',
    coursecode=f'{labmanual.course.course.course_code}',
    coursetitle=f'{labmanual.course.course.course_title}',
    instructor=f'{labmanual.instructor}',
    objectives=f'{labmanual.objectives}',
    ilo=f'{labmanual.ilo}',
    discussion=f'{labmanual.discussion}',
    resources=f'{labmanual.resources}',
    procedure=f'{labmanual.procedure}',
    results=f'{labmanual.results}',
    supplementary=f'{labmanual.supplementary}',
    observation=f'{labmanual.observation}',
    conclusion=f'{labmanual.conclusion}'
)
    document.write(os.path.join(settings.TEMPLATE_ROOT, f'{labmanual.lab_name}.docx'))
    print(settings.TEMPLATE_ROOT)

    file_dir = os.path.join(settings.TEMPLATE_ROOT, f'{labmanual.lab_name}.docx')
    if os.path.exists(file_dir):
        with open(file_dir, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_dir)
            print('gumana')
            return response
    return redirect('mainsite:viewlab', pk=pk)

# ----------------- Authentication ----------------- #

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('mainsite:home')
    else:
        reg_form = UserAdminCreationForm()
        if 'login-submit' in request.POST:
            if request.method == 'POST':
                email = request.POST.get("email")
                password = request.POST.get("password")

                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('mainsite:home')
                    
                else:
                    messages.info(request,'Username OR Password is incorrect')
        elif 'register-submit' in request.POST:
            if request.method == 'POST':
                regform = UserAdminCreationForm(request.POST)
                if regform.is_valid():
                    regform.save()
                    messages.success(request, 'Successfully created an account')
                else:
                    messages.success(request, 'Failed to created an account')
                
    context = {'reg_form': reg_form}
    return render(request, "main/authenticate.html", context)

@login_required(login_url='mainsite:login')
def logoutUser(request):
    logout(request)
    return redirect('mainsite:login')

# ----------------- Home ----------------- #

@login_required(login_url='mainsite:login')
def home(request):
    user = request.user
    if request.method == 'POST':
        searched = request.POST['searched']

        return redirect('mainsite:search', pk=searched)
    else:
        labmanuals = Lab_Manual.objects.filter(instructor=user)
        context = {'labmanuals': labmanuals}
        return render(request, "main/home.html", context)

@login_required(login_url='mainsite:login')
def about_us(request):
    return render(request, "main/aboutus.html")

@login_required(login_url='mainsite:login')
def contact(request):
    return render(request, "main/contact.html")

@login_required(login_url='mainsite:login')
def searchpage(request, pk):
    if request.method == 'POST':
        searched = request.POST['searched']

        return redirect('mainsite:search', pk=searched)

    labmanuals = Lab_Manual.objects.filter(Q(lab_name__icontains=pk) | Q(activity_name__icontains=pk))

    return render(request, "main/search.html", {
        'searched': pk,
        'labmanuals': labmanuals,
    })

# ----------------- Profile ----------------- #

@login_required(login_url='mainsite:login')
def profile(request):
    user = request.user
    courselist = CourseInstructor.objects.filter(instructor=user)

    for i in courselist:
        if i.course.course_code in request.POST:
            delcourse = CourseInstructor.objects.get(instructor=user, course=i.course)
            delcourse.delete()
            messages.success(request, 'Course successfully Deleted')
    
    if 'eprofile' in request.POST:
        return redirect('mainsite:editprofile')

    context = {"user": user, "courses": CourseInstructor.objects.filter(instructor=user)}
    return render(request, "main/profile.html", context)

@login_required(login_url='mainsite:login')
def editProfile(request):
    user = request.user
    
    form = EditProfile(instance=user)

    context = {"user": user, "form": form}
    return render(request, "main/editprofile.html", context)

@login_required(login_url='mainsite:login')
def editCourse(request):
    user = request.user

    courselist = CourseInstructor.objects.filter(instructor=user)
    courseform = NewCourse(initial={'instructor': user})

    if 'addcourse' in request.POST:
        form = NewCourse(request.POST)
        getcourse = request.POST.get("course")
        if form.is_valid():
            try:
                checkCourse = CourseInstructor.objects.get(instructor=user, course=getcourse)
            except ObjectDoesNotExist:
                form.save()

            messages.success(request, 'Course Already Exist to this user')

    for i in courselist:
        if i.course.course_code in request.POST:
            delcourse = CourseInstructor.objects.get(instructor=user, course=i.course)
            delcourse.delete()
            messages.success(request, 'Course successfully Deleted')

    context = {"user": user, "courses": CourseInstructor.objects.filter(instructor=user) ,"form": courseform}
    return render(request, "main/editcourse.html", context)

# ----------------- Laboratory ----------------- #

@login_required(login_url='mainsite:login')
def createlab(request):
    user = request.user
    usercourselist = CourseInstructor.objects.filter(instructor=user)

    form = NewLab(initial={'instructor': user})
    form.fields['course'].queryset = usercourselist
    if 'newlab' in request.POST:
        form = NewLab(request.POST,
            request.FILES, initial={'instructor': user})
        if form.is_valid():
            form.save()
            return redirect('mainsite:home')

    return render(request, 'main/createlab.html', {
        'form': form,
        })

@login_required(login_url='mainsite:login')
def viewlab(request, pk):
    user = request.user
    labmanual = Lab_Manual.objects.get(id=pk)
    if 'editlab' in request.POST:
        return redirect('mainsite:editlab', pk=pk)
    if 'teacherdownload' in request.POST:
        return redirect('mainsite:teacherdownload', pk=pk)


    context = {'labelements': labmanual}
    return render(request, 'main/viewlab.html', context)

@login_required(login_url='mainsite:login')
def editlab(request, pk):
    user = request.user
    labmanual = Lab_Manual.objects.get(id=pk)
    if labmanual.instructor == request.user:
        form = NewLab(instance=labmanual)
        if request.method == 'POST':
            form = form = NewLab(request.POST,
            request.FILES, instance=labmanual)
            if form.is_valid():
                form.save()
                return redirect('mainsite:viewlab', pk=pk)
        context = {'form': form, 'labelements': labmanual}
        return render(request, 'main/createlab.html', context )
    else:
        redirect('mainsite:home')

    