from django.contrib import admin
import nested_admin
from .models import * #Department, Course, Student

# Register your models here.
class ChoiceInline(admin.TabularInline):
    extra = 4
    model = Choice

class QuestionAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Question Info',               {'fields': ['qn_text','pub_date']}),
        # ('Date information',            {'fields': []}),
    ]
    inlines = [ChoiceInline]
    list_display = ['qn_text', 'pub_date', 'was_published_recently']
    list_filter = ['pub_date']
    
    search_fields = ['qn_text']

class QuestionInline(admin.TabularInline):
    extra = 1
    model = Question

class QuestionBankAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Course Info',               {'fields': ['course_fk']}),
        # ('Date information',            {'fields': []}),
    ]
    inlines = [QuestionInline]
    # list_display = ['qn_text', 'pub_date', 'was_published_recently']
    # list_filter = ['pub_date']
    
    # search_fields = ['qn_text']

class CourseInline(admin.TabularInline):
    extra = 1
    model = Course

class DepartmentAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Department Info',               {'fields': ['dept_code','dept_name']}),
        # ('Date information',            {'fields': []}),
    ]
    inlines = [CourseInline]
    list_display = ['dept_code', 'dept_name']
    # list_filter = ['pub_date']
    
    search_fields = ['course_fk']

# Register your models here.
admin.site.register(Student)
admin.site.register(Department,DepartmentAdmin)

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionBank, QuestionBankAdmin)
