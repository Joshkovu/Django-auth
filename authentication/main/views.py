from django.shortcuts import redirect, render
from .forms import SignUpForm
# Create your views here.
def home(request):
    return render(request, "main/home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     login(request, user)
        #     return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {"form": form})