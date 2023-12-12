
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.models import Group
from .models import StudentInfo


# admin.site.unregister(Group)
Group._meta.verbose_name = 'Rol'
Group._meta.verbose_name_plural = 'Rollar'


class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_active','is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    # fields = '__all__'
    # list_filter = ['role']
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','first_name', 'last_name','role','group')}),
        ("Ruxsatlar", {'fields': ( 'is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = None
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password_2',
                       'is_staff', 'role','group','is_active', 'groups', 'user_permissions')
            }
         ),
    )


# class GroupAdmin(admin.ModelAdmin):
#     list_display = ['name']

from .models import Group

admin.site.register(User, UserAdmin)
admin.site.register(Group)


@admin.register(StudentInfo)
class StAdmin(admin.ModelAdmin):
    list_display = ['student','gender','dob','photo']

