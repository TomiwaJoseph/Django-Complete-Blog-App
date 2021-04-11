from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
        unique_for_date='publish')
    category = models.ForeignKey(Category,
        on_delete=models.CASCADE,
        related_name='blog_category')
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='blog_posts')
    body = RichTextUploadingField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
        choices=STATUS_CHOICES,
        default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('index')


def get_default():
    return User.objects.get(id=1)

class Comment(models.Model):
    post = models.ForeignKey(Blog,
        on_delete=models.CASCADE,
        related_name='comments')
    commenter = models.ForeignKey(User,
        default=get_default().id,
        on_delete=models.CASCADE,
        related_name='commenter_comments')
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, related_name='replies',
        on_delete=models.CASCADE, blank=True)
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return 'Reply by Author on {}'.format(self.post)

class NewsLetterList(models.Model):
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.email
