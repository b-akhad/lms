from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 'teacher')


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 'student')


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 'admin')



