from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
import requests
from django.utils import timezone
from .models import OTP
import random



def generate_otp():
    
    otp = random.randint(000000, 999999)
    
    return otp



User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        
        
        if instance.role in ('app_admin', 'root_admin', 'user'):
            
            instance.is_active = False
            instance.save()
            
            otp = generate_otp()
            print(otp)
            
            expiry_date = timezone.now() + timezone.timedelta(minutes=5)
            
            OTP.objects.create(
                otp = otp,
                expiry_date= expiry_date,
                user = instance
            )
            
            url = "https://api.useplunk.com/v1/track"
            header = {
                "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
                "Content-Type": "application/json"
            }

        data = {
                "email": instance.email,
                "event" : "welcome",
                "data" : {
                        "full_name": instance.full_name,
                        'otp': str(otp)
                    }
            }


        response = requests.post(
            url = url,
            headers = header,
            json = data
        )

        print(response.json())
    
    
    
        

