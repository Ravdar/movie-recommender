from django.urls import path
from . import views

app_name = "mainapp"
urlpatterns = [path("", views.main_view, name="main_view_url"),
               path("results/", views.main_view, name="results_view_url")]