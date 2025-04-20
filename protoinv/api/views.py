from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



# Custom reporting and alert views
from rest_framework.views import APIView

class LowStockAlertView(APIView):
    def get(self, request):
        low_stock_products = Product.objects.filter(quantity_in_stock__lte=F('reorder_level'))
        serializer = ProductSerializer(low_stock_products, many=True)
        return Response(serializer.data)


class StockSummaryReportView(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        low_stock = Product.objects.filter(quantity_in_stock__lte=F('reorder_level')).count()
        stock_value = Product.objects.aggregate(value=Sum(F('quantity_in_stock') * F('cost_price')))['value'] or 0
        return Response({
            'total_products': total_products,
            'low_stock_products': low_stock,
            'total_stock_value': stock_value,
        })

