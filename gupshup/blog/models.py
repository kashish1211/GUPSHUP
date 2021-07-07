from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

Category_choices = (
    ("Technology", "Technology"),
    ("Mechanical", "Mechanical"),
    ("Electronic", "Electronic"),
    ("Sports", "Sports"),
    ("Business", "Business"),
    ("Announcments", "Announcments"),
    ("Cultural", "Cultural"),
    ("Politics", "Politics"),
    ("Health", "Health"),
    ("Travel", "Travel"),
    ("Fashion", "Fashion"),
    ("Miscellenous", "Miscellenous"),


)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.CharField(
        max_length=20,
        choices=Category_choices,
        default='Miscellenous'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    upvote = models.ManyToManyField(User, related_name='upvote',blank=True)
    downvote = models.ManyToManyField(User, related_name='downvote',blank=True)
    bookmark = models.ManyToManyField(User, related_name='bookmark',blank=True)

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
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.author) + ', ' + self.post_connected.title[:40]
