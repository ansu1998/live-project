from django.db.models import Max
from django.shortcuts import render, redirect
from django.db.models import Max

# Create your views here.
from training.models import Course, Topic, Batch, Milestone, StudentBatch

from manageuser.models import student_tbl, Trainer_tbl
from user.trainer.models import ProgressTbl
from manageuser.views import getdate
from datetime import date

from manageuser.models import Trainer_tbl


def base(reqeust):
    return render(reqeust, 'training/base.html')


def course(reqeust):
    course = Course.objects.all()
    return render(reqeust, 'training/course.html', {
        "course": course
    })


def delete(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('/training/course')


def add_course(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        duration = request.POST.get('duration')
        disc = request.POST.get('disc')
        status = request.POST.get('status')
        topz = request.POST.get('topstr')
        topics = topz.split(',')
        course_obj = Course.objects.create(course_name=cname, course_duration=duration, description=disc, status=status)
        course_obj.save()
        for top in topics:
            new_topic = Topic.objects.create(topic=top, course_id=course_obj.id)
        return redirect(f'milestone/{course_obj.id}')
    else:
        return render(request, 'training/add_course.html')


def view_course(request, id):
    course = Course.objects.get(id=id)
    topics = Topic.objects.filter(course=course)
    batch = Batch.objects.filter(course=course)
    return render(request, 'training/view_course.html', {
        "course": course,
        "topics": topics,
        "batch": batch
    })


def batch(request, id):
    course = Course.objects.get(id=id)
    course_id = course.id
    batch = Batch.objects.filter(course=course_id)

    if batch:
        batch1 = batch[0]
    else:
        batch1 = False

    return render(request, 'training/batch.html', {
        "batch": batch,
        "course_id": course_id,
        "batch1":batch1
    })


def add_batch(request, id):
    if request.method == 'POST':
        course = Course.objects.get(id=id)
        bname = request.POST.get('bname')
        sdate = request.POST.get('sdate')
        edate = request.POST.get('edate')
        status = request.POST.get('status')
        trainer_id = request.POST['trainer']
        trainer_obj = Trainer_tbl.objects.get(id=trainer_id)
        batch_obj = Batch.objects.create(batch_name=bname, start_date=sdate, end_date=edate, course=course,
                                         trainer=trainer_obj, status=status)
        batch_obj.save()
        return redirect(f'/training/batch/{batch_obj.course.id}')
    else:
        course = Course.objects.get(id=id)
        course_id = course.id
        trainer = Trainer_tbl.objects.all().values('user__first_name', 'user__last_name', 'id')
        return render(request, 'training/add_batch.html', {
            "trainer": trainer,
            "course_id": course_id
        })


def edit_course(request, id):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        duration = request.POST.get('course_duration')
        description = request.POST.get('description')
        status = request.POST.get('status')
        Course.objects.filter(id=id).update(course_name=course_name, course_duration=duration, description=description,
                                            status=status)

        return redirect(f'/training/course')
    if request.method == 'GET':
        course = Course.objects.get(id=id)
        topics = Topic.objects.filter(course=course)
        return render(request, 'training/edit_course.html', {
            "course": course,
            "topics": topics
        })


def view_batch(request, id):
    batch = Batch.objects.get(id=id)
    student = StudentBatch.objects.filter(batch_id=batch.id).values()
    student_list = [item['student_id_id']for item in student]
    student_dtl =student_tbl.objects.filter(id__in=student_list)
    return render(request, 'training/view_batch.html', {
        "batch": batch,
        "student_dtl": student_dtl
    })


def edit_batch(request, id):
    if request.method == 'POST':
        new_batch = Batch.objects.get(id=id)
        new_batch.batch_name = request.POST.get('bname')
        new_batch.sart_date = request.POST.get('sdate')
        new_batch.end_date = request.POST.get('edate')
        new_batch.status = request.POST.get('status')
        trainer_id = request.POST.get('trainer')
        trainer_obj = Trainer_tbl.objects.get(id=trainer_id)
        new_batch.trainer = trainer_obj
        new_batch.save()

        return redirect(f'/batch/{new_batch.course.id}')
    else:
        batch = Batch.objects.get(id=id)
        trainer = Trainer_tbl.objects.all().values('user__first_name', 'user__last_name', 'id')
        return render(request, 'training/edit_batch.html', {
            "batch": batch,
            "trainer": trainer
        })


def delete_batch(request, id):
    batch = Batch.objects.get(id=id)
    course = Course.objects.get(id=batch.course.id)
    batch.delete()
    return redirect(f'/batch/{batch.course.id}')


def milestone(request, id):
    if request.method == 'POST':
        mile_name = request.POST.get('mile_name')
        topics_input = request.POST.getlist('mile')
        topics = [int(i) for i in topics_input[0].split(',') if i]
        for top in topics:
            print(top)
        course = Course.objects.get(id=id)
        order = Milestone.objects.all().aggregate(Max('order'))
        if not order.get("order__max"):
            ord = 1
        else:
            ord = int(order.get("order__max")) + 1
        mile_obj = Milestone.objects.create(mile_name=mile_name, order=ord, course=course)
        for top in topics:
            topz = Topic.objects.get(id=top)
            topz.milestone = mile_obj.id
            topz.save()
        topics = Topic.objects.filter(course_id=id)
        top_list = []
        for topic_items in topics:
            if topic_items.milestone == None:
                top_list.append(topic_items)
        print(top_list)
        show_mile = Milestone.objects.filter(course=id)
        mile_list = []
        for each_milestone in show_mile:
            mile_topic = Topic.objects.filter(milestone=each_milestone.id)
            topic_names = [each_topic.topic for each_topic in mile_topic]
            mile_list.append({
                "name": each_milestone.mile_name,
                "topic_list": topic_names
            })
        return render(request, 'training/milestone.html', {
            "topics": top_list,
            "course_id": id,
            "mile_list": mile_list
        })
    else:
        topics = Topic.objects.filter(course_id=id)
        top_list = []
        for topic_items in topics:
            if not topic_items.milestone:
                top_list.append(topic_items)
        if not top_list:
            mile_flag = False
        else:
            mile_flag = True
        print(top_list)

        return render(request, 'training/milestone.html', {
            "topics": top_list,
            "course_id": id,
            "mile_flag": mile_flag
        })


def sample(request):
    course = Course.objects.filter(created_on)
    student = student_tbl.objects.all()
    batch = Batch.objects.all()



    return render(request, 'training/sample.html')


def view_milestone(request, id):
    batch = Batch.objects.get(id=id)
    course = Course.objects.get(id=batch.course.id)
    show_mile = Milestone.objects.filter(course=course)
    mile_list = []
    for each_milestone in show_mile:
        mile_topic = Topic.objects.filter(milestone=each_milestone.id)
        topic_names = [each_topic.topic for each_topic in mile_topic]
        mile_list.append({
            "name": each_milestone.mile_name,
            "topic_list": topic_names
        })
    return render(request, 'training/view_milestone.html', {
        "course_id": id,
        "mile_list": mile_list
    })


def new_topic(request, id):
    if request.method == 'POST':
        new_topic = request.POST.get('new_topic')
        course = Course.objects.get(id=id)
        new_course = Topic.objects.create(topic=new_topic, course=course)
        return redirect(f'/training/edit_course/{course.id}')


def add_student(request, id):
    if request.method == 'POST':
        student_l = request.POST.getlist('student')
        student_list = [int(i) for i in student_l[0].split(',')]

        for stud in student_list:
            new_students = StudentBatch.objects.create(student_id_id=stud, batch_id_id=id, created_on=date.today())
        batch= Batch.objects.get(id=id)
        return redirect(f'/training/batch/{batch.course.id}')
    else:
        students = student_tbl.objects.all().values('user__first_name', 'user__last_name', 'id')
        return render(request, 'training/add_student.html', {

            "students": students,
            "batch_id": id

        })


def view_progress(reqeust, id):
    batch = Batch.objects.get(id=id)
    course = Course.objects.get(batch=batch)
    milestone = Milestone.objects.filter(course=course)
    progress_list = []
    progress_count = 0
    progress_sum = 0
    for each_milestone in milestone:
        mile_topic = Topic.objects.filter(milestone=each_milestone.id)
        topic_list = []
        for each_topic in mile_topic:
            prog_topic = ProgressTbl.objects.filter(topic=each_topic.id,batch=batch.id)
            if prog_topic:
                topic_dict = {
                    "topic_name": each_topic.topic,
                    "status": prog_topic[0].prog_status,
                    "start_date": prog_topic[0].start_date,
                    "end_date": prog_topic[0].end_date,
                    "topic_id": each_topic.id
                }
            else:
                topic_dict = {
                    "topic_name": each_topic.topic,
                    "status": "To Do",
                    "start_date": "12/12/2022",
                    "end_date": "12/12/2022",
                    "topic_id": each_topic.id
                }
            topic_list.append(topic_dict)
        num_of_topic = len(topic_list)
        count = 0
        for top in topic_list:

            if top['status'] == 'Completed':
                count = count + 1
        progs = int(count / num_of_topic * 100)
        progress_count = progress_count + 1
        progress_sum = progress_sum + progs
        progress_list.append({
            "name": each_milestone.mile_name,
            "topic_dtl": topic_list,
            "milestone_id": each_milestone,
            "progs": progs
        })
    progress_count_sum = progress_count * 100
    progress_rate =  progress_sum / progress_count_sum * 100

    return render(reqeust, 'training/view_progress.html', {
        "progress_list": progress_list,
        "batch": batch,
        "progress_rate": progress_rate
    })
