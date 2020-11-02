from django.contrib import admin
import nested_admin
from .models import * #Department, Course, Student

# Register your models here.
class ChoiceInline(nested_admin.NestedTabularInline):
    extra = 0
    model = Choice

class QuestionAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Course Info',         {'fields': ['course_fk', 'exams']}),
        ('Question Info',       {'fields': ['qn_text','pub_date','qn_image']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['qn_text', 'pub_date', 'was_published_recently']   #course fk
    list_filter = ['pub_date']
    
    search_fields = ['qn_text']
    readonly_fields = ('pub_date',)

# class QuestionInline(nested_admin.NestedTabularInline):
#     extra = 1
#     exclude = ['was_published_recently', ]
#     model = Question    
#     # sortable_field_name = 'was_published_recently'
#     inlines = [ChoiceInline]

# class QuestionBankAdmin(nested_admin.NestedModelAdmin):

#     fieldsets = [
#         ('Course Info',               {'fields': ['course_fk']}),
#         # ('Date information',            {'fields': []}),
#     ]
#     inlines = [QuestionInline]
#     # list_display = ['qn_text', 'pub_date', 'was_published_recently']
#     # list_filter = ['pub_date']
    
#     search_fields = ['qn_text']

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
    search_fields = ['course_fk']

class ExamAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Exam Info',               {'fields': ['course_fk','exam_name','time_limit','pub_date']}),
        # ('Questions',               {'fields': []}),
    ]
    # inlines = [CourseInline]
    # list_display = ['dept_code', 'dept_name']
    search_fields = ['exam_name']

    readonly_fields = ('pub_date',)

# Register your models here.
admin.site.register(Student)
admin.site.register(Department,DepartmentAdmin)

admin.site.register(Question, QuestionAdmin)
# admin.site.register(QuestionBank, QuestionBankAdmin)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Result)