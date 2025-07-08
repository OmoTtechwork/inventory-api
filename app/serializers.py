from rest_framework import serializers
from .models import *






class ProductInventorySerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = ProductInventory
        fields = ['product_name', 'category', 'price', 'stock_amount', 'description', 'sku_id', 'company_min_stock']
        
        
class StockSuppliedSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = StockSupplied
        fields = ['item_name', 'serial_number', 'comments', 'quantity', 'category']
        

class SuppliersSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Suppliers
        fields = ['company_name', 'company_address', 'item_name', 'delivery_id', 'first_name', 'last_name', 'phone_number']
        
        
class OTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = OTP
        fields = ['otp', 'created_at']
        ref_name = 'NotificationOTPSerializer'
        


class ProductDetailedLogSerializers(serializers.ModelSerializer):
    
    class Meta:
        
        model = ProductDetailedLog
        fields = ['amount_purchased', 'amount_sold', 'stock_left', 'order_status', 'company_min_stock','top_product', 'stock_in_name', 'stock_out_name']  

        
class OrderSerializers(serializers.ModelSerializer):
    
    products= ProductInventorySerializer()
    stocks= StockSuppliedSerializer()
    suppliers= SuppliersSerializer()
    # otp = OTPSerializer()
    
    class Meta:
        model = OrderModel
        fields = ['products', 'stocks', 'suppliers']
    
    def create(self, validated_data, **kwargs):
        
        user = self.context['request'].user
        
        product_data = validated_data.pop('products')
        stock_data = validated_data.pop('stocks')
        suppliers_data = validated_data.pop('suppliers')
        # otp_data = validated_data.pop('otp')
        
        product_instance = ProductInventory.objects.create(user=user, **product_data)
        stock_instance = StockSupplied.objects.create(user=user,product=product_instance, **stock_data)
        supplier_instance = Suppliers.objects.create(user=user, **suppliers_data)
        # otp_instance = OTP.objects.create(**otp_data)
        
        order = OrderModel.objects.create(
            products=product_instance,
            stocks=stock_instance,
            suppliers=supplier_instance,
            user=user,
            **kwargs
            # otp=otp_instance
        )
        
        return order
    
   
class PurchasedItemsSerializers(serializers.ModelSerializer):
    
    product_name = serializers.CharField(write_only=True)
     
    class Meta:
         
         model = PurchasedItems
         fields = ['buyer_name', 'items_amount', 'category', 'items', 'product_name']
         read_only_fields = ['items']
         
    def create(self, validated_data, **kwargs):
        
        product_name = validated_data.pop("product_name")
        
        try:
            product = ProductInventory.objects.get(product_name=product_name)
        except ProductInventory.DoesNotExist:
            raise serializers.ValidationError({'product_name': 'Product not found.'})
        
        validated_data['product_name'] = product.product_name
        validated_data['items'] = product
        validated_data['category'] = product.category
        
        return super().create(validated_data)
        
         