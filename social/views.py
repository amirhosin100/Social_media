from django.shortcuts import render
from .forms import *
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.generic import ListView,DetailView
from .models import *
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

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
