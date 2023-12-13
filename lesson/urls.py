from django.urls import path, include

from . import views

urlpatterns = [
    path("teacher/",views.TeacherLessonsApiView.as_view()),
    path("teacher/today/",views.TeacherTodaysLessonsApiView.as_view()),

    path("student/",views.StudentLessonsListApiView.as_view()),
    path("student/today/",views.StudentTodaysLessonsListApiView.as_view()),

    path("student/attendance/<int:pk>", views.StudentAttendanceListApiView.as_view()),
    path('attendance/update/<int:pk>',views.StudentAttendanceUpdateApiView.as_view()),
    # path("student/attendance/create/",views.StudentAttendanceCreateApiView.as_view()),

    path("score/create/",views.StudentScoreCreateApiView.as_view()),

    path("student/subjects/",views.StudentSubjectsListApiView.as_view())

]

