from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.urls import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

import datetime
from django.utils import timezone
import xlwt
from django.core.files import File

def export_users_xls():
        # response = HttpResponse(content_type='application/ms-excel')
        # response['Content-Disposition'] = 'attachment; filename= "users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Scores')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Student', 'Scores']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Attendee.objects.filter(exam_fk=self.exam_fk).values_list('student_fk', 'total_marks')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        filename = str(self)+".xls"
        wb.save(filename)
        return filename



# @login_required(login_url=reverse('stud_app:login'))       circular call
# @login_required(login_url='/students/login')
def home_view(request, username):
    student = Student.objects.get(user__username = username)

    return render(request, 'stud_app/home.html', context={
        'username': username,
        'student' : student,
        'name': student.get_name(),
        'current_page': 'home',
        
    })



def blank_page(request):
    return HttpResponseRedirect(reverse('stud_app:login'))

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            student = Student.objects.get(user__username = username)
        except Student.DoesNotExist:
            context = { 
                'no_user' : True,
                'first_render' : False,
                'wrong_password' : False,
            } 
            return render(request, 'stud_app/login.html', context)
        else:
            if student.user.check_password(password):
                # return HttpResponse("HOME")
                # return HttpResponseRedirect('students/home/')
                return HttpResponseRedirect(reverse('stud_app:home', args=[username,]))
            else:
                context = { 
                'wrong_password' : True,
                'no_user' : False,
                'first_render' : False,
                } 
                return render(request, 'stud_app/login.html', context)
    else:
        context = { 
                'first_render' : True,
                'wrong_password' : False,
                'no_user' : False,
            } 
        return render(request, 'stud_app/login.html', context)


def courses_view(request, username):
    if request.method == 'POST':
        pass
    else:
        student = get_object_or_404(Student, user__username = username)
        courses = student.course_fk.all()
        context = { 
                'username': username,
                'courses': courses,
                'current_page': 'courses',
            } 
        return render(request, 'stud_app/courses.html', context)

def exam_list_view(request, username):
    if request.method == 'POST':
        exams = Exam.objects.all()
        for exam in exams:
            if str(exam.id) in request.POST:
                # return HttpResponse('Attending exam' + exam.exam_name)
                return HttpResponseRedirect(reverse('stud_app:exams', args=[username, exam.id,]))
        else:
            return HttpResponse('NO such exams\n',request.POST)

    else:
        student = get_object_or_404(Student, user__username = username)
        courses = student.course_fk.all()
        exams = Exam.objects.filter(Q(course_fk__in=courses))
        unattended_exams = Exam.objects.filter(
            ~Q(attendee__exam_fk__in=exams),
            Q(is_active=True)
        )

        context = { 
                'username': username,
                'exams': unattended_exams,
                'now': timezone.now(),
                'current_page': 'exams',
            } 
        return render(request, 'stud_app/exam_list.html', context)


def exam_view(request, username, exam_id):
    student = get_object_or_404(Student, user__username = username)
    exam = Exam.objects.get(id=exam_id)

    questions = exam.question_set.all()
    

    if request.method == 'POST':
        total_marks = 0
        attendee = Attendee.objects.create(exam_fk=exam, student_fk=student, total_marks=total_marks)

        for qn in questions:
            selected = request.POST.getlist(str(qn.id))
            
            marked_correct = True
            for choice in qn.choice_set.all():
                if (choice.is_correct and str(choice.id) not in selected) or (not choice.is_correct and str(choice.id) in selected):
                    marked_correct = False
                if str(choice.id) in selected:
                    Response.objects.create(attendee_fk=attendee, question=qn, choice=choice)
            
            if marked_correct:
                total_marks += exam.qn_mark
            else:
                if selected:
                    total_marks -= exam.neg_mark
        
        attendee.total_marks=total_marks
        # attendee.excel_file.save('new', File(attendee.export_users_xls()))

        attendee.save()

        return HttpResponseRedirect(reverse('stud_app:scores', args=[username,]))

    else:

        context = {
                'username': username,
                'exam': exam,
                # 'response_formset': response_formset,
                'questions': questions,
                'time_in_sec': int(exam.time_limit.total_seconds()),
                'current_page': 'exams',
        }
        return render(request, 'stud_app/exam.html', context)
        

def scores_view(request, username):
    if request.method == 'POST':
        pass

    else:
        student = get_object_or_404(Student, user__username = username)
        # courses = student.course_fk.all()
        exams_attended = Attendee.objects.filter(student_fk=student)

        context = { 
                'username': username,
                'exams_attended': exams_attended,
                'current_page': 'scores',
            } 
        return render(request, 'stud_app/scores.html', context)