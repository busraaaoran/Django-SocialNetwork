from collections import namedtuple
from django.urls import path
from .views import ProfileDetailView, ProfileListView, follow_unfollow_profile, invite_profiles_list_view, invites_received_view, my_profile_view, profiles_list_view

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('myprofile/', my_profile_view, name='my-delete-view'),
    path('my-invitations/', invites_received_view, name='my-invitations-view'),
    path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('<pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('', follow_unfollow_profile, name='follow-unfollow-profile'),
    
]