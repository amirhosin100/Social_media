from django.shortcuts import render
from .forms import *

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
            AccountModel.objects.create(user=user)
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
            for i in form.cleaned_data:
                print(form.cleaned_data[i])
    else:
        form = TicketForm()

    context = {
        "form":form,
    }
    return render(request,"forms/ticket.html",context)
