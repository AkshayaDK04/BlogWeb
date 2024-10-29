# models.py
from django.db import models
from django.contrib.auth.models import User

import os
from django.utils import timezone

def upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{base}_{timestamp}{extension}"
    return os.path.join('/images/', new_filename)



class Content(models.Model):
    CONTENT_TYPES = (
        ('calligraphy', 'Calligraphy'),
        ('blog', 'Blog'),
        ('quote', 'Quote'),
        ('poem', 'Poem'),
        ('essay', 'Essay'),
    )
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_content', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.ForeignKey(Content, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.content.title}'
