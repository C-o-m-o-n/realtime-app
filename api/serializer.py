from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.password_validation import validate_password
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import School, MyUser, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# deactivate user
class UserActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('is_active',)

# logout user
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


#Registering a user
class UserSerializer(ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
   
    class Meta:
        model = MyUser
        fields = ('id', 'uuid','email', 'firstname', 'lastname','phone_number', 'is_active', 'user_level','avatar', 'school', 'address', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'uuid': {'read_only': True},
        }
   

    def save(self):
        user = MyUser(
            email=self.validated_data['email'], 
            firstname=self.validated_data['firstname'],
            lastname=self.validated_data['lastname'],
            user_level=self.validated_data['user_level'],
            phone_number=self.validated_data['phone_number'],
            address=self.validated_data['address'],
            avatar=self.validated_data['avatar'],
            school=self.validated_data['school'],
            )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user
   
   

#logging user to get jwt token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # try:
        #     profile = Profile.objects.get(user=user)
        # except Profile.DoesNotExist:
        #     profile = None

        # Add custom claims
        token['uuid'] = user.uuid
        token['email'] = str(user.email)
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['user_level'] = user.user_level
        token['phone_number'] = user.phone_number
        token['avatar'] = str(user.avatar)
        token['school'] = str(user.school)
        token['address'] = str(user.address)

        
        return token


class SchoolSerializer(ModelSerializer):
   
    class Meta:
        model = School
        fields = ['id', 'uuid','name','address','logo','sector','phone_number', 'location', 'email', 'description']
        extra_kwargs = {
            'uuid': {'read_only': True}
        }