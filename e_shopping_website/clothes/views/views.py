# Create your views here.
from django.shortcuts import render

from clothes.models import Post, Website


def home(request):
    post_list = Post.objects.all()
    website_list = Website.objects.all()
    return render(
        request,
        "home.html",
        {"post_list": post_list, "website_list": website_list},
    )
