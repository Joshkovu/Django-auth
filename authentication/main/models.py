from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    INTERNSHIP_ADMIN = "internship_admin"
    ACADEMIC_SUPERVISOR = "academic_supervisor"
    WORKPLACE_SUPERVISOR = "workplace_supervisor"
    STUDENT = "student"

    ROLE_CHOICES = [
        (INTERNSHIP_ADMIN, "Internship Administrator"),
        (ACADEMIC_SUPERVISOR, "Academic Supervisor"),
        (WORKPLACE_SUPERVISOR, "Workplace Supervisor"),
        (STUDENT, "Student"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class WeeklyLog(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_logs")
    week_start = models.DateField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    workplace_supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_weekly_logs",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-week_start", "-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "week_start"], name="unique_weekly_log_per_student_week")
        ]

    def __str__(self):
        return f"{self.student.username} - {self.week_start}"


class Mark(models.Model):
    weekly_log = models.OneToOneField(WeeklyLog, on_delete=models.CASCADE, related_name="mark")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marks")
    academic_supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="awarded_marks",
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.student = self.weekly_log.student
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.score}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"