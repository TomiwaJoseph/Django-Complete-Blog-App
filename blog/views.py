from django.shortcuts import render
# from django.generic.views import Create

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

