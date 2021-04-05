from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignupForm, UserUpdateForm, AuthorProfileUpdateForm, UserProfileUpdateForm
from main.views import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from main.models import Blog
from django.contrib.auth import views as auth_views


# Create your views here.
class UserRegister(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['length'] = length 
        context['all_cat_name'] = all_cat_name
        return context

def profile(request, user_):
    if user_ != request.user.username:
        raise PermissionDenied

    context = {
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'users/profile.html', context)


def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        author_profile_form = AuthorProfileUpdateForm(request.POST, 
            request.FILES, instance=request.user.profile)
        user_profile_form = UserProfileUpdateForm(request.POST, 
            request.FILES, instance=request.user.profile)
        if request.user.is_staff and user_form.is_valid() and author_profile_form.is_valid():
            user_form.save()
            author_profile_form.save()
            messages.success(request, 'Profile successfully updated!')
            return redirect('profile', user_=request.user.username)
        else:
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Profile successfully updated!')
            return redirect('profile', user_=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        author_profile_form = AuthorProfileUpdateForm(instance=request.user.profile)
        user_profile_form = UserProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'popu_tags': popu_tags,
        'user_form': user_form,
        'author_profile_form': author_profile_form,
        'user_profile_form': user_profile_form,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'users/edit_profile.html', context)


def author_profile_view(request, user_):
    query = User.objects.filter(is_staff=True)
    all_authors = [i.username for i in query]
    if user_ not in all_authors:
        raise PermissionDenied

    author_details = User.objects.filter(username=user_)

    query_2 = User.objects.filter(username=user_).first()
    first_two = Blog.objects.filter(author=query_2)[:2]

    search_header_img = []
    search_titles = []
    search_authors = []
    search_dates = []
    search_year = []
    search_month = []
    search_day = []
    search_slug = []
    search_author_pics = []
    pub_comments = []

    for i in first_two:
        find_all = re.findall(r'<img.*?/>', i.body)
        get_first = find_all[0]
        source = get_first.split()[2][5:-1]
        pub_comments.append(len(i.comments.filter(active=True)))
        search_header_img.append(source)
        search_titles.append(i.title)
        search_authors.append(i.author)
        search_dates.append(i.updated)
        search_year.append(i.updated.year)
        search_month.append(i.updated.month)
        search_day.append(i.updated.day)
        search_slug.append(i.slug)
        search_author_pics.append(i.author.profile.image.url)

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
        'search_author_pics': search_author_pics,
        'search_number': range(len(search_titles)),
        'author_details': author_details,
        'length': length, 'all_cat_name': all_cat_name,
        'popu_tags': popu_tags,
    }
    return render(request, 'users/profile_view.html', context)
