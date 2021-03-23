from django.urls import path
from django.http import HttpResponseRedirect, request
from .views import PostDetailView, PostUpdateView, PostDeleteView, UserPostListView, SearchResultView, CategoryPostListView, PostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<str:category>', CategoryPostListView.as_view(), name='category'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post-upvote/<int:pk>/', views.Upvote, name='post-upvote'),
    path('post-downvote/<int:pk>/', views.Downvote, name='post-downvote'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/search/', SearchResultView.as_view(), name='search-result'),
    path('about/', views.about, name='blog-about'),
]