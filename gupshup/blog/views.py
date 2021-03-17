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
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content','category']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts' 
	ordering = ['-date_posted']
	paginate_by = 5

	

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
		# category = get_object_or_404(Post, category=self.kwargs.get('category'))
		return Post.objects.filter(category=category).order_by('-date_posted')




def PostLike(request, pk):
	post = get_object_or_404(Post, id = request.POST.get('post_id'))
	if post.likes.filter(id = request.user.id).exists():
		post.likes.remove(request.user)
	else:
		post.likes.add(request.user)

	return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))


class PostDetailView(DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)

		likes_connected = get_object_or_404(Post, id = self.kwargs['pk'])
		liked = False
		if likes_connected.likes.filter(id = self.request.user.id).exists():
			liked = True
		data['number_of_likes'] = likes_connected.number_of_likes()
		data['post_is_likes'] = liked


		comments_connected = PostComment.objects.filter(post_connected = self.get_object()).order_by('-date_posted')
		data['comments'] = comments_connected
		if self.request.user.is_authenticated:
			data['comment_form'] = NewCommentForm(instance = self.request.user)

		return data

	def post(self, request, *args, **kwargs):
		new_comment = PostComment(content = request.POST.get('content'), author = self.request.user, post_connected = self.get_object())
		new_comment.save()
		return self.get(self, request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content','category']

	def form_valid(self,form):
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
						Q(title__icontains = query) |
						Q(content__icontains = query))
		return posts


def about(request):
	return render(request, 'blog/about.html', {'title' : 'About'})
