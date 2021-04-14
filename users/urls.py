from django.urls import path
from .views import (profile, register,
    edit_profile, author_profile_view, know_user
    )


urlpatterns = [
    path('know_user/', know_user, name='know_user'),
    path('register/', register, name='register'),
    path('profile/<slug:user_>/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/author/<slug:user_>/', author_profile_view, name='view_profile'),
]