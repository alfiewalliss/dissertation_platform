from .models import Tag, Post, Comment
def tag_renderer(request):
    return {
        "tags_context": Tag.objects.all(), 
        "posts_context": Post.objects.all(), 
        "comment_context": Comment.objects.all()}