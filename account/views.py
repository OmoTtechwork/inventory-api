from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponse
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


User = get_user_model()


class UserGenericView(generics.ListCreateAPIView):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    
    
    def create(self, request, *args, **kwargs):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        User.objects.create_user(
            **serializer._validated_data
        )
        
        return Response(serializer.data, status=201)
    
    
    def get(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            
            return Response({'error':'Authentication credentials not valid'})
        
        user= User.object.all()
        
        data = UserSerializer(user, many=True).data
        
        return Response(data, status=200)


class UserGenericByOne(generics.DestroyAPIView):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    
    

class OTPVerifyView(APIView):
    
    @swagger_auto_schema(methods=['POST'], request_body=OTPSerializer())
    @action(detail=True, methods=["POST"])
    def post(self, request):
        
        serializers = OTPSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        
        otp = serializers.validated_data["otp"]
        
        if not OTP.objects.filter(otp=otp).exists():
            
            return Response({"error": "otp is not found or has expired"}, status=404)
        
        otp = OTP.objects.get(otp=otp)
            
        if otp.is_otp_valid():
                
            otp.user.is_active = True
            otp.user.save()
                
                
            otp.delete()
                
            return Response({"message":"User successfully validated"})
            
            
        else:
                
            otp.delete()
                
            return Response({"error": "otp expired"}, status=400)
        
        
    
class LoginView(APIView):
    
    @swagger_auto_schema(methods=['POST'], request_body=LoginSerializer())
    @action(detail=True, methods=['POST'])
    
    def post(self, request):
        
        serializers=LoginSerializer(data= request.data)
        serializers.is_valid()
        
        user = authenticate(
            request, email= serializers.validated_data.get('email'),
            password = serializers.validated_data.get('password')
        )
        
        if user:
            
            token_data = RefreshToken.for_user(user)
            
            
            data = {
                'name': user.full_name,
                'role': user.role,
                'refresh': str(token_data),
                'access': str(token_data.access_token)
            }
            
            return Response(data, status=200)
        
        return Response({'error': 'Invalid credentials'}, status=400)
