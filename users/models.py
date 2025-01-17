from django.db import models
from django.contrib.auth.models import User # django builtin user model
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")
    social_github = models.CharField(max_length=100, blank=True, null=True)
    social_twitter = models.CharField(max_length=100, blank=True, null=True)
    social_linkedin = models.CharField(max_length=100, blank=True, null=True)
    social_website = models.CharField(max_length=100, blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)  # auto_now_add = True adds time stamp automatically
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self):
        return str(self.username)
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    skill_name = models.CharField(max_length=200, blank=True, null=True)
    skill_description = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)  # auto_now_add = True adds time stamp automatically
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.skill_name)



