from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .models import Post, PostComment, Report,Category
from .forms import NewCommentForm, NewReportForm
import operator
from django.db.models import Count, F, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.http import HttpResponse
from notifications.signals import notify
from taggit.models import Tag
import datetime
from users.models import Profile

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'tags','category']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

# @login_required
# def Create_Post(request):
# 	if request.method == 'POST':
		




class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5
	
	

	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		
		user = self.request.user
		print(user)
		context['announcments'] = Post.objects.filter(category__category = 'Announcements')
		if user.is_authenticated:
			categories = user.profile.followed_category.all()
			if len(categories)==0:
				p = Paginator(Post.objects.select_related().all().order_by(
				'-date_posted'), self.paginate_by)	
			else:
				if len(Post.objects.select_related().filter(category__in = categories, is_appropriate = True).order_by('-date_posted')) ==  0:
					p = Paginator(Post.objects.select_related().filter(is_appropriate = True).order_by(
						'-date_posted'), self.paginate_by)
				else:
					p = Paginator(Post.objects.select_related().filter(category__in = categories, is_appropriate = True).order_by(
				'-date_posted'), self.paginate_by)
		else:
			p = Paginator(Post.objects.select_related().all().order_by(
				'-date_posted'), self.paginate_by)
		context['posts'] = p.page(context['page_obj'].number)
		start_date = datetime.datetime.now() - datetime.timedelta(30)
		pos = Post.objects.filter(date_posted__range=(start_date,datetime.datetime.now()))
		top5 = pos.annotate(
				q_count=Count('upvote')).filter(is_appropriate = True).order_by('-q_count')[:5]
		
		le = len(top5)
		
		if le < 5:
			req = 5 - le
			tops = Post.objects.filter(is_appropriate = True).order_by('-upvote')
			top5 = top5 | tops.union(top5)
			

		context['top5'] = top5[:5]
		

		return context

class ExploreListView(ListView):
	model = Post
	template_name = 'blog/explore.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super(ExploreListView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(is_appropriate = True)
		return context
	
	

	def get_context_data(self, **kwargs):
		context = super(ExploreListView, self).get_context_data(**kwargs)
		
		user = self.request.user
		print(user)
		context['announcments'] = Post.objects.filter(category__category = 'Announcements')
		if user.is_authenticated:
				p = Paginator(Post.objects.select_related().all().order_by(
				'-date_posted'), self.paginate_by)	
		
		else:
			p = Paginator(Post.objects.select_related().all().order_by(
				'-date_posted'), self.paginate_by)
		context['posts'] = p.page(context['page_obj'].number)
		
		return context


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'

	paginate_by = 5

	def get_context_data(self, **kwargs):
		user_profile = get_object_or_404(User, username=self.kwargs.get('username'))
		posts =Post.objects.filter(author=user_profile, is_appropriate = True).order_by('-date_posted')
		
		return {'user_profile':user_profile,'posts':posts}


class CategoryPostListView(ListView):
	model = Post
	template_name = 'blog/category.html'
	context_object_name = 'posts'
	paginate_by = 5
	

	def get_context_data(self, **kwargs):
		context = super(CategoryPostListView, self).get_context_data(**kwargs)
		category = self.kwargs.get('category')
		cat = Category.objects.filter(category = category)[0]
		user = self.request.user.profile
		
		context['num_of_post'] = cat.num_of_posts
		if user.followed_category.filter(category = category).exists():
			context['follow_status'] = True
		else:
			context['follow_status'] = False

		posts = Post.objects.filter(category__category = category, is_appropriate = True).order_by('-date_posted')
		paginator = Paginator(posts, 5) # Show 25 contacts per page.

		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)

	

		context['page_obj'] = page_obj
		
		return context




class TagsPostListView(ListView):
	model = Post
	template_name = 'blog/post_tags.html'
	context_object_name = 'posts'
	paginate_by = 5

	

	def get_context_data(self, **kwargs):
		context = super(TagsPostListView, self).get_context_data(**kwargs)
		post_tag = self.kwargs.get('post_tags')
		context['post_tags']  =  post_tag
		posts= Post.objects.filter(tags__name=post_tag,is_appropriate = True).order_by('-date_posted')
		context['num_of_post'] = len(posts)
		paginator = Paginator(posts, 5) # Show 25 contacts per page.

		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)

	

		context['page_obj'] = page_obj
		return context



class BookmarkView(ListView):
	model = Post
	template_name = 'blog/bookmark.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		return (Post.objects.filter(bookmark=self.request.user, is_appropriate = True))



