from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'



class OTPSerializer(serializers.Serializer):
    
    otp = serializers.CharField(max_length=6)
    
    class Meta:
        
        ref_name = 'AccountOTPSerializer'
    

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)