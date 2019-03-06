from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=64, default=None, unique=True, help_text="Must be Unique")
    text = models.TextField(max_length=200)
    create_time = models.DateTimeField(default=timezone.now())
    update_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=True)
    class Meta:
        ordering = ('-create_time',)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f'/{self.id}/detail'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    # objects = models.Manager()  # The default manager.
    # published = PublishedManager()  # Our custom manager.

# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,self).get_queryset().filter(status='published')