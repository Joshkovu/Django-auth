from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.",required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


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

