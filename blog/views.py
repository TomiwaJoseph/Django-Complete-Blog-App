from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


class HomeView(ListView):
    template_name = 'blog/index.html'