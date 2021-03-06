from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

import datetime
from django.utils import timezone
# from durationwidget.widgets import TimeDurationWidget
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
    dept_fk = models.ForeignKey(Department, on_delete=models.PROTECT)
    #dept_fk = models.ManyToManyField(Department, on_delete=models.SET_NULL)
    course_desc = models.TextField('Course Description',max_length=300,null=True,blank=True)
    
    def __str__(self):
        return self.course_name

class Faculty(models.Model):
    user = models.OneToOneField(User, related_name='faculty_user', on_delete=models.CASCADE, unique=True)
    course_fk = models.ManyToManyField(Course)  
    dept_fk = models.ForeignKey('Department', on_delete=models.PROTECT)
    phone_no = models.CharField(max_length=10, unique=True, help_text='10-digit phone number')

    joined_on = models.DateField(null=True, blank=True)

    # def __str__(self):
    #     if len(self.get_name()) <= 1:
    #         return f"{self.user.username}"
    #     else:
    #         return f"{self.get_name()}"
    def __str__(self):
        return f"{self.user.username}"

    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def get_username(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse('stud_app:home', kwargs={'username': self.get_username()})

    class Meta:
        ordering = ['dept_fk__dept_name']

class Student(models.Model):
    user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE, unique=True)
    course_fk = models.ManyToManyField(Course)  
    dept_fk = models.ForeignKey('Department', on_delete=models.PROTECT)
    birth_date = models.DateField(null=True, blank=True)
    phone_no = models.CharField(max_length=10, unique=True, help_text='10-digit phone number')

    joined_on = models.DateField(null=True, blank=True)

    # def __str__(self):
    #     if len(self.get_name()) <= 1:
    #         return f"{self.user.username}"
    #     else:
    #         return f"{self.get_name()}"
    def __str__(self):
        return f"{self.user.username}"

    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
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
    exam_name = models.CharField(max_length=40, unique=True)
    course_fk = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE)
    # question_fk = models.ManyToManyField('Question')

    qn_mark = models.FloatField(default=4, null=True, blank=True)
    neg_mark = models.FloatField(default=1, null=True, blank=True)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_limit = models.DurationField(help_text='HH:MM:SS format') #widget=TimeDurationWidget(), required=False, 

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    pub_date = models.DateTimeField('Date Published', auto_now_add=True, editable=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.short_description = 'Recently Published?'
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

    def __str__(self):
        return self.exam_name

    class Meta:
        ordering = ['start_time',]

# class QuestionTag(models.Model):
#     tag_name = models.TextField(max_length=20, unique=True)

#     def __str__(self):
#         return self.tag_name

class Question(models.Model):
    qn_text = models.TextField('Question Description',max_length=200)
    qn_image = models.ImageField('Question Image', null=True, blank=True)
    # qn_tag = models.ForeignKey('QuestionTag', verbose_name='Tag', on_delete=models.CASCADE, null=True, blank=True)
    exams = models.ManyToManyField('Exam')
    # course_fk = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, editable=False)
    # qn_image = ImageWithThumbsField('Question Image', upload_to='img/', sizes=((125,125),(300,200)))
    # correct_choice = models.ForeignKey(Choice)

    def __str__(self):
        return self.qn_text[:70]

    # def validate_unique(self):
    #     sol_exists = False
    #     # question = self.cleaned_data['question']
    #     for choice in self.choice_set.all():
    #         if choice.is_correct:
    #              sol_exists = True
    #     if not sol_exists:
    #         raise forms.ValidationError("Enter the correct solution")
        
    #     super(Question, self).validate_unique(exclude=exclude)
    #     # return self.cleaned_data

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
    is_selected = models.BooleanField('Selected Answer', default=False, null=True, blank=True)
    is_correct = models.BooleanField('Correct Answer', default=False)


    def __str__(self):
        return self.choice_text


class Attendee(models.Model):
    exam_fk = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student_fk = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_marks = models.FloatField(null=True, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    # excel_file = models.FileField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f'{self.exam_fk.exam_name} - {self.student_fk.get_name()}'

    def recent(self):
        return self.exams_fk.start_time

class Response(models.Model):
    attendee_fk = models.ForeignKey('Attendee', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, blank=True, null=True)
    choice = models.ForeignKey('Choice', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.attendee_fk.exam_fk.exam_name} : {self.attendee_fk.student_fk.user.username}'

# class DownloadExcel(models.Model):
#     exam_fk = models.ForeignKey('Exam', on_delete=models.CASCADE)
#     excel_file = models.FileFieldPath()    