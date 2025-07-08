from django.db import models
import string
import random
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.db.models import Sum

# Create your models here.

User = get_user_model()



class Utils(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        abstract = True       

class StockUtils(models.Model):
    
    class CategoryShuffle(models.TextChoices):
        PHONE = 'Mobile Phone'
        LAPTOP = 'Laptop'
        PERISHABLE = 'Perishable'
        NONPERISHABLE = 'Non-perishable'
        NATIVE_WEARS = 'Native Wears'
        FOREIGN_WEARS =  'Foreign Wears'

    category = models.CharField(max_length=50, choices=CategoryShuffle.choices, null=True, blank=True)
        
    class Meta:
        abstract = True




class OTP(models.Model):
      
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_user', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    
    def is_otp_valid(self):
        
        return bool(self.expiry_date > timezone.now())


class ProductInventory(Utils):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_product')
    product_name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    stock_amount = models.IntegerField()
    description = models.TextField()
    sku_id = models.UUIDField(default=uuid.uuid4, unique=True)
    company_min_stock = models.BooleanField(default=True)
    
    def hit_threshold_min(self):
        
        if self.stock_amount <= 3:
            
            self.company_min_stock = True
            self.save()
     
    def generate_skuID(self, length=6):
        
        value = string.ascii_lowercase + string.digits
        random_value = ''.join(random.choices(value, length))
        
        self.sku_id = random_value
        self.save()

    def __str__(self):
        return f'{self.product_name} has {self.stock_amount} available in stock'
    

class PurchasedItems(Utils, StockUtils):
    
    items = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, null=True, blank=True)
    buyer_name = models.CharField(max_length=200)
    items_amount = models.IntegerField()
    product_name = models.CharField(max_length=50)
    top_product = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_purchase')
    otp = models.ForeignKey(OTP, on_delete=models.SET_NULL, null=True, blank=True)
    sales_status = models.CharField(max_length=200, default='No purchase yet')
    # product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    
    def get_highest_product(self):
        
        top_product = PurchasedItems.objects.filter(category=self.category).values('items').annotate(total_sold=Sum('items_amount')).order_by('-total_sold').first()
        
        if top_product:
            self.top_product= {
                'product_name':self.product_name,
                'item_amount': self.items_amount,
                'total_sold': top_product['total_sold']
                }
            
            self.save()
    
    def increase_item_amount(self):
        
        self.items_amount += 1
        self.save()
    
   
    
class StockSupplied(Utils, StockUtils):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50)
    comments = models.TextField(blank=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    otp = models.ForeignKey(OTP, on_delete=models.SET_NULL, null=True, blank=True)
    

class Suppliers(Utils):
    
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplier_user')
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=300)
    item_name = models.CharField()
    delivery_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    stock = models.ForeignKey(StockSupplied, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    
    def __str__(self):
        return f'{self.company_name} has the current time available {self.stock.item_name}'
    


class OrderModel(Utils):
    
    products = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    stocks = models.ForeignKey(StockSupplied, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=50, default='No order yet')
    otp = models.ForeignKey(OTP, on_delete=models.SET_NULL, null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_expiry_date(self):
        
        expiry_date = self.otp.expiry_date
        self.expiry_date = expiry_date
        
        self.save()
            
    def __str__(self):
        return f'orders delivered by {self.suppliers.first_name} from {self.suppliers.company_name} has been updated by {User.full_name}'
   
    
    
class ProductDetailedLog(Utils):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_log', null=True, blank=True)
    product= models.ForeignKey(ProductInventory, on_delete=models.CASCADE, null=True, blank=True)
    stock_in = models.ForeignKey(StockSupplied, on_delete=models.CASCADE, null=True, blank=True)
    stock_out = models.ForeignKey(PurchasedItems, on_delete=models.CASCADE, null=True, blank=True)
    amount_purchased = models.IntegerField(null=True, blank=True)
    amount_sold = models.IntegerField(null=True, blank=True)
    stock_left = models.IntegerField(null=True, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.CharField(max_length=50, null=True, blank=True)
    company_min_stock = models.BooleanField(default=False, null=True, blank=True)
    stock_min_threshold = models.IntegerField(null=True, blank=True)
    stock_in_name = models.CharField(max_length=50, null=True, blank=True)
    stock_out_name = models.CharField(max_length=50, null=True, blank=True)
    # sale_ratio = models.CharField(max_length=100)
    top_product= models.JSONField(null=True, blank=True)
    
    def update_log_item(self):
        if self.stock_in:
            self.amount_purchased = self.stock_in.quantity
            self.stock_in_name = self.stock_in.item_name
            self.save()

        if self.stock_out:
            self.amount_sold = self.stock_out.items_amount
            self.top_product = self.stock_out.top_product
            self.stock_out_name = self.stock_out.product_name
            self.save()

        if self.amount_purchased is not None and self.amount_sold is not None:
            self.stock_left = self.amount_purchased - self.amount_sold
            self.save()
        else:
            self.stock_left = None

        if self.order:
            self.order_status = self.order.order_status
            self.save()

        if self.product:
            self.company_min_stock = self.product.company_min_stock
            self.save()

        self.stock_min_threshold = ProductDetailedLog.objects.filter(company_min_stock=True).count()
        self.save()

        

        
        
 
  