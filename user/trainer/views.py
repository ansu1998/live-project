from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from training.models import Course, Batch, Milestone, StudentBatch, Topic

from manageuser.models import student_tbl, Trainer_tbl

from .models import ProgressTbl


def baset(reqeust):
    return render(reqeust, 'trainer/baset.html')


def tcourse(reqeust):
    current_user = reqeust.user
    user_id = current_user.id
    trainer_obj = Trainer_tbl.objects.get(user=user_id)
    batch = Batch.objects.filter(trainer=trainer_obj).values_list('id', flat=True)
    course = Course.objects.filter(batch__in=batch).distinct()
    return render(reqeust, 'trainer/course.html', {
        "course": course
    })


def batch(reqeust, id):
    course = Course.objects.get(id=id)
    current_user = reqeust.user
    user_id = current_user.id
    trainer_obj = Trainer_tbl.objects.get(user=user_id)
    batchs = Batch.objects.filter(trainer=trainer_obj,course=course)
    return render(reqeust, 'trainer/batch.html', {
        "batchs": batchs
    })


def view_student(reqeust, id):
    batch = Batch.objects.get(id=id)
    students = StudentBatch.objects.filter(batch_id=batch)
    student_list = []
    for std in students:
        st_id = std.student_id
        student_list.append(st_id)
    student_dtl = student_tbl.objects.filter(id__in=student_list).values('id', 'phone', 'user')
    return render(reqeust, 'trainer/view_student.html', {
        "student_dtl": student_dtl
    })


def mark_progress(reqeust, id):
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
    progress_rate = progress_sum / progress_count_sum * 100
    return render(reqeust, 'trainer/mark_progress.html', {
        "progress_list": progress_list,
        "batch": batch,
        "progress_rate": progress_rate
    })


def edit_progress(request, batch_id, mile_id):
    batch = Batch.objects.get(id=batch_id)
    milestone = Milestone.objects.get(id=mile_id)
    topics = Topic.objects.filter(milestone=milestone.id)
    topic_list = []
    for each_topic in topics:
        prog_topic = ProgressTbl.objects.filter(topic=each_topic, batch=batch)
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
                "status": "To_do",
                "start_date": "12/12/2022",
                "end_date": "12/12/2022",
                "topic_id": each_topic.id
            }
        topic_list.append(topic_dict)
    return render(request, 'trainer/edit_progress.html', {
        "topic_list": topic_list,
        "batch": batch
    })


def save_progress(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')

        topic_id = request.POST.get('topic_id')
        batch_id = request.POST.get('batch_id')
        topic = Topic.objects.get(id=topic_id)
        batch = Batch.objects.get(id=batch_id)
        milestone = topic.milestone

        mile = Milestone.objects.get(id=milestone)

        prog_topic = ProgressTbl.objects.filter(topic=topic_id)
        if prog_topic:
            prog_topic[0].start_date = start_date
            prog_topic[0].end_date = end_date
            prog_topic[0].prog_status = status
            prog_topic[0].save()

        else:
            new_progress = ProgressTbl.objects.create(start_date=start_date, end_date=end_date, topic=topic,
                                                      prog_status=status, batch=batch)

        return redirect(f'/trainer/mark_progress/{batch.id}')
