from django.db import models
from account.models import CustomUser, Group

from django.core.validators import MaxValueValidator
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subject"
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class Schedule(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    teacher = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schedule"
        verbose_name = "Schedule"
        verbose_name_plural = "Schedule"

    def __str__(self):
        return f"{self.group} {self.subject} {self.teacher}"


    def save(self, *args,**kwargs):
        is_exist = Schedule.objects.filter(pk=self.pk).exists()

        obj = super().save(*args, **kwargs)
        if is_exist:
            return obj

        students = CustomUser.objects.filter(group=self.group,role="student")
        for student in students:
            Attendance.objects.create(student=student,schedule=self,is_attended=False)
        return obj


class Attendance(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    is_attended = models.BooleanField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "attendance"
        verbose_name = 'Attendance'
        verbose_name_plural = "Attendance"


class StudentScores(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    score = models.SmallIntegerField(null=True,blank=True,validators=[MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_score"
        verbose_name = "Student score"
        verbose_name_plural = "Student Scores"

