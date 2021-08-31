from django.contrib import admin

from clothes.models import Post, Website

# Register your models here.

admin.site.register(Website)
admin.site.register(Post)
