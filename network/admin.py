from django.contrib import admin

from .models import User, Post, Follow, Like, Comment

# Register your models here.

admin.site.site_title = "CS50 Project3 Dashboard"
admin.site.site_header = "CS50 Project4 Dashboard"
admin.site.index_title = "Network Dashboard"


class UserAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_owner', 'post_time',)


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
# admin.site.register(Following)
admin.site.register(Like)
admin.site.register(Comment)
