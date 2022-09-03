from django.shortcuts import render


def index_views(request):
    return render(request, "home/index.html")

def about_views(request):
    return render(request, "home/about.html")

def contact_views(request):
    return render(request, "home/contact.html")