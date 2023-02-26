from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime 

CHOICES = (('User', 'USER'), ('Post', 'POST'), ('Both', 'BOTH'))
# Create your models here.
class Tag(models.Model):
    tags = models.CharField(max_length=1000)
    followers = models.ManyToManyField(User, related_name='tag_followers')
    
    def __str__(self):
        return self.tags

class Post(models.Model):
    title = models.CharField(max_length=1000)
    abstract = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    likes = models.ManyToManyField(User, related_name='blog_post')
    dislikes = models.ManyToManyField(User, related_name='blog_post1')
    saves = models.ManyToManyField(User, related_name='blog_post2')
    primary_tag = models.ForeignKey(Tag, default=23 ,on_delete=models.CASCADE)
    secondary_tags= models.ManyToManyField(Tag, related_name='secondary_tag')
    identifier = models.URLField(default="")
    version = models.IntegerField(default=1)
    publisher = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def total_saves(self):
        return self.saves.count()

    def get_year(self):
        return self.publication_date.year

    def get_ordinal(self):
        n = self.version
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        return str(n) + suffix

class Comment(models.Model):
    post1 = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True)
    likes = models.ManyToManyField(User, blank=True, symmetrical=False, related_name='comment-likes+')
    dislikes = models.ManyToManyField(User, blank=True, symmetrical=False, related_name='comment-dislikes+')


    def __str__(self):
        return self.post1.title

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    

class MessageModel(models.Model):
    thread = models.ForeignKey('Thread', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)





