from django.shortcuts import render

from booking.models import Post


# Create your views here.

def look_main(request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request, "main.html", context=context)
