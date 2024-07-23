from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Admin_tbl, Trainer_tbl, student_tbl
from datetime import date, datetime

# Create your views here.
# def login(request):
#     return render(request, 'manageuser/login.html')
# from ..training.models import Course, Batch
from training.models import Batch

from training.models import StudentBatch


from training.models import Course

from student.models import feedback


def test(request):
    return render(request, 'manageuser/adminprof.html')


def base(request):
    return render(request, 'manageuser/base.html')


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         print(username)
#         print("*******77*****")
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             print("user test")
#             login(request, user)
#             if request.user.is_active:
#                 # list = User.objects.all()
#
#                 user_obj = User.objects.filter(username=username).values('id')
#
#                 student_obj = student_tbl.objects.filter(user__in=user_obj).all().values('id')
#
#                 student_batch_obj = StudentBatch.objects.filter(student_id__in=student_obj).all().values('batch_id')
#                 batch_obj = Batch.objects.filter(id__in=student_batch_obj).all().values('id', 'course__course_name',
#                                                                                         'course__course_duration',
#                                                                                         'trainer_id')
#                 print('llll', batch_obj)
#
#                 table_data = StudentBatch.objects.select_related('student_id').all()
#                 print("tsting obj")
#
#                 # context_values = {'user_obj': user_obj, 'student_obj': student_obj, 'student_batch_obj': student_batch_obj, 'batch_obj': batch_obj}
#                 return render(request, 'user/student/student.html',
#                               {'context': user_obj, 'student_obj': student_obj, 'student_batch_obj': student_batch_obj,
#                                'batch_obj': batch_obj})
#
#                 # print(table_data)
#                 # context_values = {'user_obj': user_obj, 'student_obj': student_obj, 'student_batch_obj': student_batch_obj, 'batch_obj': batch_obj}
#                 # print("tsting obj")
#                 # print(context_values)
#                 # # context = {'usr': obj1}
#                 # # print('llkwlqd', context)
#                 #
#                 # return render(request, 'manageuser/student.html', {'context': user_obj})
#
#             return redirect(studentlist)
#         else:
#             print("invalid credentials")
#             msg = "Invalid Username or password..."
#             return render(request, 'manageuser/login2.html')
#     return render(request, 'manageuser/login2.html')


def loginadmin(request):
    return render(request, 'manageuser/adminlogin.html')


def trainer(request):
    return render(request, 'manageuser/trainer.html')


def getdate(format='%Y-%m-%d %H:%M'):
    return datetime.now().strftime(format)


@login_required(login_url='/adminlogin')
def addadmin(request):
    if request.method == 'POST':
        # print('************',request.data)
        first_name = request.POST['first_name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        created_on = getdate()
        status = request.POST['status']
        # username = request.POST['username']
        password = request.POST['password']
        print("Hai")
        print(first_name)

        data1 = User.objects.create(first_name=first_name, last_name=last_name, username=email, email=email,
                                    password=password)

        print(data1)
        # Admin_tbl.objects.update(data1)
        print(data1)
        data2 = Admin_tbl.objects.create(user_id=data1.id, phone=phone, created_on=created_on, status=status)
        print(data2)

        data1.save()
        data2.save()

    return render(request, 'manageuser/addadmins.html')


@login_required(login_url='/adminlogin')
def adminview(request, id):
    print('++++++++++1++++++++=')
    user = Admin_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                  'created_on',
                                                  'id', 'status')
    print(user)

    if request.method == 'GET':
        # user = Admin_tbl.objects.get(id=id)
        print(user)

        context = {
            "user": user
        }
    else:
        context = {
            "user": user
        }
        print('++++++++++2++++++++++')

    return render(request, 'manageuser/adminprof.html', context)


@login_required(login_url='/adminlogin')
def adminedit(request, id, user=None):
    if request.method == 'GET':
        user = Admin_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                      'status', 'id')
        print('+++++++++56+++++++++', user)

        context = {
            "user": user
        }
    else:
        print('+++++++++3++++++++++')

        context = {
            "user": user
        }

    return render(request, 'manageuser/editadmins.html', context)


