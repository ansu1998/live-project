from django.urls import path


from . import views
app_name = 'student'

urlpatterns = [
    path('userlogin/', views.user_login, name='user_login'),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('studenttrainerview/<int:id>', views.studenttrainerview, name='studenttrainerview'),
    path('studentviewcourse/<int:id>', views.studentviewcourse, name='studentviewcourse'),
    # path('logout', views.logout, name='logout'),
    path('stdfeedback/<int:id>', views.stdfeedback, name='stdfeedback'),
    path('feedback/<int:id>/<int:bat>/<int:course>', views.feed__back, name='feedback'),
    path('stdcourse/', views.stdcourse, name='stdcourse'),



]