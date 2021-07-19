from django.urls import path
from django.http import HttpResponseRedirect, request
from .views import PostDetailView, PostUpdateView, PostDeleteView, UserPostListView, SearchResultView, CategoryPostListView, PostListView, TagsPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/tags/<str:post_tags>', TagsPostListView.as_view(), name='post-tags'),
    path('post/category/<str:category>', CategoryPostListView.as_view(), name='category'),
    path('post-upvote-ajax/', views.Upvote_ajax, name='post-upvote-ajax'),
    path('post-downvote-ajax/', views.Downvote_ajax, name='post-downvote-ajax'),
    path('post-bookmark-ajax/', views.Bookmark_ajax, name='post-bookmark-ajax'),
    path('comment-upvote-ajax/', views.Upvote_Comment_Ajax, name='comment-upvote-ajax'),
    path('comment-downvote-ajax/', views.Downvote_Comment_Ajax, name='comment-downvote-ajax'),
    path('comment-ajax/', views.Comment_Ajax, name='comment-ajax'),
    path('post/bookmark/', views.BookmarkView.as_view(), name='bookmark-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/report', views.Report_Form, name='post-report'),
    path('post/search/', SearchResultView.as_view(), name='search-result'),
    path('about/', views.about, name='about'),
    path('autocomplete/', views.autocompleteModel, name='tags-auto'),
]
