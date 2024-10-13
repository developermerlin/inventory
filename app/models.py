from django.db import models

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
    
