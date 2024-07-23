from django.contrib import admin

# Register your models here.
from .models import Admin_tbl, Trainer_tbl, student_tbl

admin.site.register(Admin_tbl)
admin.site.register(Trainer_tbl)
admin.site.register(student_tbl)