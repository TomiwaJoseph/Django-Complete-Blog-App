from django.urls import path
from . import views
from .views import ComposeBlogView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',
        views.blog_detail, 
        name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('tags/<slug:tag>/', views.tag_finder, name='tag_finder'),
    path('category/<slug:tag>/', views.category_finder, name='category_finder'),
    path('search_results/', views.search_it, name='search_it'),
    path('newsletter_sub/', views.newsletter, name='newsletter'),
    path('compose/', ComposeBlogView.as_view(), name='compose'),
    path('archive/<slug:day>/', views.archive, name='archive'),
]
