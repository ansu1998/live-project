from django.db import models

# Create your models here.
from manageuser.models import student_tbl, Trainer_tbl
from manageuser.models import Trainer_tbl


class Abstract(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Course(models.Model):
    course_name = models.CharField(max_length=50, )
    course_duration = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField(default=True)


class Topic(models.Model):
    topic = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    milestone = models.IntegerField(null=True)


class Batch(models.Model):
    batch_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer_tbl, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=True)


class Milestone(models.Model):
    order = models.IntegerField(default=0)
    mile_name = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class StudentBatch(models.Model):
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batches')
    student_id = models.ForeignKey(student_tbl, on_delete=models.CASCADE, related_name='students')
    created_on = models.DateField()
