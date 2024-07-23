
from django.urls import path

from . import views

app_name = 'training'

urlpatterns = [
    path('base', views.base, name='base'),
    path('course', views.course, name='course'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('add_course', views.add_course, name='add_course'),
    path('batch/<int:id>', views.batch, name='batch'),
    path('add_batch/<int:id>', views.add_batch, name='add_batch'),
    path('view_course/<int:id>', views.view_course, name='view_course'),
    path('edit_course/<int:id>', views.edit_course, name='edit_course'),
    path('view_batch/<int:id>', views.view_batch, name='view_batch'),
    path('edit_batch/<int:id>', views.edit_batch, name='edit_batch'),
    path('delete_batch/<int:id>', views.delete_batch, name='delete_batch'),
    path('milestone/<int:id>', views.milestone, name='milestone'),
    path('sample', views.sample, name='sample'),
    path('view_milestone/<int:id>', views.view_milestone, name='view_milestone'),
    path('new_topic/<int:id>', views.new_topic, name='new_topic'),
    path('add_student/<int:id>', views.add_student, name='add_student'),
    path('view_progress/<int:id>', views.view_progress, name='view_progress'),

]
