from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jm

# Create your models here.

class User(AbstractUser):

    birthday = jm.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(max_length=250,blank=True,null=True,verbose_name="بیوگرافی")
    phone = models.CharField(max_length=11,blank=True,null=True,verbose_name="شماره تلفن")
    photo = models.ImageField(upload_to="profile_images",verbose_name="تصویر",blank=True,null=True)


