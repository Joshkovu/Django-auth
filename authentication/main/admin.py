from django.contrib import admin
from .models import Comment, Mark, UserProfile, WeeklyLog

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WeeklyLog)
admin.site.register(Mark)
admin.site.register(Comment)