@login_required(login_url='/adminlogin')
def updateadmin(request):
    if request.method == 'POST':
        # userid =  request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # created_on = request.POST.get('created_on')
        status = request.POST.get('status')
        print('+++++f+++++++++', status)

        # user1 = User.objects.filter(id=id).update(first_name=first_name, last_name=last_name, email=email)

        # print(userid)

        Admin_tbl.objects.filter(user__email=email).update(phone=phone, status=status)
        User.objects.filter(email=email).update(first_name=first_name, last_name=last_name, email=email)

        return redirect('manageuser:adminlist')


@login_required(login_url='/adminlogin')
def adminlist(request):
    if request.method == 'GET':
        # list = User.objects.all()
        list = Admin_tbl.objects.all().values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                              'created_on', 'id', 'status')

        print(list)
        context = {'list': list}
        print('+++++++++++++++++++++++', list)
        return render(request, 'manageuser/listadmins.html', context)


@login_required(login_url='/adminlogin')
def deleteadmin(request, id):
    Admin_tbl.objects.filter(id=id).delete()
    return redirect('manageuser:adminlist')


def adminlogin(request):
    # if request.user.is_authenticated:
    #     return redirect(admin_login)

    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        print("*******11*****")
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('manageuser:adminlist')
        else:
            print("invalid credentials")
            msg = "Invalid Username or password..."
            return render(request, 'manageuser/adminlogin.html', {'msg': msg})
    return render(request, 'manageuser/adminlogin.html')


def check_is_admin(args):
    pass


# def adminlogin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         print(username)
#         password = request.POST.get('password')
#
#         data = User.objects.filter(username=username, password=password).all()
#         print(data)
#
#         if request.user.data.is_admin:
#             return render(request, 'manageuser/adminlist.html')
#         else:
#             return render(request, 'manageuser/trainer')


# def admin_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(username)
#
#
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return render(request,'manageuser/sample.html')
#         else:
#             messages.info(request, 'Invalid Username or Password')
#             return render(request,'manageuser/login.html')
#
#


# else:
#      return render(request, 'manageuser/login.html')
@login_required(login_url='/adminlogin')
def addtrainer(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        created_on = getdate()
        status = request.POST['status']
        password = request.POST['password']
        print("Hai")
        print(first_name)

        var1 = User.objects.create(first_name=first_name, last_name=last_name, username=email, email=email,
                                   password=password, is_staff=True)
        print(var1)
        var2 = Trainer_tbl.objects.create(user_id=var1.id, phone=phone, created_on=created_on, status=status)
        print(var2)

        var1.save()
        var2.save()

    return render(request, 'manageuser/addtrainers.html')


@login_required(login_url='/adminlogin')
def trainerlist(request):
    if request.method == 'GET':
        list = Trainer_tbl.objects.all().values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                'created_on', 'id', 'status')
        print(list)
        context = {'list': list}
        return render(request, 'manageuser/listtrainers.html', context)


@login_required(login_url='/adminlogin')
def trainerview(request, id):
    user = Trainer_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                    'id', 'created_on', 'status')
    if request.method == 'GET':
        print('++++++++25++++++++++++')

        context = {
            "user": user
        }
    else:
        context = {
            "user": user
        }

    return render(request, 'manageuser/trainerprof.html', context)


@login_required(login_url='/adminlogin')
def updatetrainer(request):
    if request.method == 'POST':
        # userid =  request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # created_on = request.POST.get('created_on')
        status = request.POST.get('status')

        # user1 = User.objects.filter(id=id).update(first_name=first_name, last_name=last_name, email=email)

        Trainer_tbl.objects.filter(user__email=email).update(phone=phone, status=status)
        User.objects.filter(email=email).update(first_name=first_name, last_name=last_name)

        print('+++++++++++++++', email)

    return redirect('manageuser:trainerlist')


@login_required(login_url='/adminlogin')
def traineredit(request, id):
    if request.method == 'GET':
        user = Trainer_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                        'status', 'id')
        # user = Admin_tbl.objects.get(id=id)
        print('+++++45++++++++')

        context = {
            "user": user
        }

    return render(request, 'manageuser/edittrainers.html', context)


