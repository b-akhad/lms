
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# from lesson.models import Group


class Group(models.Model):
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "group"
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name


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
    group = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True)

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


class StudentInfo(models.Model):
    male = "male"
    female = "female"
    GENDER_CHOICE = (
        (male,"Male"),
        (female,"Female")
    )
    gender = models.CharField(max_length=100,null=True,blank=True,choices=GENDER_CHOICE)
    dob = models.DateField(null=True,blank=True)
    nationality = models.CharField(max_length=100,null=True,blank=True)
    birth_place = models.CharField(max_length=100,null=True,blank=True)
    living_place = models.CharField(max_length=100,null=True,blank=True)
    citizenship = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=30,null=True,blank=True)
    home_phone = models.CharField(max_length=30,null=True,blank=True)
    student = models.OneToOneField(CustomUser,null=True,blank=True,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="photo/")

    class Meta:
        db_table = "student_info"
        verbose_name = "Student Information"
        verbose_name_plural = "Students Information"


