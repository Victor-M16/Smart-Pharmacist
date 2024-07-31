from django.shortcuts import render

# Create your views here.

# def home(request):
#     return render(request, "index.html")

def home(request):
    return render(request, "core/doc-home.html")
