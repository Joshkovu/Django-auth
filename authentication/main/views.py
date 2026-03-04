from django.shortcuts import redirect, render
from .forms import CommentForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout, authenticate
# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, "main/home.html")

@login_required(login_url="/login")
def create_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment =form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("/home")
    else:
        form = CommentForm()
    return render(request, "main/create_comment.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {"form": form})