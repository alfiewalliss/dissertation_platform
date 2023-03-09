from django.contrib import admin
from .models import Post, Comment, Tag, Thread, Notification

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Thread)
admin.site.register(Notification)
