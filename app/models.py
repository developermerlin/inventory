from django.db import models # type: ignore
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder # type: ignore
from django.db.models import JSONField # type: ignore
from django.utils import timezone # type: ignore
import uuid

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category_name
    
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    supplier_email = models.EmailField(max_length=50)
    supplier_address = models.CharField(max_length=100)
    supplier_phone = models.IntegerField()
    profile = models.ImageField(upload_to='supplier/', blank=True, null=True)  
    def __str__(self):
        return self.supplier_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    in_stock = models.IntegerField()  
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)  
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)  
    added_date = models.DateTimeField()  
    profile = models.ImageField(upload_to='products/', blank=True, null=True)  

    def __str__(self):
        return self.product_name
    
class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=50)
    customer_address = models.CharField(max_length=100)
    customer_phone = models.IntegerField()
    profile = models.ImageField(upload_to='customer/', blank=True, null=True)  
    
    def __str__(self):
        return self.customer_name
    


class Purchase(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('Pending', 'Pending'),
    ]
    product_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    date_order = models.DateTimeField()
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        self.product_price = Decimal(self.product_price)  
        self.quantity = int(self.quantity)  
        self.product_cost = self.product_price * self.quantity
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.product_name} - {self.status}"





class TemporaryCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)

    @property
    def total_price(self):
        """Calculates the total price based on quantity and unit price."""
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        """Sets the unit price based on the product's selling price when saving."""
        self.unit_price = self.product.selling_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} units at {self.unit_price} each (Total: {self.total_price})"





class FinalCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)
    transfer_session_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique ID for each transfer session

    def save(self, *args, **kwargs):
        self.unit_price = self.product.selling_price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} units at {self.unit_price} each"
