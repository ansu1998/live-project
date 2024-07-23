from django.urls import path
from . import views


app_name = 'trainer'


urlpatterns = [
    path('baset', views.baset, name='baset'),
    path('tcourse', views.tcourse, name='tcourse'),
    path('batch/<int:id>', views.batch, name='batch'),
    path('view_student/<int:id>', views.view_student, name='view_student'),
    path('mark_progress/<int:id>', views.mark_progress, name='mark_progress'),
    path('edit_progress/<int:batch_id>/<int:mile_id>', views.edit_progress, name='edit_progress'),
    path('save_progress', views.save_progress, name='save_progress'),

]