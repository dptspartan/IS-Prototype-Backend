from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'order': {'required': False}  # ✅ Let DRF know it's handled manually
        }
        

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            # Create OrderItem
            OrderItem.objects.create(order=order, **item_data)

            # Deduct product stock
            product.quantity_in_stock -= quantity
            product.save()

            # Create Inventory Transaction
            InventoryTransaction.objects.create(
                product=product,
                change_type=InventoryTransaction.OUT,
                quantity_changed=quantity,
                note=f"Order #{order.pk} — Stock OUT"
            )

        return order
