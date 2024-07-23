from django.db import models

# Create your models here.
from training.models import Batch,Course

from manageuser.models import student_tbl


class feedback(models.Model):
    student_id = models.ForeignKey(student_tbl, on_delete=models.CASCADE)
    rating = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student_id)