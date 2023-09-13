from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


from .serializer import SchoolSerializer, MyTokenObtainPairSerializer, UserSerializer, RefreshTokenSerializer, UserActiveSerializer, StudentSerializer
from .models import School, MyUser, Student


# Deactivate or Activate user
class UpdateActiveUserView(APIView):
    permission_classes =(IsAuthenticated,)
    
    def put(self, request, user_id):
        try:
            user = MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserActiveSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get and Post Students
class StudentView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get and Post a user
class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Edit and Delete User
class UserDetail(APIView):
    
    def get_object(self, id):
        try:
            user = MyUser.objects.get(id=id)
            return user
        
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request,id , format=None):
        user = self.get_object(id)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        

# generate token using simple-jwt
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
@api_view(['GET'])
def get_schools(request):
    schools = School.objects.all()
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data) 

# logout user jwt
class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
