from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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
    course_desc = models.TextField('Course Description')
    
    # class Meta:
    #     ordering = ['course_code']

    def __str__(self):
        return self.course_name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #firstname, lastname, username, password, email
    course_fk = models.ManyToManyField(Course)  #, on_delete=models.CASCADE)
    dept_fk = models.ForeignKey(Department, on_delete=models.CASCADE,null=False)
    phone = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.course_name

def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=Student.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)