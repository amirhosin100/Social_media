from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jm
from django.dispatch import receiver
from django.db.models.signals import pre_save
from taggit.models import Tag
from unidecode import unidecode
from taggit.managers import TaggableManager
from django.utils.text import slugify

# Create your models here.
class PUBLISH(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class User(AbstractUser):

    birthday = jm.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(max_length=250,blank=True,null=True,verbose_name="بیوگرافی")
    phone = models.CharField(max_length=11,blank=True,null=True,verbose_name="شماره تلفن")
    photo = models.ImageField(upload_to="profile_images",verbose_name="تصویر",blank=True,null=True)



class Post(models.Model):

    class Status(models.TextChoices):
        REJECTED = "RJ","رد شده"
        PUBLISHED = "PB","منتشر شده"

    description = models.TextField(verbose_name="توضیحات")
    author = models.ForeignKey(User,models.CASCADE,related_name="posts",verbose_name="نویسنده")

    create = jm.jDateTimeField(auto_now_add=True)
    update = jm.jDateTimeField(auto_now=True)
    status = models.CharField(choices=Status.choices,verbose_name="وضعیت",default=Status.PUBLISHED)
    tags = TaggableManager()

    objects = jm.jManager()
    publish = PUBLISH()

    class Meta:
        ordering = [
            "-create"
        ]
        indexes = [
            models.Index(fields=[
                "-create"
            ])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name}"

@receiver(pre_save,sender=Tag)
def create_slug_for_tag(sender, instance, **kwargs):
    #Convert Persian name to Latin and create slug
    latin_name = unidecode(instance.name)
    instance.slug = slugify(latin_name)