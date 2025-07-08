from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from .models import *
from rest_framework.viewsets import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import logging

# Create your views here.

User = get_user_model()


class RetrieveProductsViews(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(methods=['GET'])
    @action(detail=True, methods=['GET'])
    def get_all(self, request):
        
        if not request.user.is_authenticated:
            
            return HttpResponseForbidden('Request Invalid')
        
        products = ProductInventory.objects.all()
        
        serializer = ProductInventorySerializer(products, many=True)
        
        return Response(serializer.data, status=200)



@swagger_auto_schema(methods=['GET'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@action(detail=True, methods=['GET'])
def get_one_request(request, id):
    
    if not request.user.is_authenticated:
            
        return HttpResponseForbidden('Request Invalid')
    
    try:
        product = ProductInventory.objects.get(id=id)
        
    except:
        return HttpResponseBadRequest('Product with ID does not exist')
    
    serializer = ProductInventorySerializer(product)
    
    return Response(serializer.data, status=200)
    


class CreateProductGenericView(generics.CreateAPIView):
    
    authentication_classes = [JWTAuthentication]
    queryset = ProductInventory.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=ProductInventorySerializer)
    @action(detail=True, methods=['POST'])    
    def post(self, request, *args, **kwargs):
        
        serializer= ProductInventorySerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
        
        
class UpdatePartialProductView(generics.UpdateAPIView):
    
    authentication_classes = [JWTAuthentication]
    queryset = ProductInventory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductInventorySerializer
    
    @swagger_auto_schema(methods=['PUT'], request_body=ProductInventorySerializer)
    @action(detail=True, methods=['PUT'])
    def put(self, request, *args, **kwargs):
        
        serializer = ProductInventorySerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    

@swagger_auto_schema(methods=['DELETE'], request_body=SuppliersSerializer)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@action(detail=True, methods=['DELETE'])
def delete(request):
    
    delete_supplier = Suppliers.objects.get('id')
    
    delete_supplier.delete()
    
    return Response(f'user with {delete_supplier} does not exist')




class OrderNewStocks(APIView):
    
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]
    
    @swagger_auto_schema(methods=['POST'], request_body=OrderSerializers)
    @action(detail=True, methods=["POST"])
    def post(self, request, *args, **kwargs):
        
        order_serializer = OrderSerializers(data=request.data, context={'request': request})
        order_serializer.is_valid(raise_exception=True)
        
        order = order_serializer.save(order_status='Pending Verification to Complete Order')
        
        response_serializer = OrderSerializers(order)
        
        return Response(response_serializer.data, status=201)
    
        
class VerifyOrderOTPViews(APIView):
    
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]
           
    @swagger_auto_schema(methods=['POST'], request_body=OTPSerializer)
    @action(detail=True, methods=["POST"])
    def post(self, request):
            
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        otp = serializer.validated_data['otp']
            
        if not OTP.objects.filter(otp=otp).exists():
                
            return Response({"error": "otp is not found or has expired"}, status=404)
            
        get_otp = OTP.objects.get(otp=otp)
            
        order = OrderModel.objects.get(otp=get_otp, order_status='Pending Verification to Complete Order')
            
        if get_otp.is_otp_valid():
                
            order.order_status = 'Order Completed'
            order.save()
                
            get_otp.delete()
                
            return Response({'message': 'Order has been completed'})
            
        else:
            get_otp.delete()
                
            order.order_status = 'Order cancelled'
            order.save()
                
            return Response({'error': 'OTP expired'})
        
    
    
