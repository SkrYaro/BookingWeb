from django.contrib import admin

from booking.models import Post, Book, Profile

# Register your models here.

admin.site.register(Post)

admin.site.register(Book)

admin.site.register(Profile)
