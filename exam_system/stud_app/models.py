from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import datetime
from django.utils import timezone

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


class QuestionBank(models.Model):
    course_fk = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Belongs to')

    def __str__(self):
        return self.course_fk.course_code

class Question(models.Model):
    qn_text = models.TextField('Question Description',max_length=200)
    qn_image = models.ImageField('Question Image')
    qn_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, verbose_name='IN QNbank')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

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

