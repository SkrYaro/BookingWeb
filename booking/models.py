from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    description = models.TextField(null=True)
    add_at = models.DateTimeField(auto_now=True)
    upt_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}({self.owner})"


class Book(models.Model):
    title = models.ForeignKey(Post, related_name='book title', on_delete=models.CASCADE)
    owner = models.ForeignKey(Post, related_name='owner book', on_delete=models.CASCADE)
    customer = models.ForeignKey(Post, related_name='customer', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time_contract = models.DateTimeField(auto_now=True)
