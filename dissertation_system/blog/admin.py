from django.contrib import admin
from .models import Post, Comment, Tag, Thread, Notification
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class TagResource(resources.ModelResource):
   class Meta:
      model = Tag
class TagAdmin(ImportExportModelAdmin):
   resource_class = TagResource
admin.site.register(Tag,TagAdmin)
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Thread)
admin.site.register(Notification)

