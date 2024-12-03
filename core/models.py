from django.db import models
from django.conf import settings

class Post(models.Model):
    written_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        on_delete = models.DO_NOTHING,
        blank=True
        )
    written_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
        )
    written_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.CASCADE
        )
    def __str__(self):
        return f"Comment by {self.written_by.username} on {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name