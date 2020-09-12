from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Post(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text_field = models.TextField(max_length=9999)
    post_time = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.text_field

    class Meta:
        ordering = ['-post_time']


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_following = models.ManyToManyField(
        User, related_name='followings', blank=True)
    user_follower = models.ManyToManyField(
        User, related_name='followers', blank=True)

    def __str__(self):
        return str(self.user)


class Like(models.Model):
    liked_by = models.ManyToManyField(User, blank=True)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.liked_post.text_field)


class Comment(models.Model):
    post_comment = models.CharField(max_length=999, blank=True)
    of_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_comment

    def serialize(self):
        return {
            "id": self.id,
            "post_comment": self.post_comment,
            "of_post": self.of_post,
            "comment_user": self.comment_user,
            "comment_time": self.comment_time
        }
