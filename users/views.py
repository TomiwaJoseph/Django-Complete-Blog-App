from django.shortcuts import render, redirect
from .forms import SignupForm, UserUpdateForm, AuthorProfileUpdateForm, UserProfileUpdateForm
from main.views import *
from django.contrib import messages
from django.contrib.auth.models import User
from main.models import Blog
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account has been created successfully for {username}. Log in now!")
            return redirect('login')
    else:
        form = SignupForm()
        
    context = {
        'form': form,
        'length': length, 
        'all_cat_name': all_cat_name,
        'details': details,
    }
    return render(request, 'registration/register.html', context)

@login_required
def profile(request, user_):
    query = User.objects.filter(username=user_).first()
    user_details = Profile.objects.filter(user=query).first()

    if user_ != request.user.username:
        return redirect('profile', request.user)

    context = {
        'details': details, 'user_details': user_details,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'users/profile.html', context)

@login_required
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
        'carousel_src': carousel_sources, 'carousel_titles': carousel_titles,
        'carousel_authors': carousel_authors, 'carousel_dates': carousel_dates,
        'popular': range(len(carousel_authors)-1),
        'carou_year': carou_year,
        'carou_month': carou_month,
        'carou_day': carou_day,
        'carou_slug': carou_slug,
        'carou_comments': carou_comments,
        'popu_tags': popu_tags,
        'user_form': user_form, 'details': details,
        'author_profile_form': author_profile_form,
        'user_profile_form': user_profile_form,
        'length': length, 'all_cat_name': all_cat_name,
    }
    return render(request, 'users/edit_profile.html', context)

def author_profile_view(request, user_):
    query = User.objects.filter(is_staff=True)
    all_authors = [i.username for i in query]
    if user_ not in all_authors:
        return redirect('profile', request.user)

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

def know_user(request):
    return redirect('profile', user_=request.user.username)