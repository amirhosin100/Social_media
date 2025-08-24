from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from taggit.admin import TaggedItemInline,TagAdmin
from taggit.models import Tag

# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class ImagePostInline(admin.StackedInline):
    model = ImagePost
    extra = 0

@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('موارد دیگر' ,{
            "fields":('bio','phone','photo',"birthday")
        }),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["author","description","create","status"]
    list_editable = ["status"]
    ordering = ["-create"]
    inlines = [ImagePostInline,CommentInline]

@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author","message","create"]

