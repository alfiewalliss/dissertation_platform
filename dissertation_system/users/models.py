from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from blog.models import Tag

#User._meta.get_field('email')._unique = True

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    followers = models.ManyToManyField('self',blank=True, symmetrical=False, related_name='user_followers')
    following = models.ManyToManyField('self',blank=True, symmetrical=False, related_name='user_following')
    bio = models.TextField(max_length=1000)
    admin = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, symmetrical=False, related_name='user_tags')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




