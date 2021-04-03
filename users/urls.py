from django.urls import path
from .views import (UserRegister, profile, 
    edit_profile, author_profile_view,
    )


urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('profile/<slug:user_>/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/author/<slug:user_>/', author_profile_view, name='view_profile'),
]