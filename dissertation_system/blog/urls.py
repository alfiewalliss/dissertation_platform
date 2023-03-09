from django.urls import path
from django.urls import re_path as url

from . import views
from .views import (
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    CreateMessage,
    CreateThread,
    ListThreads,
    MessageDeleteView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    TagListView,
    ThreadDeleteView,
    ThreadView,
    UserFeedListView,
    UserPostListView,
    UserSaveListView,
    ReviewDetailView,
    UserReviewListView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="blog-detail"),
    path("post/new/", PostCreateView.as_view(), name="blog-create"),
    path("post/search/<int:order>/", views.post_list, name="blog-search"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="blog-update"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="blog-comment-update"),
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="blog-comment"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="blog-comment-delete"),
    path("post/<int:ppk>/comment/<int:cpk>/like/", views.like_comment, name="blog-comment-like"),
    path("post/<int:ppk>/comment/<int:cpk>/dislike/", views.dislike_comment, name="blog-comment-dislike"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="blog-delete"),
    path("post/<int:pk>/pdf/", views.pdf, name="blog-pdf"),
    path("user/<str:username>/", UserPostListView.as_view(), name="user-posts"),
    path("user/<str:username>/saves/", UserSaveListView.as_view(), name="user-saves"),
    path("post/<int:pk>/like/", views.like, name="blog-like"),
    path("user/<int:pk>/follow/", views.follow, name="user-follow"),
    path("post/<int:pk>/dislike/", views.dislike, name="blog-dislike"),
    path("post/<int:pk>/saves/", views.saves, name="blog-saves"),
    path("inbox/", ListThreads.as_view(), name="inbox"),
    path("inbox/create-thread/", CreateThread.as_view(), name="create-thread"),
    path("inbox/<int:pk>/", ThreadView.as_view(), name="thread"),
    path("inbox/<int:pk>/delete/", ThreadDeleteView.as_view(), name="delete-thread"),
    path("inbox/<int:pk>/create-message/", CreateMessage.as_view(), name="create-message"),
    path("inbox/<int:pk>/delete-message/<int:pk1>/", MessageDeleteView.as_view(), name="delete-message"),
    path("tags/", views.tags_page, name="edit-tags"),
    path("tags/delete/", views.tags_delete, name="tag-delete"),
    path("tags/add/", views.tags_add, name="tag-add"),
    path("tags/<int:pk>/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:pk>/follow/", views.tag_follow, name="tag-follow"),
    path("info/<str:information>/", views.site_info, name='site-info'),
    path("feed/", UserFeedListView.as_view(), name="user-feed"),
    path("reviews/", UserReviewListView.as_view(), name="list-review"),
    path("promote/<int:pk>/", views.promote, name="promote"),
    path("review/<int:pk>/", ReviewDetailView.as_view(), name="review"),
    path("reviewed/<int:pk>", views.review_form, name="review-form"),
    path("review/request/<int:pk>", views.request_review, name="request-review"),
    path('notifications/<int:pk>/update_new/', views.update_notification_new, name='update_notification_new'),
]
