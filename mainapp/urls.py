from django.urls import path
from . import views

app_name = "mainapp"
urlpatterns = [path("", views.main_view, name="main_view_url"),
               path("about/", views.about_view, name="about_view_url"),]