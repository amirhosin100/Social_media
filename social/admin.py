from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from taggit.admin import TaggedItemInline,TagAdmin
from taggit.models import Tag
# Register your models here.


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('موارد دیگر' ,{
            "fields":('bio','phone','photo',"birthday")
        }),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["author","create","status"]
    list_editable = ["status"]
    ordering = ["-create"]

# edit tag
