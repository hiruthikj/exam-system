from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

import datetime
from django.utils import timezone
from durationwidget.widgets import TimeDurationWidget
# from django.utils.html import mark_safe
# from .thumbs import ImageWithThumbsField

class Department(models.Model):
    dept_code = models.CharField(max_length=3, unique=True)
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name

class Course(models.Model):
    course_code = models.CharField(max_length=6, unique=True)
    course_name = models.CharField(max_length=50)
    dept_fk = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    #dept_fk = models.ManyToManyField(Department, on_delete=models.SET_NULL)
    course_desc = models.TextField('Course Description',max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.course_name

class Student(models.Model):
    user = models.OneToOneField(User, related_name='usserrr', on_delete=models.CASCADE, unique=True)
    course_fk = models.ManyToManyField(Course)  
    dept_fk = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True, unique=True, help_text='10-digit phone number') 

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"

    def get_name(self):
        return (self.user.first_name, self.user.last_name)
    
    def get_username(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('stud_app:home', kwargs={'username': self.get_username()})

    class Meta:
        ordering = ['dept_fk__dept_name']


# def create_profile(sender,**kwargs):
#     if kwargs['created']:
#         user_profile=Student.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile,sender=User)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Student.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Exam(models.Model):
    exam_name = models.CharField(max_length=40)
    course_fk = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE, null=True, blank=True)
    # question_fk = models.ManyToManyField('Question')

    is_active = models.BooleanField(default=True)
    time_limit = models.DurationField(help_text='In what UNITS???') #widget=TimeDurationWidget(), required=False, 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField('Date Published', auto_now_add=True, editable=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.short_description = 'Recently Published?'
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

    def __str__(self):
        return self.exam_name

class QuestionTag(models.Model):
    tag_name = models.TextField(max_length=20, unique=True)

    def __str__(self):
        return self.tag_name

class Question(models.Model):
    qn_text = models.TextField('Question Description',max_length=200)
    qn_image = models.ImageField('Question Image', null=True, blank=True)
    qn_tag = models.ForeignKey('QuestionTag', verbose_name='Tag', on_delete=models.CASCADE, null=True, blank=True)
    exams = models.ManyToManyField('Exam')
    course_fk = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, editable=False)
    # qn_image = ImageWithThumbsField('Question Image', upload_to='img/', sizes=((125,125),(300,200)))
    # correct_choice = models.ForeignKey(Choice)

    def __str__(self):
        return self.qn_text[:10]

    # def image_tag(self):
    #     from django.utils.html import escape
    #     return u'<img src="%s" />' % escape(self.qn_image)
    # image_tag.short_description = 'Image'
    # image_tag.allow_tags = True

    # def image_img(self):
    #     if self.image:
    #         return mark_safe('<img src="%s" />' % self.qn_image.url_125x125)
    #     else:
    #         return '(No image)'
    # image_img.short_description = 'Thumb'

    # def image_tag(self):
    #         return mark_safe('<img src="%s" width="150" height="150" alt="Question Image">' % (self.qn_image))

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.short_description = 'Recently Published?'
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_selected = models.BooleanField('Correct Answer', default=False, null=True, blank=True)
    is_correct = models.BooleanField('Correct Answer', default=False)

    def __str__(self):
        return self.choice_text


class Attendee(models.Model):
    exam_fk = models.ForeignKey('Exam', on_delete=models.CASCADE)
    student_fk = models.ForeignKey('Student', on_delete=models.CASCADE)
    total_marks = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{exam_fk.exam_name} : {student_fk.get_name()}'

class Response(models.Model):
    list_fk = models.ForeignKey('Attendee', on_delete=models.CASCADE)
    # question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)

    def __str__(self):
        return self.student_fk.user.username