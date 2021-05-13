from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.shortcuts import render
from .utils import get_random
from django.template.defaultfilters import slugify
from django.db.models import Q

class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.sender)
                accepted.add(rel.receiver)

        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)

        return available
        


    def get_all_profiles(self,me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Hello!...", max_length=400)
    email = models.EmailField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    followings = models.ManyToManyField(User, blank=True, related_name='followings')
    slug = models.SlugField(blank=True, unique=True)
    edited = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    avatar = models.ImageField(default= 'avatar.png', upload_to='avatars/')

    objects = ProfileManager()

    def get_followers(self):
        return self.followers.all()
    
    def get_followers_num(self):
        return self.followers.all().count()
    
    def get_followings(self):
        return self.followings.all()
    
    def get_followings_num(self):
        return self.followings.all().count()

    def __str__(self):
        return f"{self.user}--{self.created}"

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name)+ " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            
            while ex:
                to_slug= slugify(to_slug+" "+str(get_random()))
                ex = Profile.objects.filter(slug = to_slug).exists()

        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)

STATUS_CHOICES = (

    ('send', 'send'),
    ('accepted','accepted')

)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs
    

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    edited = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}--{self.receiver}--{self.status}"

