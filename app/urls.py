from django.urls import path
from .views import *


urlpatterns = [
    path('product/products/', RetrieveProductsViews.as_view()),
    path('product/<int:id>/', get_one_request),
    # path('product/create_product/', CreateProductGenericView.as_view()),
    path('product/update_product/<int:id>/', UpdatePartialProductView.as_view()),
    
    
    path('product/logs/<int:id>/', get_one_log_details),
    path('product/logs/', RetrieveAllLogsViews.as_view()),
    path('product/order_status/', RetrieveOrderStatus.as_view()),
    path('product/min_threshold/', GetMinThresholdViews.as_view()),
    path('product/purchase/', PurchaseItemsViews.as_view()),
    path('product/verify_purchase', VerifyPurchaseOTPViews.as_view()),
    
    path('supplier/<int:id>/', get_one_supplier),
    path('supplier/suppliers/', RetrieveSuppliersViews.as_view()),
    path('supplier/delete/', delete),
    
    
    path('order/orders/', OrderNewStocks.as_view()),
    path('order/orders/<int:id>/', get_one_order),
    
    path('order/verify_order/', VerifyOrderOTPViews.as_view())
]