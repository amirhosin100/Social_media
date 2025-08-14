from django.shortcuts import render
from .forms import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
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
            login(request, user)
            return redirect("blog:profile")
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
