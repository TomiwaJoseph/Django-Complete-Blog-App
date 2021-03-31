from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from .models import Blog, Category, Comment
import re
from taggit.models import Tag
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages




all_published = Blog.objects.all()[:6]
carou_pics = Blog.objects.all()

carousel_sources = []
carousel_titles = []
carousel_authors = []
carousel_dates = []
carou_year = []
carou_month = []
carou_day = []
carou_slug = []
carou_comments = []

for i in carou_pics[:3]:
    find_all = re.findall(r'<img.*?/>', i.body)
    get_first = find_all[0]
    source = get_first.split()[2][5:-1]
    carou_comments.append(len(i.comments.filter(active=True)))
    carousel_sources.append(source)
    carousel_titles.append(i.title)
    carousel_authors.append(i.author)
    carousel_dates.append(i.updated)
    carou_year.append(i.updated.year)
    carou_month.append(i.updated.month)
    carou_day.append(i.updated.day)
    carou_slug.append(i.slug)

pub_header_img = []
pub_titles = []
pub_authors = []
pub_dates = []
pub_year = []
pub_month = []
pub_day = []
pub_slug = []
pub_comments = []

for i in all_published:
    find_all = re.findall(r'<img.*?/>', i.body)
    get_first = find_all[0]
    source = get_first.split()[2][5:-1]
    pub_comments.append(len(i.comments.filter(active=True)))
    pub_header_img.append(source)
    pub_titles.append(i.title)
    pub_authors.append(i.author)
    pub_dates.append(i.updated)
    pub_year.append(i.updated.year)
    pub_month.append(i.updated.month)
    pub_day.append(i.updated.day)
    pub_slug.append(i.slug)


a = Category.objects.all()
all_cat_id = [i.id for i in a]
all_cat_name = [i.name for i in a]
length = [len(Blog.objects.filter(category=i)) for i in all_cat_id]


# Create your views here.
def index(request):
    context = {
        'carousel_src': carousel_sources, 'carousel_titles': carousel_titles,
        'carousel_authors': carousel_authors, 'carousel_dates': carousel_dates,
        'pub_header_img': pub_header_img, 'pub_titles': pub_titles,
        'pub_authors': pub_authors, 'pub_dates': pub_dates, 'number': range(len(all_published)),
        'popular': range(len(carousel_authors)-1),
        'pub_year': pub_year,'pub_month': pub_month,
        'pub_day': pub_day, 'pub_slug': pub_slug,
        'carou_year': carou_year, 'carou_month': carou_month,
        'carou_day': carou_day, 'carou_slug': carou_slug,
        'length': length, 'all_cat_name': all_cat_name,
        'carou_comments': carou_comments,
        'pub_comments': pub_comments,
        }
    return render(request, 'main/index.html', context)
    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        send_mail(name, message, email, 
            ['blog_owner@gmail.com'], fail_silently=False)
        
        messages.success(request, 'Message successfully sent!')
        return redirect('contact')
        
    context = {
        'carousel_src': carousel_sources, 'carousel_titles': carousel_titles,
        'carousel_authors': carousel_authors, 'carousel_dates': carousel_dates,
        'popular': range(len(carousel_authors)-1),
        'carou_year': carou_year,
        'carou_month': carou_month,
        'carou_day': carou_day,
        'carou_slug': carou_slug,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'main/contact.html', context)

def about(request):
    context = {
        'carousel_src': carousel_sources, 'carousel_titles': carousel_titles,
        'carousel_authors': carousel_authors, 'carousel_dates': carousel_dates,
        'popular': range(len(carousel_authors)-1),
        'carou_year': carou_year,
        'carou_month': carou_month,
        'carou_day': carou_day,
        'carou_slug': carou_slug,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'main/about.html', context)

