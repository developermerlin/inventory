
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Category, Product, Customer, Supplier
from django.contrib import messages
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')



# Add Category
def category(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        category = Category(
            category_name=category_name,
            category_description=category_description
        )

        category.save()
        messages.success(request, "Category information saved successfully!")
        return redirect('category')
    return render(request, 'category.html',{'categories':categories})


# Edit Category
def edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        category.category_name = category_name
        category.category_description = category_description

        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect('category')
    return render(request, 'edit_category.html', {'category': category})



# Delete Category
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('category')
    return render(request, 'delete_category.html', {'category': category})


# add products
def product(request):
    if request.method == 'POST':
        # Extracting form data
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier')
        in_stock = request.POST.get('stock_number')
        buying_price = request.POST.get('buying_price')
        selling_price = request.POST.get('selling_price')
        added_date = request.POST.get('added_date')
        profile = request.FILES.get('file')

        product_category = Category.objects.get(id=category_id)
        product_supplier = get_object_or_404(Supplier, id=supplier_id)

        product = Product(
            product_name=product_name,
            product_category=product_category,
            product_supplier=product_supplier,
            in_stock=in_stock,
            buying_price=buying_price,
            selling_price=selling_price,
            added_date=datetime.strptime(added_date, '%Y-%m-%d').date(), 
            profile=profile
        )
        product.save()

        messages.success(request, "Product added successfully!")
        return redirect('product')
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    products = Product.objects.all()
    return render(request, 'product.html', {'categories': categories,'products':products,'suppliers':suppliers})


# edit product
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier')
        in_stock = request.POST.get('stock_number')
        buying_price = request.POST.get('buying_price')
        selling_price = request.POST.get('selling_price')
        added_date = request.POST.get('added_date')
        profile = request.FILES.get('file') if 'file' in request.FILES else product.profile


        product_category = Category.objects.get(id=category_id)
        product_supplier = Supplier.objects.get(id=supplier_id)
        product.product_name = product_name
        product.product_category = product_category
        product.product_supplier = product_supplier
        product.in_stock = in_stock
        product.buying_price = buying_price
        product.selling_price = selling_price
        product.added_date = datetime.strptime(added_date, '%Y-%m-%d').date()  
        product.profile = profile
        product.save()

        messages.success(request, "Product updated successfully!")
        return redirect('product')
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    formatted_date = product.added_date.strftime('%Y-%m-%d') if product.added_date else ''
    return render(request, 'edit_product.html', {'product': product, 'categories': categories,'suppliers': suppliers,'formatted_date':formatted_date})


def delete_product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product')
    return render(request, 'delete_product.html')


def view_product(request, product_id):
    # Get the product using its ID or return a 404 error if not found
    product = Product.objects.get(id=product_id)
    return render(request, 'view_product.html', {
        'product': product,
    })
    
    
# Add customer
def customer(request):
    if request.method == 'POST':
        # Extracting form data
        customer_name = request.POST.get('customer_name')
        customer_address = request.POST.get('customer_address')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        profile = request.FILES.get('file')


        customer = Customer(
            customer_name=customer_name,
            customer_address=customer_address,
            customer_email=customer_email,
            customer_phone=customer_phone,
            profile=profile
        )
        customer.save()
        messages.success(request, "Customer added successfully!")
        return redirect('customer')
    customers = Customer.objects.all()
    return render(request, 'customer.html', {'customers':customers})



# edit product
def edit_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_address = request.POST.get('customer_address')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email')
        
        profile = request.FILES.get('file') if 'file' in request.FILES else customer.profile

        customer.customer_name = customer_name
        customer.customer_email = customer_email
        customer.customer_address = customer_address
        customer.customer_phone = customer_phone
        customer.profile = profile
        customer.save()
        messages.success(request, "Customer updated successfully!")
        return redirect('customer')
   
    return render(request, 'edit_customer.html', {'customer': customer})


def delete_customer(request, customer_id):
    if request.method == 'POST':
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(request, "Customer deleted successfully!")
        return redirect('customer')
    return render(request, 'delete_customer.html')



# Add customer
def supplier(request):
    if request.method == 'POST':
        # Extracting form data
        supplier_name = request.POST.get('supplier_name')
        supplier_address = request.POST.get('supplier_address')
        supplier_email = request.POST.get('supplier_email')
        supplier_phone = request.POST.get('supplier_phone')
        profile = request.FILES.get('file')


        supplier = Supplier(
            supplier_name=supplier_name,
            supplier_address=supplier_address,
            supplier_email=supplier_email,
            supplier_phone=supplier_phone,
            profile=profile
        )
        supplier.save()
        messages.success(request, "Supplier added successfully!")
        return redirect('supplier')
    suppliers = Supplier.objects.all()
    return render(request, 'supplier.html', {'suppliers':suppliers})



# edit product
def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name')
        supplier_address = request.POST.get('supplier_address')
        supplier_phone = request.POST.get('supplier_phone')
        supplier_email = request.POST.get('supplier_email')
        
        profile = request.FILES.get('file') if 'file' in request.FILES else supplier.profile

        supplier.supplier_name = supplier_name
        supplier.supplier_email = supplier_email
        supplier.supplier_address = supplier_address
        supplier.supplier_phone = supplier_phone
        supplier.profile = profile
        supplier.save()
        messages.success(request, "Supplier updated successfully!")
        return redirect('supplier')
   
    return render(request, 'edit_supplier.html', {'supplier': supplier})


def delete_supplier(request, supplier_id):
    if request.method == 'POST':
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        messages.success(request, "Supplier deleted successfully!")
        return redirect('supplier')
    return render(request, 'delete_supplier.html')
