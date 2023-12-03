from django.shortcuts import render

def search_view(request):
    return render(request, "mainapp/search_view.html", {})