def blog_detail(request, year, month, day, slug):
    blog = Blog.objects.filter(slug=slug)
    header_img = []
    images_indexes = []
    a = [i.tags.all() for i in blog][0]
    tags = [a[i] for i in range(len(a))]
    
    for i in blog:
        find_all = re.findall(r'<img.*?/>', i.body)
        get_first = find_all[0]
        source = get_first.split()[2][5:-1]
        header_img.append(source)
        category = i.category

        all_images = re.findall(r'<img.*?/>', i.body)
        find_p = re.findall(r'<p.*?</p>', i.body)
        images = [find_p.index(i) for i in find_p if '<img' in i]
        images_indexes.append(images)
        p_indexes = [find_p.index(i) for i in find_p if '<img' not in i]
        without = [i[3:-4] for i in find_p]
        without_tags = [i.split()[2][5:-1] if '<img' in i else i for i in without]

    post_comments = get_object_or_404(Blog, slug=slug)
    comments = post_comments.comments.filter(active=True)

    context = {
        'blog': blog, 'header_img': header_img,
        'carousel_src': carousel_sources, 'carousel_titles': carousel_titles,
        'carousel_authors': carousel_authors, 'carousel_dates': carousel_dates,
        'popular': range(len(carousel_authors)-1), 'category': category,
        'carou_year': carou_year, 'carou_month': carou_month,
        'carou_day': carou_day, 'carou_slug': carou_slug,
        'length': length, 'all_cat_name': all_cat_name,
        'tags': tags, 'content': without_tags,
        'begin_': range(p_indexes[0], images_indexes[0][1]),
        'end_': range(images_indexes[0][-1]+1, p_indexes[-1]+1),
        'images_indexes': images_indexes[0][1:],
        'current_id': i.id, 'comments': comments,
        'carou_comments': carou_comments,
        'pub_comments': pub_comments,
    }
    return render(request, 'main/blog-single.html', context)

def tag_finder(request, tag):
    object_list = Blog.objects.all()
    tagg = get_object_or_404(Tag, slug=tag)
    object_list = object_list.filter(tags__in=[tagg])

    tag_header_img = []
    tag_titles = []
    tag_authors = []
    tag_dates = []
    tag_year = []
    tag_month = []
    tag_day = []
    tag_slug = []

    for i in object_list:
        find_all = re.findall(r'<img.*?/>', i.body)
        get_first = find_all[0]
        source = get_first.split()[2][5:-1]
        tag_header_img.append(source)
        tag_titles.append(i.title)
        tag_authors.append(i.author)
        tag_dates.append(i.updated)
        tag_year.append(i.updated.year)
        tag_month.append(i.updated.month)
        tag_day.append(i.updated.day)
        tag_slug.append(i.slug)
    context = {
        'tag_titles': tag_titles,
        'tag_header_img': tag_header_img,
        'tag_authors': tag_authors,
        'tag_dates': tag_dates,
        'tag_year': tag_year,
        'tag_month': tag_month,
        'carou_comments': carou_comments,
        'pub_comments': pub_comments,
        'tag_day': tag_day,
        'tag_slug': tag_slug,
        'tag_number': range(len(tag_titles)), 'tag': tag,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'main/tag_finder.html', context)

def category_finder(request, tag):
    cat = Category.objects.filter(name=tag)
    cat_id = [i.id for i in cat]
    object_list = Blog.objects.filter(category=cat_id[0])

    cat_header_img = []
    cat_titles = []
    cat_authors = []
    cat_dates = []
    cat_year = []
    cat_month = []
    cat_day = []
    cat_slug = []

    for i in object_list:
        find_all = re.findall(r'<img.*?/>', i.body)
        get_first = find_all[0]
        source = get_first.split()[2][5:-1]
        cat_header_img.append(source)
        cat_titles.append(i.title)
        cat_authors.append(i.author)
        cat_dates.append(i.updated)
        cat_year.append(i.updated.year)
        cat_month.append(i.updated.month)
        cat_day.append(i.updated.day)
        cat_slug.append(i.slug)
    context = {
        'cat_titles': cat_titles,
        'cat_header_img': cat_header_img,
        'cat_authors': cat_authors,
        'cat_dates': cat_dates,
        'cat_year': cat_year,
        'cat_month': cat_month,
        'pub_comments': pub_comments,
        'cat_day': cat_day,
        'cat_slug': cat_slug,
        'cat_number': range(len(cat_titles)), 'tag': tag,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'main/category_finder.html', context)