@swagger_auto_schema(methods=['GET'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@action(detail=True, methods=['GET'])
def get_one_order(request, id):

    if not request.user.is_authenticated:
            
        return HttpResponseForbidden('Request forbidden')
    
    try:
        order = OrderModel.objects.get(id=id)
        
    except:
        return HttpResponseBadRequest('Product with ID does not exist')
    
    serializer = OrderSerializers(order)
    
    return Response(serializer.data, status=200)        


@swagger_auto_schema(methods=['GET'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@action(detail=True, methods=['GET'])
def get_one_supplier(request, id):
    
    if not request.user.is_authenticated:
            
        return HttpResponseForbidden('Request forbidden')
    
    try:
        supplier = Suppliers.objects.get(id=id)
        
    except:
        return HttpResponseBadRequest('Product with ID does not exist')
    
    serializer = SuppliersSerializer(supplier)
    
    return Response(serializer.data, status=200) 



class RetrieveSuppliersViews(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(methods=['GET'])
    @action(detail=True, methods=['GET'])
    def get_all(self, request):
        
        if not request.user.is_authenticated:
            
            return HttpResponseForbidden('Request forbidden')
        
        products = Suppliers.objects.all()
        
        serializer = SuppliersSerializer(products, many=True)
        
        return Response(serializer.data, status=200)
    
 

@swagger_auto_schema(methods=['GET'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@action(detail=True, methods=['GET'])
def get_one_log_details(request, id):
    
    if not request.user.is_authenticated:
            
        return HttpResponseForbidden('Request forbidden') 
    
    try:
        log_details = ProductDetailedLog.objects.get(id=id)
        
    except:
        return HttpResponseBadRequest('Product with ID does not exist')
    
    serializer = ProductDetailedLogSerializers(log_details)
    
    return Response(serializer.data, status=200) 



class RetrieveAllLogsViews(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(methods=['GET'])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        
        if not request.user.is_authenticated:
            
            return HttpResponseForbidden('Request Invalid')
        
        log_details = ProductDetailedLog.objects.all()
        
        serializer = ProductDetailedLogSerializers(log_details, many=True)
        
        return Response(serializer.data, status=200)



class RetrieveOrderStatus(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(methods=['GET'])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        
        if not request.user.is_authenticated:
            
            return HttpResponseForbidden('Request forbidden')
        try:
            status_order = request.GET.get('order_status')
            
        except:
            return Response({'pick_an_instruction':{
                'first_instruction':'Order Completed',
                'second_instruction': 'Order cancelled'
                }
            })
            
        serializer = ProductDetailedLogSerializers(status_order)
        
        return Response(serializer.data, status=200)
    
    
class GetMinThresholdViews(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
      
    @swagger_auto_schema(methods=['GET'])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        
        if not request.user.is_authenticated:
            
            return HttpResponseForbidden('Request forbidden')
        try:
            company_min_stock = request.GET.get('company_min_stock')
            
        except:
            return HttpResponseBadRequest('Invalid Input')
            
        serializer = ProductDetailedLogSerializers(company_min_stock)
        
        return Response(serializer.data, status=200)
    

class VerifyPurchaseOTPViews(APIView):
    
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]
           
    @swagger_auto_schema(methods=['POST'], request_body=OTPSerializer)
    @action(detail=True, methods=["POST"])
    def post(self, request):
            
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        otp = serializer.validated_data['otp']
            
        if not OTP.objects.filter(otp=otp).exists():
                
            return Response({"error": "otp is not found or has expired"}, status=404)
            
        get_otp = OTP.objects.get(otp=otp)
            
        order = PurchasedItems.objects.get(otp=get_otp, sales_status='Pending Verification to Complete Purchase')
            
        if get_otp.is_otp_valid():
                
            order.sales_status = 'Purchase Completed'
            order.save()
                
            get_otp.delete()
                
            return Response({'message': 'Order has been completed'})
            
        else:
            get_otp.delete()
                
            order.sales_status = 'Purchase cancelled'
            order.save()
                
            return Response({'error': 'OTP expired'})
        
    
class PurchaseItemsViews(APIView):
    
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]
    
    @swagger_auto_schema(methods=['POST'], request_body=PurchasedItemsSerializers)
    @action(detail=True, methods=["POST"])
    def post(self, request, *args, **kwargs):
        
        purchase_serializer = PurchasedItemsSerializers(data=request.data, context={'request': request})
        purchase_serializer.is_valid(raise_exception=True)
        
        purchase = purchase_serializer.save(sales_status='Pending Verification to Complete Order', user=request.user)
        
        response_serializer = PurchasedItemsSerializers(purchase)
        
        return Response(response_serializer.data, status=201)
    
        