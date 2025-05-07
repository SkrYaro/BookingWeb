from django.shortcuts import render

from booking.models import Post


# Create your views here.

def look_main(request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request, "main.html", context=context)

def look_users(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request, "users.html", conects=context)