from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from manageuser.models import student_tbl, Trainer_tbl
from training.models import StudentBatch, Batch
from training.models import Course, Topic
from student.models import feedback


def studentlist(request):
    if request.method == 'GET':
        # list = User.objects.all()
        list = student_tbl.objects.all().values('user__first_name', 'user__last_name', 'user__email', 'phone',
                                                'created_on', 'id', 'status')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_active:
                user_obj = User.objects.filter(username=username)
                if user_obj[0].is_staff:
                    return redirect('trainer:tcourse')

                user_obj = User.objects.get(username=username)
                student_obj = student_tbl.objects.get(user=user_obj.id)
                student_batch_obj = StudentBatch.objects.filter(student_id=student_obj.id).values()

                student_batch_id_list = [item['batch_id_id'] for item in student_batch_obj]

                batch_details = Batch.objects.filter(id__in=student_batch_id_list).values('course__course_name',
                                                                                          'course__course_duration',
                                                                                          'course__id',
                                                                                          'id', 'trainer_id')
                for item in batch_details:
                    item.update(
                        {
                            'student_id': student_obj.id
                        }
                    )

                print("***********11111111111***********", batch_details)

                # context_values = {'user_obj': user_obj, 'student_obj': student_obj, 'student_batch_obj': student_batch_obj, 'batch_obj': batch_obj}
                return render(request, 'student/student.html',
                              {'batch_details': batch_details
                               })

                # print(table_data)
                # context_values = {'user_obj': user_obj, 'student_obj': student_obj, 'student_batch_obj': student_batch_obj, 'batch_obj': batch_obj}
                # print("tsting obj")
                # print(context_values)
                # # context = {'usr': obj1}
                # # print('llkwlqd', context)
                #
                # return render(request, 'manageuser/student.html', {'context': user_obj})

            return redirect(studentlist)
        else:
            print("invalid credentials")
            msg = "Invalid Username or password..."
            return render(request, 'manageuser/login2.html')
    return render(request, 'manageuser/login2.html')


def stdcourse(request):
    if request.method == 'GET':
        username=request.user.username
        user_obj = User.objects.get(username=username)
        student_obj = student_tbl.objects.get(user=user_obj.id)
        student_batch_obj = StudentBatch.objects.filter(student_id=student_obj.id).values()

        student_batch_id_list = [item['batch_id_id'] for item in student_batch_obj]

        batch_details = Batch.objects.filter(id__in=student_batch_id_list).values('course__course_name',
                                                                                  'course__course_duration',
                                                                                  'course__id',
                                                                                  'id', 'trainer_id')
        for item in batch_details:
            item.update(
                {
                    'student_id': student_obj.id
                }
            )

        print("***********pppppppppppppp***********", batch_details)

        # context_values = {'user_obj': user_obj, 'student_obj': student_obj, 'student_batch_obj': student_batch_obj, 'batch_obj': batch_obj}
        return render(request, 'student/student.html',
                      {'batch_details': batch_details
                       })


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

    return render(request, 'student/studenttrnr.html', context)


def studentviewcourse(request, id):
    course = Course.objects.get(id=id)
    topics = Topic.objects.filter(course=course)
    batch = Batch.objects.filter(course=course)

    return render(request, 'student/studentcourse.html', {
        "course": course,
        "topics": topics,
        "batch": batch
    })


# def logout_view(request):
#     logout(request)
#     return redirect('login2')

def feed__back(request, id, bat, course):
    # stdbatch = StudentBatch.objects.get(id=id)
    # print(stdbatch.id)
    # print("haii")
    #
    # bat = stdbatch.batch_id
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5")
    # print(bat.id)
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    #
    # bati = Batch.objects.get(id=bat.id)
    # print(bati)
    # if request.method == 'POST':
    #     student_id = stdbatch.id
    #     rating = request.POST.get('rating')
    #     message = request.POST.get('message')
    #     batch_id = bat.id
    #     course_id = bati.course__id
    #
    #     feedback_obj = feedback.objects.create(student_id=student_id,rating=rating,message=message,batch_id=batch_id,course_id=course_id)
    #     feedback_obj.save()
    #     return render(request, 'student/feedback.html')

    return render(request, 'student/feedback.html', {"user_id": id, "batch_id": bat, "course": course})


def stdfeedback(request, id):
    print("ads", id)

    # stdbatch = StudentBatch.objects.filter(student_id_id=id)
    #
    # bat = [item.batch_id_id for item in stdbatch]
    #
    # bati = Batch.objects.filter(id__in=bat).values('id')
    # print('**************', bati)
    if request.method == 'POST':
        student_id = request.POST.get('user_id')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        batch_id = request.POST.get('batch')
        course_id = request.POST.get('course')
        print('#################', student_id)
        print('$$$$$$$$$$$$$$$$$', batch_id)
        print('@@@@@@@@@@@@@@@@@', course_id)

        feedback_obj = feedback.objects.create(student_id_id=student_id, rating=rating, message=message,
                                               batch_id_id=batch_id,
                                               course_id_id=course_id)
        feedback_obj.save()
    return render(request, 'student/feedback.html', {"user_id": id})
