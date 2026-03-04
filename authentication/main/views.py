from django.shortcuts import redirect, render
from .forms import CommentForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout, authenticate
from .models import Comment
# Create your views here.
@login_required(login_url="/login")
def home(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        comment = Comment.objects.filter(id=comment_id, user=request.user).first()
        if comment and comment.user == request.user:
            comment.delete()
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            comment.delete()
            return redirect("/home/")
        except Comment.DoesNotExist:
            return redirect("/home/")
    return render(request, "main/home.html",{"comments": Comment.objects.all().order_by("-created_at")})

@login_required(login_url="/login")
def create_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment =form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("/home/")
    else:
        form = CommentForm()
    return render(request, "main/create_comment.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home/")
    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {"form": form})