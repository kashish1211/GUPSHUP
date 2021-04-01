from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .models import Post, PostComment
from .forms import NewCommentForm
import operator
from django.db.models import Count, F, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        top3 = Post.objects.annotate(
            q_count=Count('upvote')).order_by('-q_count')[:5]
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['tops'] = top3
        context['announcments'] = Post.objects.filter(category='Announcments')
        p = Paginator(Post.objects.select_related().all().order_by(
            '-date_posted'), self.paginate_by)
        context['posts'] = p.page(context['page_obj'].number)
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'

    paginate_by = 5

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Post.objects.filter(category=category).order_by('-date_posted')


class BookmarkView(ListView):
    model = Post
    template_name = 'blog/bookmark.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return (Post.objects.filter(bookmark=self.request.user))


def Upvote(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.upvote.filter(id=request.user.id).exists():
        post.upvote.remove(request.user)

    else:
        if post.downvote.filter(id=request.user.id).exists():
            post.downvote.remove(request.user)
            post.upvote.add(request.user)
        else:
            post.upvote.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def Bookmark(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmark.filter(id=request.user.id).exists():
        post.bookmark.remove(request.user)
    else:
        post.bookmark.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def Downvote(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.downvote.filter(id=request.user.id).exists():
        post.downvote.remove(request.user)
    else:
        if post.upvote.filter(id=request.user.id).exists():
            post.upvote.remove(request.user)
            post.downvote.add(request.user)
        else:
            post.downvote.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def Downvote_comment(request, pk, pck):
    comment = get_object_or_404(PostComment, id=request.POST.get('comment_id'))
    if comment.downvote_comment.filter(id=request.user.id).exists():
        comment.downvote_comment.remove(request.user)
    else:
        if comment.upvote_comment.filter(id=request.user.id).exists():
            comment.upvote_comment.remove(request.user)
            comment.downvote_comment.add(request.user)
        else:
            comment.downvote_comment.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def Upvote_comment(request, pk, pck):
    comment = get_object_or_404(PostComment, id=request.POST.get('comment_id'))
    if comment.upvote_comment.filter(id=request.user.id).exists():
        comment.upvote_comment.remove(request.user)
    else:
        if comment.downvote_comment.filter(id=request.user.id).exists():
            comment.downvote_comment.remove(request.user)
            comment.upvote_comment.add(request.user)
        else:
            comment.upvote_comment.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post_connected = get_object_or_404(Post, id=self.kwargs['pk'])

        upvoted = False
        downvoted = False
        bookmarked = False
        if post_connected.upvote.filter(id=self.request.user.id).exists():

            upvoted = True
        if post_connected.downvote.filter(id=self.request.user.id).exists():

            downvoted = True
        if post_connected.bookmark.filter(id=self.request.user.id).exists():
            bookmarked = True
        data['number_of_upvotes'] = post_connected.number_of_upvotes()
        data['number_of_downvotes'] = post_connected.number_of_downvotes()
        data['post_is_upvoted'] = upvoted
        data['post_is_downvoted'] = downvoted
        data['post_is_bookmarked'] = bookmarked

        comments_connected = PostComment.objects.filter(
            post_connected=self.get_object()).order_by('-date_posted')

        comment_new = []
        for c in comments_connected:
            upvoted_comment = False
            downvoted_comment = False
            if c.upvote_comment.filter(id=self.request.user.id).exists():
                upvoted_comment = True
            if c.downvote_comment.filter(id=self.request.user.id).exists():
                downvoted_comment = True
            comment_new.append([c.id, upvoted_comment, downvoted_comment])

        data['comments'] = comments_connected
        data['comment_status'] = comment_new

        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = PostComment(comment=request.POST.get(
            'comment'), author=self.request.user, post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    success_url = '/'


class SearchResultView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/search_result.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query))
        return posts


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
