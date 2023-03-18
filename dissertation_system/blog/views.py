from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Thread, MessageModel, Tag, Notification
from .forms import CommentForm, ThreadForm, MessageForm, PostForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from users.models import Profile
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
import base64


# Create your views here.



class PostListView(ListView):
    def get(self, request):
        posts = Post.objects.all().order_by("-likes")[:6]
        context = {
            "posts": posts
        }
        return render(request, "blog/home.html", context)



class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_post.html"
    context_object_name = "posts"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        context = {
            "form": form,
            "posts": Post.objects.filter(author=user).order_by("-date_posted"),
            "name": self.kwargs.get("username"),
            "user1": user,
        }
        return render(request, "blog/user_post.html", context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get("username")
        try:
            receiver = User.objects.get(username=username)
            if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect("thread", pk=thread.pk)
            elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect("thread", pk=thread.pk)
            if form.is_valid():
                thread = Thread(user=request.user, receiver=receiver)
                thread.save()
                return redirect("thread", pk=thread.pk)
        except:
            return redirect("create-thread")


def post_list(request, order):
    posts_list = Post.objects.all()
    user_list = User.objects.all()
    comment_list = Comment.objects.all()
    tag_list = Tag.objects.all()
    query = request.GET.get("q")
    tab = int(request.GET.get("u"))
    method = order
    if method == 0:
        method1 = "-date_posted"
        method2 = "-date_joined"
        method3 = "-date_added"
    elif method == 1:
        method1 = "date_posted"
        method2 = "date_joined"
        method3 = "date_added"
    elif method == 2:
        method1 = "-likes"
        method2 = "-profile__followers"
        method3 = "-likes"
    elif method == 3:
        method1 = "likes"
        method2 = "profile__followers"
        method3 = "likes"

    if query:
        posts_list = (
            Post.objects.filter(
                Q(title__icontains=query)
                | Q(abstract__icontains=query)
                | Q(author__username__icontains=query)
            )
            .distinct()
            .order_by(method1)[:30]
        )
        user_list = (
            User.objects.filter(Q(username__icontains=query))
            .distinct()
            .order_by(method2)[:30]
        )
        comment_list = (
            Comment.objects.filter(
                Q(username__username__icontains=query) | Q(body__icontains=query)
            )
            .distinct()
            .order_by(method3)[:30]
        )
        tag_list = Tag.objects.filter(Q(tags__icontains=query)).distinct()
    context = {
        "posts": posts_list,
        "users": user_list,
        "comments": comment_list,
        "tags": tag_list,
        "tab": tab,
        "query": query,
    }
    return render(request, "blog/user_search.html", context)


class UserSaveListView(ListView):
    model = Post
    template_name = "blog/user_save.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(saves__username__contains=user).order_by(
            "-date_posted"
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = post.total_likes()
        total_dislikes = post.total_dislikes()
        total_saves = post.total_saves()
        liked = False
        disliked = False
        saved = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if post.dislikes.filter(id=self.request.user.id).exists():
            disliked = True
        if post.saves.filter(id=self.request.user.id).exists():
            saved = True
        temp_list = []
        for i in range(post.comments.all().count()):
            temp_list.append(post.comments.all()[i])

        # Check if user is able to request peer review
        # can_request: 0 = Not author; 1 = request available; 2 = requested
        if self.request.user == post.author: #Check if user owns post
            print("1")
            if post.requested == "requested": # Check if peer review has been requested
                print("2")
                utc=pytz.UTC
                date = datetime.now() - timedelta(days=7)
                if post.requested_time.replace(tzinfo=utc) < date.replace(tzinfo=utc): # Check if it has been requested within the last week
                    print("3")
                    can_request = 1 #Request available
                else:
                    print("4")
                    can_request = 2 #Requested
            else:
                print("5")
                can_request = 1 #Request available
        else: #User doesn't own post
            print("6")
            can_request = 0 # Not author 
        
        context["can_request"] = can_request
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["total_dislikes"] = total_dislikes
        context["disliked"] = disliked
        context["total_saves"] = total_saves
        context["saved"] = saved
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        pdf_file = form.instance.file.open("rb")
        encoded_base64 = base64.b64encode(pdf_file.read())
        encoded_str = encoded_base64.decode('utf-8')
        form.instance.blob_file = encoded_str
        messages.success(self.request, "Post successfully uploaded")
        return super(PostCreateView, self).form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse("blog-detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        author = post.author
        if author != self.request.user:
            noti = Notification(receiver=author, kind=2, heading="New comment on " + post.title, content=("New comment from " + self.request.user.username))
            noti.save()
        form.instance.username_id = self.request.user.id
        form.instance.post1_id = self.kwargs["pk"]
        return super(CommentCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        pdf_file = form.instance.file.open("rb")
        encoded_base64 = base64.b64encode(pdf_file.read())
        encoded_str = encoded_base64.decode('utf-8')
        form.instance.blob_file = encoded_str
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["body"]

    def get_success_url(self):
        return reverse("blog-detail", args=[self.get_object().post1.id])

    def form_valid(self, form):
        form.instance.username_id = self.request.user.id
        form.instance.post_id = self.kwargs["pk"]
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.username:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/delete.html"
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse("user-posts", args=[self.request.user])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/delete_comment.html"
    success_url = "/"

    def get_success_url(self):
        return reverse("blog-detail", args=[self.get_object().post1.id])

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.username:
            return True
        else:
            return False


def pdf(request):
    response = FileResponse(open())


def like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        if post.author != request.user:
            noti = Notification(receiver=post.author, kind=3, heading="New like on " + post.title, content=("New like from " + request.user.username))
            noti.save()
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("blog-detail", args=[str(pk)]))


def follow(request, pk):
    user1 = get_object_or_404(Profile, id=request.POST.get("post_id"))
    if user1 != request.user.profile:
        if request.user.profile.following.filter(id=user1.id).exists():
            request.user.profile.following.remove(user1)
            user1.followers.remove(request.user.profile)
        else:
            request.user.profile.following.add(user1)
            user1.followers.add(request.user.profile)
            if user1.user != request.user:
                noti = Notification(receiver=user1.user, kind=2, heading="New follow", content=("New follow from " + request.user.username))
                noti.save()
    return HttpResponseRedirect(reverse("user-posts", args=[str(user1.user)]))


def dislike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse("blog-detail", args=[str(pk)]))


def saves(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
    else:
        post.saves.add(request.user)
    return HttpResponseRedirect(reverse("blog-detail", args=[str(pk)]))


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user)).order_by("-last_message")
        context = {"threads": threads}

        return render(request, "blog/inbox.html", context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {"form": form}
        return render(request, "blog/create_thread.html", context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get("username")
        try:
            receiver = User.objects.get(username=username)
            if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect("thread", pk=thread.pk)
            elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect("thread", pk=thread.pk)
            if form.is_valid():
                thread = Thread(user=request.user, receiver=receiver)
                thread.save()
                return redirect("thread", pk=thread.pk)
        except:
            return redirect("create-thread")


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = Thread.objects.get(pk=pk)
        if thread.new == "sender" and thread.user == request.user:
            thread.new = "none"
        elif thread.new == "receiver" and thread.receiver == request.user:
            thread.new = "none"
        thread.save()
        message_list = MessageModel.objects.filter(thread__pk__contains=pk).order_by("-date")
        context = {"thread": thread, "form": form, "message_list": message_list}

        return render(request, "blog/thread.html", context)


class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    template_name = "blog/delete_thread.html"
    success_url = "/"

    def get_success_url(self):
        return reverse("inbox")

    def test_func(self):
        thread = self.get_object()
        if self.request.user == thread.user or self.request.user == thread.receiver:
            return True
        else:
            return False


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MessageModel
    success_url = "/"

    def get_success_url(self):
        return reverse("thread", args=[self.kwargs["pk1"]])

    def test_func(self):
        message = self.get_object()
        if self.request.user == message.sender_user:
            return True
        else:
            return False


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = Thread.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
            thread.new = "sender"
            noti = Notification(receiver=thread.sender, kind=0, heading="New message", content=("New message from " + request.user.username))
            noti.save()
            
        else:
            receiver = thread.receiver
            thread.new = "receiver"
            noti = Notification(receiver=thread.receiver, kind=0, heading="New message", content=("New message from " + request.user.username))
            noti.save()
        thread.last_message = datetime.now()
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get("message"),
        )
        message.save()
        thread.save()
        return redirect("thread", pk=pk)


def dislike_comment(request, ppk, cpk):
    comment = get_object_or_404(Comment, id=cpk)
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
    else:
        comment.dislikes.add(request.user)
    return HttpResponseRedirect(reverse("blog-detail", args=[str(ppk)]))


def like_comment(request, ppk, cpk):
    comment = get_object_or_404(Comment, id=cpk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
        if comment.username.user != request.user:
                noti = Notification(receiver=comment.username.user, kind=5, heading="Comment like", content=("New comment like from from " + request.user.username))
                noti.save()
    return HttpResponseRedirect(reverse("blog-detail", args=[str(ppk)]))


def tags_page(request):
    context = {"tags": Tag.objects.all().order_by("tags")}
    return render(request, "blog/tags.html", context)


def tags_delete(request):
    query = request.POST.getlist("select")
    for i in query:
        tag = get_object_or_404(Tag, id=i)
        tag.delete()
    return redirect("edit-tags")


def tags_add(request):
    tag = request.GET.get("new")
    tag = Tag(tags=tag)
    tag.save()
    return redirect("edit-tags")


class TagListView(ListView):
    model = Tag
    template_name = "blog/tag_list.html"
    context_object_name = "tags"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        tag = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        context = {
            "posts": Post.objects.filter(Q(primary_tag=tag) | Q(secondary_tags=tag)).distinct().order_by("-date_posted"),
            "tag": tag,
            "users": Profile.objects.filter(tags=tag).order_by("followers"),
        }
        return render(request, "blog/tag_list.html", context)


class UserFeedListView(ListView):
    model = Post
    template_name = "blog/user_feed.html"
    paginate_by = 5

    def get(self, request):
        users = request.user.profile
        posts = (
            Post.objects.filter(
                Q(author__profile__followers=users) | Q(author=users.user) | Q(primary_tag__followers=users.user) | Q(secondary_tags__followers=users.user)
            )
            .distinct()
            .order_by("-date_posted")[:50]
        )
        context = {"posts": posts}
        return render(request, "blog/user_feed.html", context)

class UserReviewListView(ListView):
    model = Post
    template_name = "blog/user_review.html"
    paginate_by = 5

    def get(self, request):
        users = request.user.profile
        posts = Post.objects.filter(
            Q(reviewers=request.user)
        )
        context = {"posts": posts}
        return render(request, "blog/user_review.html", context)

def tag_follow(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    if tag.followers.filter(id=request.user.id).exists():
        tag.followers.remove(request.user)
    else:
        tag.followers.add(request.user)
    return HttpResponseRedirect(reverse("tag-list", args=[str(pk)]))

def site_info(request, information):
    context = {"information": information}
    return render(request, "blog/site_info.html", context)


def promote(request, pk):
    if request.user.profile.admin != 0:
        user1 = get_object_or_404(Profile, id=pk)
        user1.admin = 1
        user1.save()
        noti = Notification(receiver=user1.user, kind=6, heading="Promotion", content=("Congradulations, you have been promoted to a reviewer by " + request.user.username))
        noti.save()
    return HttpResponseRedirect(reverse("user-posts", args=[user1.user.username]))
    
class ReviewDetailView(DetailView):
    model = Post
    template_name = "blog/review.html"

    def get_context_data(self, **kwargs):
        context = super(ReviewDetailView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = post.total_likes()
        total_dislikes = post.total_dislikes()
        total_saves = post.total_saves()
        liked = False
        disliked = False
        saved = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if post.dislikes.filter(id=self.request.user.id).exists():
            disliked = True
        if post.saves.filter(id=self.request.user.id).exists():
            saved = True
        temp_list = []
        for i in range(post.comments.all().count()):
            temp_list.append(post.comments.all()[i])

        context["total_likes"] = total_likes
        context["liked"] = liked
        context["total_dislikes"] = total_dislikes
        context["disliked"] = disliked
        context["total_saves"] = total_saves
        context["saved"] = saved
        return context

def review_form(request, pk):
    review_user = request.user
    if request.user.profile.admin != 0:
        notes = request.GET.get("notes")
        answer = request.GET.get("pass")
        post = get_object_or_404(Post, id=pk)
        user = post.author
        post.reviewed = answer
        post.requested = "none"
        post.save()
        mail_subject = "Your Peer Review results!"
        message = render_to_string(
            "blog/review_email.html",
            {
                "user": user,
                "review": str(answer),
                "notes": notes,
                "reviewer": review_user,
            },
        )
        message_html = render_to_string(
            "blog/review_email.html",
            {
                "user": user,
                "review": str(answer),
                "notes": notes,
                "reviewer": review_user,
            },
        )
        to_email = user.email
        send_mail(mail_subject, message, "noreply@dissertationexchange.com", [to_email], html_message=message_html)
        if user != request.user:
            noti = Notification(receiver=user, kind=7, heading="Review Complete", content=("Check your email for more details"))
            noti.save()
    return HttpResponseRedirect(reverse("blog-detail", args=[pk]))

def request_review(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.requested = "requested"
    users = Profile.objects.filter(
                Q(admin=1) | Q(admin=0) | Q(tags__tags__icontains=post.primary_tag.tags) | Q(tags__in=post.secondary_tags.all()))# | Q(id!=request.user.profile.id)
            #).order_by("?")
    reviewers = round(len(users) * 0.05) # 5% selection rate 
    if reviewers < 5:
        if len(users) < 5:
            reviewers = len(users)
        else:
            reviewers = 5
    users = users[0:5]
    for i in users:
        post.reviewers.add(i.user)
    post.requested_time = datetime.now()
    post.save()
    
    return HttpResponseRedirect(reverse("blog-detail", args=[pk]))


def update_notification_new(request, pk):
    notification = Notification.objects.get(pk=pk)
    if(notification.new == 1):
        notification.new = 0
        change = 1
    else:
        notification.new = 1
        change = 0
    notification.save()
    return JsonResponse({'success': True, 'change': change})


def delete_notification(request, pk):
    notification = Notification.objects.get(pk=pk)
    if request.user == notification.receiver:
        notification.delete()
    return JsonResponse({'success': True})