def Upvote_ajax(request):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	post_id = post.id
	up_status = ''
	if post.upvote.filter(id=request.user.id).exists():
		post.upvote.remove(request.user)
		up_status = 'disliked'
	else:
		if post.downvote.filter(id=request.user.id).exists():
			post.downvote.remove(request.user)
			post.upvote.add(request.user)
			sender = User.objects.get(id=request.user.id)
			recipient = User.objects.get(id=post.author.id)
			if sender != recipient:
				message = f'liked your '
				notify.send(sender=sender, recipient=recipient, verb='Post',
				description=message, target = post)
			up_status = 'liked'
		else:
			post.upvote.add(request.user)
			sender = User.objects.get(id=request.user.id)
			recipient = User.objects.get(id=post.author.id)
			if sender != recipient:
				message = f'liked your '
				notify.send(sender=sender, recipient=recipient, verb='Post',
				description=message, target = post)
			up_status = 'liked'
	up_count = post.number_of_upvotes()
	down_count = post.number_of_downvotes()
	ctx = {'up_status':up_status,'up_count':up_count,'down_count':down_count}
	return HttpResponse(json.dumps(ctx), content_type='application/json')

def Downvote_ajax(request):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	down_status = ''
	if post.downvote.filter(id=request.user.id).exists():
		post.downvote.remove(request.user)
		down_status = 'disliked'
	else:
		if post.upvote.filter(id=request.user.id).exists():
			post.upvote.remove(request.user)
			post.downvote.add(request.user)
			down_status = 'liked'
		else:
			post.downvote.add(request.user)
			down_status = 'liked'

	up_count = post.number_of_upvotes()
	down_count = post.number_of_downvotes()
	ctx = {'down_status':down_status,'up_count':up_count,'down_count':down_count}
	return HttpResponse(json.dumps(ctx), content_type='application/json')



def Bookmark_ajax(request):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	status = ''
	if post.bookmark.filter(id=request.user.id).exists():
		post.bookmark.remove(request.user)
		status = False
	else:
		post.bookmark.add(request.user)
		status = True
	ctx = {'status':status}
	return HttpResponse(json.dumps(ctx), content_type='application/json')

def Category_Ajax(request):
	print(request.POST.get('category'))
	category = get_object_or_404(Category, category=request.POST.get('category'))
	user = request.user.profile
	status = ''
	if user.followed_category.filter(category = category).exists():
		user.followed_category.remove(category)
		status = False
	else:
		user.followed_category.add(category)
		status = True
	user.save()
	ctx = {'status':status}
	return HttpResponse(json.dumps(ctx), content_type='application/json')



def Upvote_Comment_Ajax(request):
	comment = get_object_or_404(PostComment, id=request.POST.get('comment_id'))
	up_status = ''
	if comment.upvote_comment.filter(id=request.user.id).exists():
		comment.upvote_comment.remove(request.user)
		up_status = 'disliked'
	else:
		if comment.downvote_comment.filter(id=request.user.id).exists():
			comment.downvote_comment.remove(request.user)
			comment.upvote_comment.add(request.user)
			up_status = 'liked'
			comment.upvote_comment.add(request.user)
			sender = User.objects.get(id=request.user.id)
			recipient = User.objects.get(id=comment.author.id)
			if sender != recipient:
				message = f'liked your '
				notify.send(sender=sender, recipient=recipient, verb='Comment',
				description=message, target = comment.post_connected)
		else:
			comment.upvote_comment.add(request.user)
			sender = User.objects.get(id=request.user.id)
			recipient = User.objects.get(id=comment.author.id)
			if sender != recipient:
				message = f'liked your '
				notify.send(sender=sender, recipient=recipient, verb='Comment',
				description=message, target = comment.post_connected)
			up_status = 'liked'
	count_upvotes = comment.number_of_upvotes_comment()
	count_downvotes = comment.number_of_downvotes_comment()
	ctx = {'up_status':up_status,'up_count':count_upvotes,'down_count':count_downvotes,'id':request.POST.get('comment_id')}
	return HttpResponse(json.dumps(ctx), content_type='application/json')

