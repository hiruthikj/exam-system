from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.urls import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# @login_required(login_url=reverse('stud_app:login'))       circular call
# @login_required(login_url='/students/login')
def home_view(request, username):
    return render(request, 'stud_app/home.html', context={
        'username' : username,
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
        exams = Exam.objects.filter(course_fk__in=courses)

        context = { 
                'username': username,
                'exams': exams,
            } 
        return render(request, 'stud_app/exam_list.html', context)


def exam_view(request, username, exam_id):
    student = get_object_or_404(Student, user__username = username)
    exam = Exam.objects.get(id=exam_id)

    questions = exam.question_set.all()


    if request.method == 'POST':
        total_marks = 0
    
        for qn in questions:
            selected = request.POST.getlist(str(qn.id))
            
            marked_correct = True
            for choice in qn.choice_set.all():
                if (choice.is_correct and str(choice.id) not in selected) or (not choice.is_correct and str(choice.id) in selected):
                    marked_correct = False
                    break
            
            if marked_correct:
                total_marks += exam.qn_mark
            else:
                total_marks -= exam.neg_mark
        
        attendee = Attendee.objects.create(exam_fk=exam, student_fk=student, total_marks=total_marks)
        return HttpResponse(f'Attendee  got {total_marks} having selected {selected} {exam.qn_mark}  {exam.neg_mark}')

    else:

        context = {
                'username': username,
                'exam': exam,
                # 'response_formset': response_formset,
                'questions': questions,
        }
        return render(request, 'stud_app/exam.html', context)