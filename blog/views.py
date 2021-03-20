from django.shortcuts import render
from django.views.generic import ListView
from .models import Blog
import re


# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

class HomeView(ListView):
    model = Blog
    template_name = 'blog/index.html'

    # def get_queryset(self):
    #     return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        carou_pics = Blog.objects.all()
        all_published = Blog.objects.all()

        carousel_sources = []
        carousel_titles = []
        carousel_authors = []
        carousel_dates = []
        for i in carou_pics[:3]:
            find_all = re.findall(r'<img.*?/>', i.body)
            get_first = find_all[0]
            source = get_first.split()[2][5:-1]
            carousel_sources.append(source)
            carousel_titles.append(i.title)
            carousel_authors.append(i.author)
            carousel_dates.append(i.updated)

        pub_header_img = []
        pub_titles = []
        pub_authors = []
        pub_dates = []
        for i in all_published:
            find_all = re.findall(r'<img.*?/>', i.body)
            get_first = find_all[0]
            source = get_first.split()[2][5:-1]
            pub_header_img.append(source)
            pub_titles.append(i.title)
            pub_authors.append(i.author)
            pub_dates.append(i.updated)

        context = {
            'carousel_src': carousel_sources, 'carousel_titles': carousel_titles,
            'carousel_authors': carousel_authors, 'carousel_dates': carousel_dates,
            'pub_header_img': pub_header_img, 'pub_titles': pub_titles,
            'pub_authors': pub_authors, 'pub_dates': pub_dates, 'number': range(len(all_published)),
            'popular': range(len(carousel_authors)-1)
            }
        return context