def search_it(request):
    get_search = request.POST.get('search_input')
    object_list = Blog.objects.filter(title__contains=get_search)

    search_header_img = []
    search_titles = []
    search_authors = []
    search_dates = []
    search_year = []
    search_month = []
    search_day = []
    search_slug = []

    for i in object_list:
        find_all = re.findall(r'<img.*?/>', i.body)
        get_first = find_all[0]
        source = get_first.split()[2][5:-1]
        search_header_img.append(source)
        search_titles.append(i.title)
        search_authors.append(i.author)
        search_dates.append(i.updated)
        search_year.append(i.updated.year)
        search_month.append(i.updated.month)
        search_day.append(i.updated.day)
        search_slug.append(i.slug)
    context = {
        'search_titles': search_titles,
        'search_header_img': search_header_img,
        'search_authors': search_authors,
        'search_dates': search_dates,
        'search_year': search_year,
        'search_month': search_month,
        'search_day': search_day,
        'search_slug': search_slug,
        'pub_comments': pub_comments,
        'get_search': get_search,
        'search_number': range(len(search_titles)),
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'main/search_results.html',context)

def newsletter(request):
    get_search = request.POST.get('email')
    context = {

    }
    return render(request, 'main/newsletter_success.html',context)

class ComposeBlogView(CreateView):
    model = Blog
    template_name = 'main/compose.html'

    # fields = '__all__'
    fields = ['title', 'category', 'body', 'tags']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['length'] = length
        context['all_cat_name'] = all_cat_name
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def archive(request, day):
    if day == 'today':
        cat = Blog.objects.filter(publish__day=timezone.now().day)

    if day == 'past-7-days':
        cat = Blog.objects.filter(
    publish__day__lte=datetime.today().strftime('%d'), 
    publish__day__gte=int(datetime.today().strftime('%d')) - 7)


    if day == 'this-month':
        cat = Blog.objects.filter(publish__month=timezone.now().month)

    if day == 'this-year':
        cat = Blog.objects.filter(publish__year=timezone.now().year)

    pub_header_img = []
    pub_titles = []
    pub_authors = []
    pub_dates = []
    pub_year = []
    pub_month = []
    pub_day = []
    pub_slug = []

    for i in cat:
        find_all = re.findall(r'<img.*?/>', i.body)
        get_first = find_all[0]
        source = get_first.split()[2][5:-1]
        pub_header_img.append(source)
        pub_titles.append(i.title)
        pub_authors.append(i.author)
        pub_dates.append(i.updated)
        pub_year.append(i.updated.year)
        pub_month.append(i.updated.month)
        pub_day.append(i.updated.day)
        pub_slug.append(i.slug)

    context = {
        'pub_header_img': pub_header_img, 'pub_titles': pub_titles,
        'pub_authors': pub_authors, 'pub_dates': pub_dates, 'number': range(len(cat)),
        'pub_year': pub_year,
        'pub_month': pub_month,
        'pub_day': pub_day,
        'pub_slug': pub_slug,

        'pub_comments': pub_comments, 'day': day,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'main/archive.html',context)

def comment(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    current_blog_id = request.POST.get('id')
    post = Blog.objects.filter(id=current_blog_id).first()

    new_comment = Comment(post=post, name=name,
        email=email, body=message)
    new_comment.save()

    year = post.created.year
    month = post.created.month
    day = post.created.day
    slug = post.slug
    
    return redirect('blog_detail', year=year,
        month=month, day=day, slug=slug)