@login_required(login_url='/adminlogin')
def deletetrainer(request, id):
    Trainer_tbl.objects.filter(id=id).delete()
    return redirect('trainerlist')


def adminsearch(request):
    admin_list = Admin_tbl.objects.all()


@login_required(login_url='/adminlogin')
def addstudent(request):
    if request.method == 'POST':
        # print('************',request.data)
        first_name = request.POST['first_name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        created_on = getdate()
        status = request.POST['status']
        # username = request.POST['username']
        password = request.POST['password']
        print("Hai")
        print(first_name)

        data1 = User.objects.create(first_name=first_name, last_name=last_name, username=email, email=email,
                                    password=password)

        print(data1)
        # Admin_tbl.objects.update(data1)
        print(data1)
        data2 = student_tbl.objects.create(user_id=data1.id, phone=phone, created_on=created_on, status=status)
        print(data2)

        data1.save()
        data2.save()

    return render(request, 'manageuser/addstudents.html')


@login_required(login_url='/adminlogin')
def liststudents(request):
    if request.method == 'GET':
        # list = User.objects.all()
        list = student_tbl.objects.all().values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                'created_on', 'id', 'status')

        print(list)
        context = {'list': list}
        print('+++++++++++++++++++++++', list)
        return render(request, 'manageuser/liststudents.html', context)


@login_required(login_url='/adminlogin')
def studentview(request, id):
    print('++++++++++1++++++++=')
    user = student_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                    'created_on',
                                                    'id', 'status')
    print(user)

    if request.method == 'GET':
        # user = Admin_tbl.objects.get(id=id)
        print(user)

        context = {
            "user": user
        }
    else:
        context = {
            "user": user
        }
        print('++++++++++2++++++++++')

    return render(request, 'manageuser/studentprof.html', context)


@login_required(login_url='/adminlogin')
def editstudent(request, id, user=None):
    if request.method == 'GET':
        user = student_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                        'status', 'id')
        print('+++++++++56+++++++++', user)

        context = {
            "user": user
        }
    else:
        print('+++++++++3++++++++++')

        context = {
            "user": user
        }

    return render(request, 'manageuser/editstudents.html', context)


@login_required(login_url='/adminlogin')
def updatestudent(request):
    if request.method == 'POST':
        # userid =  request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # created_on = request.POST.get('created_on')
        status = request.POST.get('status')
        print('+++++f+++++++++', status)

        # user1 = User.objects.filter(id=id).update(first_name=first_name, last_name=last_name, email=email)

        # print(userid)

        student_tbl.objects.filter(user__email=email).update(phone=phone, status=status)
        User.objects.filter(email=email).update(first_name=first_name, last_name=last_name, email=email)

        return redirect('manageuser:studentlist')


@login_required(login_url='/adminlogin')
def deletestudent(request, id):
    student_tbl.objects.filter(id=id).delete()
    return redirect('manageuser:studentlist')


def studenttrainerview(request, id):
    user = Trainer_tbl.objects.filter(id=id).values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                    'id', 'created_on', 'status')
    if request.method == 'GET':
        print('++++++++100++++++++++++')

        context = {
            "user": user
        }
    else:
        context = {
            "user": user
        }

    return render(request, 'manageuser/studenttrnr.html', context)


def view_feedback(request):
    if request.method == 'GET':
        # list = User.objects.all()
        list = feedback.objects.all().values('batch_id', 'student_id__user__first_name','student_id__user__last_name',
                                             'student_id__user__email',
                                             'course_id', 'rating',
                                             'message')

        print(list)
        context = {'list': list}
        print('+++++++++++++++++++++++', list)
        return render(request, 'manageuser/feedbackview.html', context)

def viewprogresscourse(reqeust):
    course = Course.objects.all()
    return render(reqeust, 'manageuser/viewprogresscourse.html', {
        "course": course
    })

def viewprogressbatch(request, id):
    course = Course.objects.get(id=id)
    course_id = course.id

    batch = Batch.objects.filter(course=course_id)
    print('ffwef',batch)

    return render(request, 'manageuser/viewprogressbatch.html', {
        "batch": batch,
        "course_id": course_id

    })