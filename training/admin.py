from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Course, Batch, Topic, Milestone, StudentBatch


admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Topic)
admin.site.register(Milestone)

admin.site.register(StudentBatch)



