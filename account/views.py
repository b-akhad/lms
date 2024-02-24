from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated


from . import serializers
from lms.authenticate import CustomAuthentication
from .models import StudentInfo



# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


class LoginView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)

                response.data = {"access_token": data["access_token"]}

                return response
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid username or password!!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []

    authentication_classes = [CustomAuthentication]
    serializers = serializers.UserSerializer

    def get(self, format=None):
        serializer = serializers.UserSerializer(self.request.user)
        return Response(serializer.data)


class StudentInfoCreateApiView(generics.CreateAPIView):
    queryset = StudentInfo.objects.all()
    serializer_class = serializers.StudentInfoCreateSerializer


class StudentInfoApiView(APIView):
    def get(self,request):
        user = request.user
        student_info = StudentInfo.objects.get(student=user)
        info_serializer = serializers.StudentInfoCreateSerializer(student_info)

        data = info_serializer.data
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name

        return Response(data, status=status.HTTP_200_OK)


