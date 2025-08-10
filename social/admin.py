from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["user","birthday"]

@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('موارد دیگر' ,{
            "fields":('bio','phone','photo')
        }),
    )
    inlines = [AccountInline]
