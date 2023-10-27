
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    admin = 'admin'
    teacher = 'teacher'
    student = "student"
    CHOICES = (
        (admin,'Admin'),
        (teacher, "Teacher"),
        (student, "Student"),

    )
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=200,choices=CHOICES,null=True,blank=True)
    position = models.CharField(max_length=70,null=True,blank=True)
    phone = models.CharField(max_length=25,null=True,blank=True)

    def save(self, *args, **kwargs):
        try:
            if kwargs['password']:
                self.set_password(kwargs['password'])
        except Exception:
            pass
        finally:
            super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        db_table = 'account'
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

