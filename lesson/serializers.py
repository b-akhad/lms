from rest_framework import serializers

import account.models
from .models import Schedule, Attendance, StudentScores

from account.models import StudentInfo


class TeacherLessonsListSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name',read_only=True)
    subject = serializers.SlugRelatedField(slug_field='name',read_only=True)

    class Meta:
        model = Schedule
        fields = ['id','group','subject','start','end']


class StudentLessonsListSerializer(TeacherLessonsListSerializer):
    teacher = serializers.SerializerMethodField()
    is_attended = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta(TeacherLessonsListSerializer.Meta):
        fields = TeacherLessonsListSerializer.Meta.fields + ['teacher','is_attended',"score"]

    def get_teacher(self,instance:Schedule):
        teacher = instance.teacher
        return teacher.first_name + " " + teacher.last_name

    def get_is_attended(self,instance:Schedule):
        student = self.context['request'].user
        try:
            attendance = Attendance.objects.get(student=student,schedule=instance)
        except Attendance.DoesNotExist:
            return False
        return attendance.is_attended

    def get_score(self,instance:Schedule):
        student = self.context['request'].user
        try:
            score = StudentScores.objects.get(student=student,schedule=instance)
        except StudentScores.DoesNotExist:
            return None
        return score.score


class AttendanceStudentCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields = ("id",'student','schedule','is_attended',"first_name",'last_name',"photo")

    def get_first_name(self,instance:Attendance):
        return instance.student.first_name

    def get_last_name(self,instance:Attendance):
        return instance.student.last_name

    def get_photo(self,instance:Attendance):
        student = instance.student
        try:
            info = StudentInfo.objects.get(student=student)
        except StudentInfo.DoesNotExist:
            return None
        return self.context['request'].build_absolute_uri(info.photo.url)







class AttendanceStudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id",'is_attended']


class ScoreStudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScores
        fields = ['id','student',"schedule",'score']




