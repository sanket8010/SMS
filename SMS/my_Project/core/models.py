from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):

    # -------------------------
    # Status Choices
    # -------------------------
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    # -------------------------
    # User Login (Django Auth)
    # -------------------------
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    # -------------------------
    # Personal Details
    # -------------------------
    dob = models.DateField(verbose_name="Date of Birth")
    age = models.PositiveIntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=10)

    gender = models.CharField(
        max_length=10,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ),
        default='Male'
    )

    # -------------------------
    # Academic Details
    # -------------------------
    course = models.CharField(max_length=50, default="MCA")
    previous_marks = models.FloatField(default=0.0)

    roll_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # -------------------------
    # Verification Status
    # -------------------------
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # -------------------------
    # Timestamp
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)

    # -------------------------
    # String Representation
    # -------------------------
    def __str__(self):
        return f"{self.user.username} - {self.status}"
