from django.urls import path

from . import views

app_name = "mainsite"

urlpatterns = [
    #path("", views.welcome, name="home"), #go to views.index
    path("login", views.loginpage, name="login"),
    path("logout", views.logoutUser, name="userexit"),

    path("", views.home, name="home"),
    path("search/<str:pk>", views.searchpage, name="search"),
    path("about", views.about_us, name="aboutus"),
    path("contact", views.contact, name="contact"),

    # Profile URLS
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.editProfile, name="editprofile"),
    path("profile/courses", views.editCourse, name="editcourse"),

    # Lab Manual URLS
    path("create", views.createlab, name='newlab'),
    path("view/<str:pk>", views.viewlab, name='viewlab'),
    path("edit/<str:pk>", views.editlab, name='editlab'),
    path("share/<str:pk>", views.sharedlab, name='sharinglist'),

    path("download/teacher/<str:pk>", views.TeacherDocument, name='teacherdownload'),
]