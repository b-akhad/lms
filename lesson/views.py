import datetime

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Schedule, Attendance, StudentScores,Subject
from account.permissions import IsTeacher,IsStudent
from account.models import Group

from . import serializers

# Create your views here.


class TeacherLessonsApiView(ListAPIView):
    serializer_class = serializers.TeacherLessonsListSerializer
    permission_classes = [IsAuthenticated,IsTeacher]

    def get_queryset(self):
        date = self.request.query_params.get("date")
        user = self.request.user

        if date:
            date = datetime.datetime.strptime(date,"%Y-%m-%d")
            teacher_lessons = Schedule.objects.filter(teacher=user, start__date=date.date())
        else:
            teacher_lessons = Schedule.objects.filter(teacher=user)

        return teacher_lessons


class TeacherTodaysLessonsApiView(ListAPIView):
    serializer_class = serializers.TeacherLessonsListSerializer
    permission_classes = [IsAuthenticated,IsTeacher]

    def get_queryset(self):
        user = self.request.user
        today = datetime.datetime.today()
        teacher_todays_lessons = Schedule.objects.filter(teacher=user,start__date=today.date())
        return teacher_todays_lessons


class StudentLessonsListApiView(ListAPIView):
    serializer_class = serializers.StudentLessonsListSerializer
    permission_classes = [IsAuthenticated,IsStudent]

    def get_queryset(self):
        date = self.request.query_params.get("date")
        user = self.request.user
        if user.group:
            student_group_id = user.group.id
        else:
            return []

        if date:
            date = datetime.datetime.strptime(date,"%Y-%m-%d")
            student_lessons = Schedule.objects.filter(group_id=student_group_id,start__date=date.date())
        else:
            student_lessons = Schedule.objects.filter(group_id=student_group_id)

        return student_lessons



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class StudentTodaysLessonsListApiView(ListAPIView):
    serializer_class = serializers.StudentLessonsListSerializer
    permission_classes = [IsAuthenticated,IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.group:
            student_group_id = user.group.id
        else:
            return []

        today = datetime.datetime.today()
        student_lessons = Schedule.objects.filter(group_id=student_group_id,start__date=today.date())

        return student_lessons


class StudentAttendanceCreateApiView(APIView):
    def post(self,request):
        serialized = serializers.AttendanceStudentCreateSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=201)
        return Response({"error":serialized.errors})


class StudentAttendanceListApiView(ListAPIView):
    serializer_class = serializers.AttendanceStudentCreateSerializer

    def get_queryset(self):
        schedule = Schedule.objects.get(pk=self.kwargs['pk'])
        return Attendance.objects.filter(schedule=schedule)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class StudentAttendanceUpdateApiView(APIView):
    permission_classes = [IsAuthenticated,IsTeacher]
    def put(self,request,pk):
        # schedule = Schedule.objects.get(pk=pk)
        attendance = Attendance.objects.get(pk=pk)
        serialized = serializers.AttendanceStudentUpdateSerializer(instance=attendance,data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response({"error":serialized.errors})


class StudentScoreCreateApiView(APIView):
    permission_classes = [IsAuthenticated,IsTeacher]

    def post(self,request):
        serialized = serializers.ScoreStudentCreateSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response({"error":serialized.errors})


class StudentSubjectsListApiView(ListAPIView):
    permission_classes = [IsAuthenticated,IsStudent]
    serializer_class = serializers.SubjectsListSerializer

    def get_queryset(self):
        user = self.request.user
        subjects = Subject.objects.filter(groups=user.group)
        return subjects