from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'transactions', InventoryTransactionViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Make sure this comes before the default router URLs to avoid overriding
    path('orders/<int:pk>/dispatch/', OrderViewSet.as_view({'patch': 'dispatch'}), name='order-dispatch'),
    
    # Include router's URLs after
    path('', include(router.urls)),

    # Other custom URLs
    path('alerts/low-stock/', LowStockAlertView.as_view()),
    path('reports/summary/', StockSummaryReportView.as_view()),
]
