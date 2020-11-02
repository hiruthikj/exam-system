from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import datetime
from django.utils import timezone
from django.utils.html import mark_safe

class Department(models.Model):
    dept_code = models.CharField(max_length=3)
    dept_name = models.CharField(max_length=50)

    # class Meta:
    #     ordering = ['dept_name', 'dept_code']

    def __str__(self):
        return self.dept_name

class Course(models.Model):
    course_code = models.CharField(max_length=6)
    course_name = models.CharField(max_length=50)
    dept_fk = models.ForeignKey(Department, on_delete=models.CASCADE)
    #dept_fk = models.ManyToManyField(Department, on_delete=models.SET_NULL)
    course_desc = models.TextField('Course Description',max_length=100)
    
    # class Meta:
    #     ordering = ['course_code']

    def __str__(self):
        return self.course_name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #firstname, lastname, username, password, email
    course_fk = models.ManyToManyField(Course)  #, on_delete=models.CASCADE)
    dept_fk = models.ForeignKey(Department, on_delete=models.CASCADE,null=False)
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + self.user.last_name

# def create_profile(sender,**kwargs):
#     if kwargs['created']:
#         user_profile=Student.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile,sender=User)


# class QuestionBank(models.Model):
#     question_fk = models.ForeignKey('Course', Course, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.course_fk.course_code

class Exam(models.Model):
    exam_name = models.CharField(max_length=40)
    course_fk = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE, null=True, blank=True)
    # question_fk = models.ManyToManyField(Question)

    time_limit = models.DurationField()
    pub_date = models.DateTimeField('Date Published', auto_now_add=True, editable=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.short_description = 'Recently Published?'
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

    def __str__(self):
        return self.exam_name


class Question(models.Model):
    qn_text = models.TextField('Question Description',max_length=200)
    qn_image = models.ImageField('Question Image', upload_to='img/')
    # qn_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, verbose_name='IN QNbank')
    exams = models.ManyToManyField(Exam)
    course_fk = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, editable=False)
    # correct_choice = models.ForeignKey(Choice)

    def __str__(self):
        return self.qn_text[:20]

    # def image_tag(self):
    #     from django.utils.html import escape
    #     return u'<img src="%s" />' % escape(<URL to the image>)
    # image_tag.short_description = 'Image'
    # image_tag.allow_tags = True

    def image_tag(self):
            return mark_safe('<img src="%s" width="150" height="150" alt="Question Image">' % (self.qn_image))

    image_tag.short_description = 'Image'

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.short_description = 'Recently Published?'
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField('Correct Answer', default=False)

    def __str__(self):
        return self.choice_text

class Result(models.Model):
    exam_fk = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student_fk = models.ForeignKey(Student, on_delete=models.CASCADE,null=True,blank=True)
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_fk.user.username

