from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # if user is deleted, set room to null
    topic =  models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # if topic is deleted, set room to null
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants =  models.ManyToManyField(User, related_name='participants', blank=True) # we already have User reference in host, so we need to specify related_name
    updated = models.DateTimeField(auto_now=True) # every time theres a change
    created = models.DateTimeField(auto_now_add=True) # only initial creation

    class Meta:
        ordering = ['-updated', '-created'] # order by most recent

    def __str__(self):
        return str(self.name)
    

class  Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted, delete message
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # if room is deleted, delete message
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] # order by most recent

    def __str__(self):
        return self.body[0:50] # only show first 50 characters of message