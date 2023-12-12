from django.contrib import admin
from .models import Subject, Schedule, Group, Attendance, StudentScores
from account.models import CustomUser
# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at")
    list_display = ['name',]



@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    exclude = ("created_at", "updated_at")
    list_display = ['group','subject','teacher','start','end']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs['queryset'] = CustomUser.objects.filter(role="teacher")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


#
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     exclude = ("created_at", "updated_at")
#     list_display = ['name',]
#

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['schedule','student','is_attended','created_at']


