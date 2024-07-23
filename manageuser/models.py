# import phone_field
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Admin_tbl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=30, null=True)
    created_on = models.DateField(max_length=30, auto_now=True)
    status = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Trainer_tbl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="trainer_user")
    phone = models.CharField(max_length=30)
    created_on = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)


class student_tbl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="student_user")
    phone = models.CharField(max_length=30)
    created_on = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

    def __str__(self):
        return str(self.user)
