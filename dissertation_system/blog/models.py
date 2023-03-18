from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime 
import base64

# Create your models here.
class Tag(models.Model):
    tags = models.CharField(max_length=1000,unique=True)
    followers = models.ManyToManyField(User, related_name='tag_followers')
    
    def __str__(self):
        return self.tags

class Post(models.Model):
    title = models.CharField(max_length=1000)
    abstract = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents')
    likes = models.ManyToManyField(User, related_name='blog_post')
    dislikes = models.ManyToManyField(User, related_name='blog_post1')
    saves = models.ManyToManyField(User, related_name='blog_post2')
    primary_tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    secondary_tags= models.ManyToManyField(Tag, related_name='secondary_tag', blank=True)
    identifier = models.URLField(default="")
    version = models.IntegerField(default=1)
    publisher = models.CharField(max_length=1000, default='')
    reviewed = models.IntegerField(default = 0)
    requested = models.CharField(max_length=30, default="none")
    reviewers = models.ManyToManyField(User, related_name="reviewers")
    requested_time = models.DateTimeField(auto_now_add=True)
    blob_file = models.TextField(db_column='data', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def popularity(self):
        return (self.likes.count())
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def total_saves(self):
        return self.saves.count()

    def get_year(self):
        return self.date_posted.year

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
    new = models.CharField(max_length=30,default="None")
    last_message = models.DateTimeField(auto_now_add=True)
    

class MessageModel(models.Model):
    thread = models.ForeignKey('Thread', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.IntegerField() # 0 = Message, 1 = Peer Review, 2 = Comment, 3=Like, 4=Follow, 5 = Comment Like, 6 = Promotion, 7 Review Complete
    new = models.IntegerField(default=0) # 0 = New, 1 = Read
    heading = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)



