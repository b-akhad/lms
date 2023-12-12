from rest_framework import serializers
from .models import CustomUser, StudentInfo


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password',"role",
                  'first_name', 'last_name', 'is_active']


class StudentsBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name']


class StudentInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = '__all__'

