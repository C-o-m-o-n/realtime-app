import os
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnDiscPlaceholderImage

# Getting the Custom User
User = settings.AUTH_USER_MODEL

class School(models.Model):
    SECTOR_TYPE = [
        ('public', 'public'),
        ('private', 'private'),
    ]

    uuid = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    logo = VersatileImageField( upload_to='school', ppoi_field='avatar_ppoi')
    avatar_ppoi = PPOIField()
    sector = models.CharField(max_length=10, choices=SECTOR_TYPE, default='private')
    description = models.TextField()

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=self.normalize_phone_number(phone_number), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)
    
    def normalize_phone_number(self, phone_number):
        return phone_number.strip().replace('-', '')

class MyUser(AbstractBaseUser):
    USER_LEVEL_TYPE = [
        ('0', 'super admin'),
        ('1', 'school admin'),
        ('2', 'teacher'),
        ('3', 'parent'),
    ]

    uuid = models.CharField(unique=True, default=uuid.uuid4, max_length=100)
    email = models.EmailField(verbose_name='email address', max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=12, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_level = models.CharField(max_length=25 ,choices=USER_LEVEL_TYPE)
    school = models.ForeignKey(School, related_name='schoolprofile', on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatars', null=True, blank=True)
    address = models.CharField(max_length=12, null=True, blank=True)
    

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['firstname','lastname', 'email', 'user_level']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Student(models.Model):
    gender_choice = [
        ('Male','male'),
        ('Female', 'female')
    ]
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, max_length=100)
    parent = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default='')
    admission_number = models.CharField(unique=True, max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(choices=gender_choice, max_length=6)
    physical_disability = models.CharField(max_length=100)
    year_joined = models.IntegerField()
    date_of_birth = models.DateField()
    avatar = models.ImageField(upload_to='student_avatars', null=True, blank=True)
    address = models.CharField(max_length=12, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    


    
