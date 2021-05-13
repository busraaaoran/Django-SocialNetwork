from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.urls import conf
from django.views.generic.detail import DetailView
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


# Create your views here.

def follow_unfollow_profile(request):
    if request.method == "POST":
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.followings.all():
            my_profile.followings.remove(obj.user)
        else:
            my_profile.followings.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')


def my_profile_view(request):
    profile = Profile.objects.get(user= request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            

    context = {
        'profile' : profile,
        'form' : form,
        'confirm' : confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

def my_delete_view(request):
    user= request.user
    qs = Profile.objects.delete(user)

    context = {
        'qs': qs
    }

    return render(request, 'accounts/signup.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user= request.user)
    qs = Relationship.objects.invitations_received(profile)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/my_invitations.html', context)


def invite_profiles_list_view(request):
    user= request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/to_invite_list.html', context)

def profiles_list_view(request):
    user= request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/profile_list.html', context)

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
        return context

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.followings.all():
            follow = True
        else:
            follow = False
        context['follow'] = follow
        return context
    



