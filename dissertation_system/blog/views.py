from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Thread, MessageModel, Tag
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
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from users.models import Profile
from django.db.models import Q
from django.contrib import messages
from dal import autocomplete


# Create your views here.
def home(request):
    context = {"posts": Post.objects.all}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


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
        messages.success(self.request, "Post successfully uploaded")
        return super(PostCreateView, self).form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse("blog-detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        form.instance.username_id = self.request.user.id
        form.instance.post1_id = self.kwargs["pk"]
        return super(CommentCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
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
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))

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
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
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
        else:
            receiver = thread.receiver
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get("message"),
        )
        message.save()
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

    def get(self, request, *args, **kwargs):
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


def tag_follow(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    if tag.followers.filter(id=request.user.id).exists():
        tag.followers.remove(request.user)
    else:
        tag.followers.add(request.user)
    return HttpResponseRedirect(reverse("tag-list", args=[str(pk)]))

def tag_info(request):
    return render(request, "blog/tag_info.html")


def promote(request, pk):
    if request.user.profile.admin != 0:
        user1 = get_object_or_404(Profile, id=pk)
        user1.admin = 1
        user1.save()
    return HttpResponseRedirect(reverse("user-posts", args=[user1.user.username]))
    
    