from django.urls import path
from . import views

app_name = "mainapp"
urlpatterns = [path("", views.search_view, name="search_view_url")]