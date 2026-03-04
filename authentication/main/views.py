from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MarkForm, SignUpForm, UserWithRoleCreationForm, WeeklyLogForm
from .models import Mark, UserProfile, WeeklyLog


def get_user_role(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile.role


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="/login")
        def wrapper(request, *args, **kwargs):
            if get_user_role(request.user) not in allowed_roles:
                messages.error(request, "You do not have permission to access this page.")
                return redirect("home")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# Create your views here.
@login_required(login_url="/login")
def home(request):
    role = get_user_role(request.user)
    context = {
        "role": role,
        "all_roles": {
            "internship_admin": UserProfile.INTERNSHIP_ADMIN,
            "academic_supervisor": UserProfile.ACADEMIC_SUPERVISOR,
            "workplace_supervisor": UserProfile.WORKPLACE_SUPERVISOR,
            "student": UserProfile.STUDENT,
        },
    }

    if role == UserProfile.STUDENT:
        context["weekly_logs"] = WeeklyLog.objects.filter(student=request.user).select_related("mark")
        context["marks"] = Mark.objects.filter(student=request.user).select_related("academic_supervisor", "weekly_log")
    elif role == UserProfile.WORKPLACE_SUPERVISOR:
        context["pending_logs"] = WeeklyLog.objects.filter(status=WeeklyLog.STATUS_PENDING).select_related("student")
        context["approved_logs"] = WeeklyLog.objects.filter(
            workplace_supervisor=request.user, status=WeeklyLog.STATUS_APPROVED
        ).select_related("student")
    elif role == UserProfile.ACADEMIC_SUPERVISOR:
        context["approved_logs"] = WeeklyLog.objects.filter(status=WeeklyLog.STATUS_APPROVED).select_related("student")
        context["awarded_marks"] = Mark.objects.filter(academic_supervisor=request.user).select_related(
            "student", "weekly_log"
        )
    elif role == UserProfile.INTERNSHIP_ADMIN:
        context["users"] = UserProfile.objects.select_related("user").order_by("user__username")

    return render(request, "main/home.html", context)


@role_required(UserProfile.STUDENT)
def create_weekly_log(request):
    if request.method == "POST":
        form = WeeklyLogForm(request.POST)
        if form.is_valid():
            weekly_log = form.save(commit=False)
            weekly_log.student = request.user
            weekly_log.save()
            messages.success(request, "Weekly log created successfully.")
            return redirect("/home/")
    else:
        form = WeeklyLogForm()
    return render(request, "main/create_weekly_log.html", {"form": form})


@role_required(UserProfile.WORKPLACE_SUPERVISOR)
def approve_weekly_log(request, log_id):
    if request.method != "POST":
        return redirect("home")

    weekly_log = get_object_or_404(WeeklyLog, id=log_id)
    weekly_log.status = WeeklyLog.STATUS_APPROVED
    weekly_log.workplace_supervisor = request.user
    weekly_log.approved_at = timezone.now()
    weekly_log.save(update_fields=["status", "workplace_supervisor", "approved_at", "updated_at"])
    messages.success(request, "Weekly log approved.")
    return redirect("home")


@role_required(UserProfile.ACADEMIC_SUPERVISOR)
def award_mark(request, log_id):
    weekly_log = get_object_or_404(WeeklyLog, id=log_id, status=WeeklyLog.STATUS_APPROVED)
    existing_mark = Mark.objects.filter(weekly_log=weekly_log).first()

    if request.method == "POST":
        form = MarkForm(request.POST, instance=existing_mark)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.weekly_log = weekly_log
            mark.student = weekly_log.student
            mark.academic_supervisor = request.user
            mark.save()
            messages.success(request, "Mark saved successfully.")
            return redirect("home")
    else:
        form = MarkForm(instance=existing_mark)

    return render(request, "main/award_mark.html", {"form": form, "weekly_log": weekly_log})


@role_required(UserProfile.INTERNSHIP_ADMIN)
def create_user_account(request):
    if request.method == "POST":
        form = UserWithRoleCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User account created successfully.")
            return redirect("home")
    else:
        form = UserWithRoleCreationForm()
    return render(request, "main/create_user_account.html", {"form": form})


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