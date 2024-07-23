from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from training.models import Topic, Batch


class ProgressTbl(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    prog_status = models.CharField(max_length=20)

