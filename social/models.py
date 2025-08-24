import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jm
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_delete
from taggit.models import Tag
from unidecode import unidecode
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.urls import reverse

# Create your models here.
class PUBLISH(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class User(AbstractUser):

    birthday = jm.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(max_length=250,blank=True,null=True,verbose_name="بیوگرافی")
    phone = models.CharField(max_length=11,blank=True,null=True,verbose_name="شماره تلفن")
    photo = ResizedImageField(upload_to="profile_images/%Y/%m",verbose_name="تصویر",blank=True,null=True,
                              size=[500,500],crop=["middle","center"],quality=70)


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
    likes = models.ManyToManyField(User,related_name="liked_posts",blank=True,verbose_name="لایک ها")

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
        return self.description[:20]

    def get_absolute_url(self):
        return reverse("social:detail",args=[self.id])

class ImagePost(models.Model):
    post = models.ForeignKey(Post,models.CASCADE,related_name="images",verbose_name="پست")
    image = ResizedImageField(upload_to="post_images/%Y/%m/%d",size=[600,750],crop=["middle","center"],quality=100,verbose_name="تصویر")
    title = models.CharField(max_length=250,verbose_name="عنوان تصویر",blank=True,null=True)

    class Meta:
        verbose_name = "تصویر پست"
        verbose_name_plural = "تصویر پست ها"

    def __str__(self):
        name = os.path.basename(self.image.name)
        return self.title if self.title else name[:20]

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments",verbose_name="پست",on_delete=models.CASCADE)
    author = models.ForeignKey(User,models.CASCADE,"comments",default=1,verbose_name="نویسنده")
    message = models.TextField(max_length=1000,verbose_name="پیام")
    create = jm.jDateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد")
    update = jm.jDateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,"liked_comments",verbose_name="کاربرانی که لایک کرده اند",blank=True)
    dislikes = models.ManyToManyField(User,"disliked_comments",verbose_name="کاربرانی که دیس لایک کرده اند",blank=True)

    class Meta :
        ordering = [
            "-create"
        ]
        indexes = [
            models.Index(fields=[
                "-create"
            ])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return self.message[:20]


@receiver(pre_save,sender=Tag)
def create_slug_for_tag(sender, instance, **kwargs):
    #Convert Persian name to Latin and create slug
    latin_name = unidecode(instance.name)
    instance.slug = slugify(latin_name)

@receiver(post_delete,sender=ImagePost)
def delete_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)