from django.db import models
import uuid
from users.models import Profile
# Create your models here. DB schema.

# DJANGO MODEL FORMS
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)    # null = false by default, MUST BE INCLUDED
    description = models.TextField(null=True, blank=True)   # allowed to create a null, empty value in DB
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_code = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)  # auto_now_add = True adds time stamp automatically
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
    # UUIDField is unique, overriding `id` attribute that begins at 1. set as primary_key and NOT editable once created

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["time_created"]    # - changes from descending to ascending


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'), 
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # will delete all reviews IF project deleted
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    time_created = models.DateTimeField(auto_now_add=True)  # auto_now_add = True adds time stamp automatically
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    class Meta:
        unique_together = [["owner", "project"]]
    def __str__(self):
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    time_created = models.DateTimeField(auto_now_add=True)  # auto_now_add = True adds time stamp automatically
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self):
        return self.name

