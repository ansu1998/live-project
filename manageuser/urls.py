from django.urls import path

# urlpatterns = [
#     path('admin_login', views.admin_login),
# ]

from . import views

app_name = 'manageuser'

urlpatterns = [
    # path('home/', views.adminlogin, name='admin_login'),
    # path('', views.user_login, name='user_login'),
    path('adminprofile', views.test, name='adminprofile'),
    path('loginadmin', views.loginadmin, name='adminlogin'),
    path('trainer/', views.trainer, name='trainer'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('addadmin', views.addadmin, name='addadmin'),
    path('adminview/<int:id>', views.adminview, name='adminview'),
    path('editadmin/<int:id>', views.adminedit, name='adminedit'),
    path('updateadmin', views.updateadmin, name='updateadmin'),
    path('adminlist/', views.adminlist, name='adminlist'),
    path('deleteadmin/<int:id>', views.deleteadmin, name='deleteadmin'),
    path('base/', views.base, name='base'),
    path('addtrainer', views.addtrainer, name='addtrainer'),
    path('trainerlist', views.trainerlist, name='trainerlist'),
    path('trainerview/<int:id>', views.trainerview, name='trainerview'),
    path('updatetrainer', views.updatetrainer, name='updatetrainer'),
    path('edittrainer/<int:id>', views.traineredit, name='traineredit'),
    path('deletetrainer/<int:id>', views.deletetrainer, name='deletetrainer'),
    path('addstudent', views.addstudent, name='addstudent'),
    path('liststudents/', views.liststudents, name='liststudents'),
    path('studentview/<int:id>', views.studentview, name='studentview'),
    path('editstudent/<int:id>', views.editstudent, name='editstudent'),
    path('updatestudent', views.updatestudent, name='updatestudent'),
    path('deletestudent/<int:id>', views.deletestudent, name='deletestudent'),
    path('view_feedback', views.view_feedback, name='view_feedback'),
    path('viewprogresscourse', views.viewprogresscourse, name='viewprogresscourse'),
    path('viewprogressbatch/<int:id>', views.viewprogressbatch, name='viewprogressbatch'),


]
