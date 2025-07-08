from django.urls import path
from .views import *





urlpatterns = [
    path('user/', UserGenericView.as_view()),
    path('user/<int:pk>/', UserGenericByOne.as_view()),
    path('otp/', OTPVerifyView.as_view()),
    path('login/', LoginView.as_view()),
]