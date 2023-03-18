from .models import Tag, Post, Comment, Notification
from datetime import datetime
def tag_renderer(request):
    return {
        "tags_context": Tag.objects.all(), 
        "posts_context": Post.objects.all(), 
        "comment_context": Comment.objects.all()}

def notification_renderer(request):
    notification_processor = []
    counter = 0
    if request.user.is_authenticated:
        counter = len(Notification.objects.filter(new = 0).filter(receiver = request.user))
        notification_processor = (Notification.objects.filter(receiver = request.user).order_by("new"))
    return {
        "notification_processor": notification_processor,
        "counter": counter
    }

def get_current_path(request):
    return {
       'date': datetime.now()
     }