def Downvote_Comment_Ajax(request):
	comment = get_object_or_404(PostComment, id=request.POST.get('comment_id'))
	down_status = ''
	if comment.downvote_comment.filter(id=request.user.id).exists():
		comment.downvote_comment.remove(request.user)
		down_status = 'disliked'
	else:
		if comment.upvote_comment.filter(id=request.user.id).exists():
			comment.upvote_comment.remove(request.user)
			comment.downvote_comment.add(request.user)
			down_status = 'liked'
		else:
			comment.downvote_comment.add(request.user)
			down_status = 'liked'
	count_upvotes = comment.number_of_upvotes_comment()
	count_downvotes = comment.number_of_downvotes_comment()
	ctx = {'down_status':down_status,'up_count':count_upvotes,'down_count':count_downvotes,'id':request.POST.get('comment_id')}
	return HttpResponse(json.dumps(ctx), content_type='application/json')



def Comment_Ajax(request):
	comment_text = request.POST.get('the_comment')
	post_connected = get_object_or_404(Post, slug = request.POST.get('object'))
	response_data = {}
	comment = PostComment(comment=comment_text, author= request.user, post_connected=post_connected)
	comment.save()
	sender = User.objects.get(id=request.user.id)
	recipient = User.objects.get(id=post_connected.author.id)
	if sender != recipient:
		message = f'commented on your  '
		notify.send(sender=sender, recipient=recipient, verb='Post',
		description=message, target = post_connected)
	response_data['result'] = 'Create post successful!'
	
	comments_connected = PostComment.objects.filter(
		post_connected=post_connected).order_by('-date_posted')
	data={}	
	comment_new = []
	for c in comments_connected:
		upvoted_comment = False
		downvoted_comment = False
		if c.upvote_comment.filter(id=request.user.id).exists():
			upvoted_comment = True
		if c.downvote_comment.filter(id=request.user.id).exists():
			downvoted_comment = True
		comment_new.append([c.id, upvoted_comment, downvoted_comment])
	data['object']=post_connected
	data['comments'] = comments_connected
	data['comment_status'] = comment_new
	
	return render(request, 'blog/comments.html', data)



class PostDetailView(DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		post_connected = get_object_or_404(Post, slug=self.kwargs['slug'])
		
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
		data['post_connect'] = self.kwargs['slug']

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
		sender = User.objects.get(id=request.user.id)
		recipient = User.objects.get(id=self.get_object().author.id)
		if sender != recipient:
			message = f'commented on your  '
			notify.send(sender=sender, recipient=recipient, verb='Post',
			description=message, target = self.get_object())
		new_comment.save()
		return self.get(self, request, *args, **kwargs)

	


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'category','tags']

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
			Q(category__icontains=query) |
			Q(content__icontains=query) |
			Q(tags__name__icontains=query))
		return posts


def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})


def Report_Form(request, slug):
	print("ehehe")
	post_connected=Post.objects.get(slug=slug)
	if Report.objects.filter(post_connected = post_connected).exists():
		report = Report.objects.filter(post_connected = post_connected)[0]
		if Report.objects.filter(reporter = request.user).exists():
			pass
		else:
			report.reporter.add(request.user)
			report.count += 1
			report.save()
	else:
		report = Report(post_connected=post_connected)
		
		report.save()
		report.reporter.add(request.user)
	# return render(request ,'')
	return redirect('post-detail',slug)

def autocompleteModel(request):
	if request.is_ajax():
		q = request.GET.get('term', '').capitalize()
		search_tags  = Tag.objects.filter(name__contains = q)
		results = []
		
		for r in search_tags:
			data = {}
			data['label']= r.name
			results.append(data)


		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def search_autocompleteModel(request):
	if request.is_ajax():
		q = request.GET.get('term', '').capitalize()
		search_tags  = Tag.objects.filter(name__contains = q)
		search_user  = User.objects.filter(username__contains = q)
		search_post  = Post.objects.filter(title__contains = q) | Post.objects.filter(category__category__contains = q) | Post.objects.filter(content__contains = q)
		search_category  = Category.objects.filter(category__contains = q)
		results = []
		

		for r in search_tags:
			data = {}
			data['label']= r.name
			data['url']= "post/tags/"+r.name
			results.append(data)

		for r in search_user:
			data = {}
			data['label']= r.username
			data['url']= "user/"+r.username
			results.append(data)

		for r in search_post:
			data = {}
			data['label']= r.title
			data['url']= "post/detail/"+r.slug
			results.append(data)

		for r in search_category:
			data = {}
			data['label']= r.category
			data['url']= "post/category/"+r.category
			results.append(data)

		if len(search_tags)==0 and len(search_user)==0 and len(search_category)==0 and len(search_post)==0:
			data = {}
			data['label']= "No search available"
			data['url']= ''
			results.append(data)

		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
