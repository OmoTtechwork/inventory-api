from django.db.models import signals
from .models import *
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import requests
import random
from django.utils import timezone


User =get_user_model()


def generate_otp():
    
    random_number = random.randint(000000, 999999)
    return random_number


@receiver(signals.post_save, sender=OrderModel)
def receive_inventory_stock(sender, instance, created, **kwargs):
    
    user = instance.user
    
    if created:
        
        if user.is_active==True:
        
            products = instance.products
            stocks = instance.stocks
            
            otp = generate_otp()

            create_otp = OTP.objects.create(
                user=user,
                otp = otp,
                created_at=timezone.now(),
                expiry_date= timezone.now() + timezone.timedelta(minutes=5)
            )
            
            #ThIS UPDATES THE STOCK OTP FOREIGN KEY BEFORE 
            # ORDERMODEL IS CREATED 
            stocks.otp = create_otp
            stocks.save()
            
            instance.otp = create_otp
            
            instance.order_status = 'Pending Verification to Complete Order'
            
            instance.save()


            url = "https://api.useplunk.com/v1/track"
            header = {
                "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
                "Content-Type": "application/json"
            }

        data = {
                "email": products.user.email,
                "event" : "Restock_order",
                "data" : {
                        'product_name': products.product_name,
                        'verification_otp': str(otp),
                        'category': stocks.category,
                        'stock_amount': str(stocks.quantity),
                        'order_status': instance.order_status
                        
                }
            }
                
        response = requests.post(
            url = url,
            headers = header,
            json = data
        )

        print(response.json())



@receiver(signals.post_save, sender=OrderModel)
def receive_completed_order(sender, instance, created, **kwargs):
    
    if instance.order_status=='Order Completed':
        
        user = instance.stocks.user
        
        if user.is_active==True:
            
            log, created = ProductDetailedLog.objects.update_or_create(
                                        user = user,
                                        order=instance,
                                        stock_in=instance.stocks,
                                        product=instance.products,
                                        
                                        defaults={
                                            "order": instance,
                                            "stock_in": instance.stocks,
                                            "product": instance.products
                                            
                                        }
                                    )
                                        
        
            log.update_log_item()
                
            url = "https://api.useplunk.com/v1/track"
            header = {
                "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
                "Content-Type": "application/json"
            }

        data = {
                "email": user.email,
                "event" : "Completed_Order",
                "data" : {
                        'product_details': str(instance.products),
                        'order_status': instance.order_status,
                        'created_at': str(instance.created_at),
                        'category': instance.stocks.category
                    }
            }
            
        response = requests.post(url=url, headers=header, json=data)

        print(response.json())

            

@receiver(signals.post_save, sender=PurchasedItems)
def purchased_item_stock(sender, instance, created, **kwargs):
    
    if created and instance.items:
        
        product = instance.items
                
        if product.stock_amount >= instance.items_amount:

                product.stock_amount -= instance.items_amount
                product.save()
                    
        else:
            print('Item does not exist in stock')
            return         
                
        url = "https://api.useplunk.com/v1/track"
        header = {
            "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
            "Content-Type": "application/json"
        }

        data = {
                "email": instance.user.email,
                "event" : "New_Purchase",
                "data" : {
                        'product_name': instance.product_name,
                        'category': instance.category,
                        'stock_amount': instance.items_amount
                    }
            }
            
        response = requests.post(
            url = url,
            headers = header,
            json = data
        )

        print(response.json())
    



@receiver(signals.post_save, sender=ProductInventory)
def receive_order_below_threshold(sender, instance, created, **kwargs):
    
    if instance.company_min_stock==True:
        
        user = instance.user
        
        if user.is_active==True:
            
            stock = instance.stock_amount
                
            url = "https://api.useplunk.com/v1/track"
            header = {
                "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
                "Content-Type": "application/json"
            }

        data = {
                "email": instance.user.email,
                "event" : "Stock_Low_Alert",
                'product_details': instance.product_name,
                'product_category': instance.category,
                'Num_of_stock_avail': str(stock),
                'message': f'{instance.stock_amount} is below company stock limit and needs restock immediately'
                }
            
        response = requests.post(url=url, headers=header, json=data)

        print(response.json())


@receiver(signals.post_save, sender=PurchasedItems)
def receive_purchase_details(sender, instance, created, **kwargs):
    
    user = instance.user
    
    if created:
        
        if user.is_active==True:
            
            otp = generate_otp()

            products = instance.items

            create_otp = OTP.objects.create(
                user=user,
                otp = otp,
                created_at=timezone.now(),
                expiry_date= timezone.now() + timezone.timedelta(minutes=5)
            )
            
            create_otp.save()
            
            #ThIS UPDATES THE STOCK OTP FOREIGN KEY BEFORE 
            #ORDERMODEL IS CREATED 
            instance.otp = create_otp
            category = instance.items.category
            instance.sales_status = 'Pending Verification to Complete Purchase'
            
            instance.save()

            url = "https://api.useplunk.com/v1/track"
            header = {
                "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
                "Content-Type": "application/json"
            }

        data = {
                "email": instance.user.email,
                "event" : "Purchase_order",
                "data" : {
                        'product_name': str(products.product_name),
                        'verification_otp': str(otp),
                        'category': category,
                        'stock_amount': str(instance.items_amount),
                        'sales_status': instance.sales_status
                        
                }
            }
                
        response = requests.post(
            url = url,
            headers = header,
            json = data
        )

        print(response.json())



@receiver(signals.post_save, sender=PurchasedItems)
def receive_completed_purchase(sender, instance, created, **kwargs):
    
    if instance.sales_status=='Purchase Completed':
        
        user = instance.user
        
        if user.is_active==True:
        
            log, created = ProductDetailedLog.objects.update_or_create(
                                            user = user,
                                            stock_out = instance,

                                            defaults={
                                                    "stock_out": instance
                                                    }
                                                )
                                        
        
            log.update_log_item()         
                
            url = "https://api.useplunk.com/v1/track"
            header = {
                "Authorization": "Bearer sk_0f52dde771f2c82f1d2a18b3df531ff3364aa12f9d817362",
                "Content-Type": "application/json"
            }

        data = {
                "email": user.email,
                "event" : "Purchase_Completed",
                "data" : {
                        'product_details': str(instance.items),
                        'sales_status': instance.sales_status,
                        'created_at': str(instance.created_at),
                        'category': instance.category
                    }
            }
            
        response = requests.post(url=url, headers=header, json=data)

        print(response.json())


def update_product_logs(sender, instance, created, **kwargs):
    
    try:
        log = ProductDetailedLog.objects.get(stock_out=instance)
        log.update_log_item()
    except ProductDetailedLog.DoesNotExist:
        return      
        