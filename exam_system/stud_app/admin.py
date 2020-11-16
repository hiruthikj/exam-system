from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import * 
from .forms import Group, GroupAdminForm
from django import forms

admin.site.site_header = 'Exam administration'

import csv
from django.http import HttpResponse
# import xlwt

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export as CSV"

# class ExportExcelMixin:
#     def export_as_xls(self, request, queryset):

#         meta = self.model._meta

#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename={}'.format(meta)

#         wb = xlwt.Workbook(encoding='utf-8')
#         ws = wb.add_sheet(str(meta))

#         # Sheet header, first row
#         row_num = 0

#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True

#         field_names = [field.name for field in meta.fields]

#         for col_num in range(len(field_names)):
#             ws.write(row_num, col_num, field_names[col_num], font_style)

#         # Sheet body, remaining rows
#         font_style = xlwt.XFStyle()

#         # for obj in queryset:
#         #     row = writer.writerow([getattr(obj, field) for field in field_names])

#         for obj in queryset:
#             row_num += 1
#             row = [getattr(obj, field) for field in field_names]
#             for col_num in range(len(row)):
#                 ws.write(row_num, col_num, row[col_num], font_style)

#         # for row in rows:
#         #     row_num += 1
#         #     for col_num in range(len(row)):
#         #         ws.write(row_num, col_num, row[col_num], font_style)

#         wb.save(response)
#         return response

#     export_as_xls.short_description = "Export as Excel"

# import nested_admin


# class DepartmentInline(admin.TabularInline):
#     # extra = 0
#     model = Department

# class CourseAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Course Info',               {'fields': ['course_code','course_name', 'course_desc']}),
#         # ('Date information',            {'fields': []}),
#     ]
#     inlines = [DepartmentInline]
#     list_display = ['course_code', 'dept_fk']
#     search_fields = ['course_name']
#     list_filter = ['dept_fk']

class CourseInline(admin.TabularInline):
    extra = 0
    model = Course

class DepartmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Department Info',               {'fields': ['dept_code','dept_name']}),
        # ('Date information',            {'fields': []}),
    ]
    inlines = [CourseInline]
    list_display = ['dept_code', 'dept_name']
    search_fields = ['dept_name']
    list_filter = ['dept_code']

class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Login Info',         {'fields': ['user',]}),
        ('Academic Info',      {'fields': ['dept_fk','course_fk','joined_on']}),
        ('Personal Info',      {'fields': ['phone_no','birth_date',]}),
    ]
    # inlines = [UserInline]
    list_display = ['user','dept_fk', 'joined_on']   #course fk
    # list_filter = ['user.username']
    
    # search_fields = ['dept_fk']
    # readonly_fields = ('pub_date',)

class FacultyAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Login Info',         {'fields': ['user',]}),
        ('Academic Info',      {'fields': ['dept_fk','course_fk','joined_on',]}),
        ('Personal Info',      {'fields': ['phone_no']}),
    ]
    # inlines = [UserInline]
    list_display = ['user','dept_fk', 'joined_on']   #course fk
    # list_filter = ['user.username']
    
    # search_fields = ['dept_fk']
    # readonly_fields = ('pub_date',)


class StudentInline(admin.StackedInline):
    model = Student

    class Meta:
        readonly_fields = ('date_joined','last_login')

class CustomUserAdmin(UserAdmin):

    inlines = (StudentInline, )

    # list_display = ['qn_text', 'pub_date', 'was_published_recently']   #course fk
    # list_filter = ['get_username()']
    
    # search_fields = ['username']
    # readonly_fields = ('pub_date',)
    
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ['is_selected',]

    # def validate_unique(self):
    #     #super(Choice, self).validate_unique(exclude=exclude)
    #     sol_exists = False
    #     question = self.cleaned_data['question']
    #     for choice in question.choice_set.all():
    #         if choice.cleaned_data['is_correct']:
    #              sol_exists = True
    #     if not sol_exists:
    #         raise forms.ValidationError("Enter the correct solution")

    #     return self.cleaned_data

class ChoiceInline(admin.TabularInline):
    extra = 0
    model = Choice
    form = ChoiceForm

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Exam Info',         {'fields': ['exams']}),
        ('Question Info',       {'fields': ['qn_text','pub_date','qn_image',]}),
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

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def clean_qn_mark(self):
        self.cleaned_data['qn_mark'] =  int(self.cleaned_data.get('qn_mark'))
        if self.cleaned_data.get('qn_mark') <= 0:
            raise forms.ValidationError("Enter valid marks for right answer!")
        return self.cleaned_data['qn_mark']

    def clean_neg_mark(self):
        self.cleaned_data['neg_mark'] =  int(self.cleaned_data.get('neg_mark'))
        if self.cleaned_data.get('neg_mark') <= 0:
            raise forms.ValidationError("Enter valid marks for wrong answer!")
        return self.cleaned_data['neg_mark']

    def clean(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("Dates are incorrect!")
        return self.cleaned_data

class ExamAdmin(admin.ModelAdmin):
    form = ExamForm
    fieldsets = [
        ('Exam Info',                 {'fields': ['exam_name', 'course_fk','is_active']}),
        ('Mark Scheme',                 {'fields': ['qn_mark', 'neg_mark']}),
        ('Other Info',               {'fields': ['start_time','end_time','time_limit',]}),
        ('Stats',                   {'fields': ['created_on','updated_on',]}),
        
    ]
    # inlines = [CourseInline]
    list_display = ['exam_name','course_fk', 'is_active']
    search_fields = ['exam_name']

    readonly_fields = ('pub_date','created_on','updated_on',)

class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )



class AttendeeAdmin(admin.ModelAdmin, ExportCsvMixin):
    fieldsets = [
        ('Attendee Info',         {'fields': ['student_fk', 'exam_fk']}),
        ('Exam Info',           {'fields': ['total_marks','submitted_on',]}),
    ]
    list_display = ['exam_fk', 'student_fk', 'total_marks']   #course fk
    list_filter = ['submitted_on']
    search_fields = ['exam_fk']
    readonly_fields = ('student_fk', 'exam_fk','submitted_on',)

    actions = ["export_as_csv",]   #"export_as_xls",
 

########################################################################
# Register your models here.

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)

admin.site.register(Department,DepartmentAdmin)
# admin.site.register(Course,CourseAdmin)

admin.site.register(Question, QuestionAdmin)
# admin.site.register(QuestionBank, QuestionBankAdmin)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Response)
admin.site.register(Attendee, AttendeeAdmin)  

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)