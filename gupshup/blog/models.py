from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from django.db.models import F
from django.utils.text import slugify


class Category(models.Model):
    category = models.CharField(max_length=20) 
    slug = AutoSlugField(populate_from='category')
    num_of_posts = models.IntegerField(default = 0)

    def number_of_posts(self):
        return self.num_of_posts
    
    def __str__(self):
        return self.category[:40]

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_appropriate  = models.BooleanField(default = True)
    notice = models.CharField(max_length=100, default="This Post was DELETED",null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_name')
       
    __original_category = None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    upvote = models.ManyToManyField(User, related_name='upvote',blank=True)
    downvote = models.ManyToManyField(User, related_name='downvote',blank=True)
    bookmark = models.ManyToManyField(User, related_name='bookmark',blank=True)
    tags = TaggableManager()

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.slug:
            self.__original_category = self.category
        

    def save(self, *args, **kwargs):
        if self.__original_category == None:
            self.category.num_of_posts +=1
            self.category.save()
            self.__original_category = self.category
        elif self.category != self.__original_category:
            self.__original_category.num_of_posts -= 1
            self.category.num_of_posts +=1
            self.__original_category.save()
            self.category.save()

        self.__original_category = self.category     
        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
            self.category.num_of_posts -=1
            self.category.save()     
            super(Post, self).save(*args, **kwargs)

    def number_of_downvotes(self):
        return self.downvote.count()

    def number_of_upvotes(self):
        return self.upvote.count()

    @property
    def number_of_comments(self):
        return PostComment.objects.filter(post_connected=self).count()
    


class PostComment(models.Model):
    post_connected = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    upvote_comment = models.ManyToManyField(User, related_name='upvote_comment',blank=True)
    downvote_comment = models.ManyToManyField(User, related_name='downvote_comment',blank=True)


    

    def number_of_downvotes_comment(self):
        return self.downvote_comment.count()

    def number_of_upvotes_comment(self):
        return self.upvote_comment.count()
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.author) + ', ' + self.post_connected.title[:40]

    



class Report(models.Model):
    post_connected = models.ForeignKey(Post, related_name='report', on_delete=models.CASCADE)
    reporter = models.ManyToManyField(User, related_name='reporter',blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    status  = models.BooleanField(default = False)
    count = models.IntegerField(default = 1)
    

    def number_of_counts(self):
        return self.count()
    
    def __str__(self):
        return self.post_connected.title[:40]


