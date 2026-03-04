from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Mark, UserProfile, WeeklyLog

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.",required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit)
        role = self.cleaned_data.get("role", UserProfile.STUDENT)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save(update_fields=["role"])
        if role == UserProfile.INTERNSHIP_ADMIN:
            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=["is_staff", "is_superuser"])
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Your Comment"})
        }
        labels = {
            "content": "Your Comment"
        }


class WeeklyLogForm(forms.ModelForm):
    class Meta:
        model = WeeklyLog
        fields = ["week_start", "title", "content"]
        widgets = {
            "week_start": forms.DateInput(attrs={"type": "date"}),
            "content": forms.Textarea(attrs={"rows": 6, "placeholder": "What did you do this week?"}),
        }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ["score", "feedback"]
        widgets = {
            "feedback": forms.Textarea(attrs={"rows": 4, "placeholder": "Feedback for the student"}),
        }


class UserWithRoleCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        role = self.cleaned_data["role"]

        if role == UserProfile.INTERNSHIP_ADMIN:
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save(update_fields=["role"])

        return user

