from django.shortcuts import render,redirect
from .forms import *
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.generic import ListView,DetailView
from .models import *
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .templatetags.tags import to_persian_numbers
# Create your views here.

def main(request):
    return render(request,"social/main_page.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd["password"])
            user.save()
            login(request, user,"django.contrib.auth.backends.ModelBackend")
            return redirect("social:main")
    else:
        form = RegisterForm()

    context = {
        "form":form,
    }
    return render(request,"registration/register.html",context)

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            context = {
                "subject": cd["subject"],
                "first_name": cd["first_name"],
                "last_name": cd["last_name"],
                "email": cd["email"],
                "message": cd["message"],
            }
            message = render_to_string("email/send_ticket.html",context)
            email = EmailMessage(cd["subject"],message,"computer.super111@gmail.com",["amirhosinmirjamali123@gmail.com"])
            email.content_subtype = "html"
            email.send()
    else:
        form = TicketForm()

    context = {
        "form":form,
    }
    return render(request,"forms/ticket.html",context)

class MyConfirm(PasswordResetConfirmView):

    def form_valid(self, form):
        responese = super().form_valid(form)
        user = form.save()
        login(self.request,user,"django.contrib.auth.backends.ModelBackend")
        return  responese


class PostListView(ListView):

    template_name = "social/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag = self.request.GET.get("tag",None)
        query = Post.publish.all()
        if tag :
            tag = get_object_or_404(Tag,slug=tag)
            query = query.filter(tags__in=[tag])
        return query
    def get_context_data(self, *args,**kwargs):
        tag = self.request.GET.get("tag", None)
        if tag:
            tag = get_object_or_404(Tag,slug=tag)
        context = super().get_context_data(**kwargs)
        context["tag"] = tag
        return context


class PostDetail(DetailView):
    context_object_name = "post"
    queryset = Post.publish.all()
    template_name = "social/post_detail.html"

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post,id=self.kwargs.get("pk"))
        tags_id = post.tags.values_list("id",flat=True)
        similar_post = Post.objects.filter(tags__in=tags_id).exclude(id=post.id)
        similar_post = similar_post.annotate(same_tags=Count("tags")).order_by("same_tags")

        context = super().get_context_data(**kwargs)
        context["similar"] : similar_post
        return context

@login_required
def create_post(request):
    images = []
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for image in request.FILES.getlist("images"):
                ImagePost.objects.create(post=post,image=image)
            form.save_m2m()
            description = form.cleaned_data["description"][:20]
            message = f"پست ({description}) با موفقیت ایجاد شد"
            messages.success(request,message)
            return redirect("social:main")
        else:
            images = request.FILES.getlist("images")
    else:
        form = PostForm()

    context = {
        "form":form,
        "images":images,
    }
    return render(request,"social/create_post.html",context)

def search_post(request):
    query = request.GET.get("query",'')
    result = []
    if query :
        result = Post.publish.annotate(similarity=TrigramSimilarity("description",query))
        result = result.filter(similarity__gt=0.1).order_by("-similarity")
    context = {
        "result":result,
    }
    return render(request,"social/search.html",context)

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get("post_id")
    if post_id is not None :
        post = Post.publish.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            like = False
        else:
            post.likes.add(user)
            like = True
        post_like_count = to_persian_numbers(post.likes.count())
        response_data = {
            "like":like,
            "like_count":post_like_count,
        }

    else:
        response_data = {
            "Error":"InValid Post ID",
        }
    return JsonResponse(response_data)