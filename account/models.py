
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
import random
from django.utils import timezone


# Create your models here.

# class User(AbstractUser):
    
#     bio = models.CharField(max_length=250)


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('app_admin', 'App Admin'),
        ('root_admin', 'Root Admin'),
        ('super_admin', 'Super Admin'),
        ('user', 'User'),


    )

    full_name = models.CharField(max_length=250)
    role = models.CharField(max_length = 225, choices=ROLE_CHOICES)
    email = models.CharField(max_length=300, unique=True)
    password = models.CharField(max_length=300)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    # otp_notification = models.CharField(max_length=6)
    # otp_created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']
    
    objects = UserManager()
    
    
    
    

class OTP(models.Model):
      
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    
    
    # def generate_otp(self, digit):
    #     digit = 6
    #     otp_code = ''.join(str(random.randint(0, 9)) for _ in range(digit))
    #     self.otp_notification = otp_code
    #     self.otp_created_at
    #     self.save()
        
    #     return otp_code
    
    def is_otp_valid(self):
        
        return bool(self.expiry_date > timezone.now())
            
            

