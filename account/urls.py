from django.urls import path

from . import views

urlpatterns = [
    path("login/",views.LoginView.as_view()),
    path("who/",views.WhoAmIView.as_view()),
    path("studentinfo/create",views.StudentInfoCreateApiView.as_view()),

]

