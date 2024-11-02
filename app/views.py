
from django.shortcuts import render, redirect # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from .models import Category, Product, Customer, Supplier, Purchase,TemporaryCart, FinalCart
from django.contrib import messages # type: ignore
from datetime import datetime
from decimal import Decimal
from collections import defaultdict
import uuid
from django.db.models import Sum # type: ignore
from django.utils.dateparse import parse_date # type: ignore
from datetime import datetime, timedelta
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


# add products
def purchase(request):
    if request.method == 'POST':
        # Extracting form data
        product_name = request.POST.get('product_name')
        supplier_id = request.POST.get('supplier')
        quantity = request.POST.get('quantity')
        product_price = request.POST.get('product_price')
        product_cost = request.POST.get('product_cost')
        date_order = request.POST.get('date_order')
        delivery_date = request.POST.get('delivery_date')
        status = request.POST.get('status')  # Either 'Pending' or 'Received'

        # Getting the supplier object
        product_supplier = get_object_or_404(Supplier, id=supplier_id)

        # Create the Purchase object
        purchase_entry = Purchase(
            product_supplier=product_supplier,
            product_name=product_name,
            quantity=quantity,
            product_price=product_price,
            product_cost=product_cost,
            date_order=datetime.strptime(date_order, '%Y-%m-%d').date(), 
            delivery_date=datetime.strptime(delivery_date, '%Y-%m-%d').date(),  
            status=status
        )
        purchase_entry.save()

        messages.success(request, "Purchase record added successfully!")
        return redirect('purchase') 

    # GET request: render the form
    suppliers = Supplier.objects.all()
    purchases = Purchase.objects.all()  # Fetch all purchase entries
    return render(request, 'purchase.html', {'suppliers': suppliers, 'purchases':purchases})



def edit_purchase(request, purchase_id):
    purchase_entry = get_object_or_404(Purchase, id=purchase_id)
    purchase = Purchase.objects.all()

    if request.method == 'POST':
        # Extract updated form data
        product_name = request.POST.get('product_name')
        supplier_id = request.POST.get('supplier')
        quantity = request.POST.get('quantity')
        product_price = request.POST.get('product_price')
        date_order = request.POST.get('date_order')
        delivery_date = request.POST.get('delivery_date')
        status = request.POST.get('status')

        # Get the updated supplier object
        product_supplier = get_object_or_404(Supplier, id=supplier_id)

        # Update the fields of the purchase_entry
        purchase_entry.product_supplier = product_supplier
        purchase_entry.product_name = product_name
        purchase_entry.quantity = int(quantity)  # Ensure quantity is an integer
        purchase_entry.product_price = Decimal(product_price)  # Ensure price is Decimal
        purchase_entry.date_order = datetime.strptime(date_order, '%Y-%m-%d').date()
        purchase_entry.delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
        purchase_entry.status = status

        # The product_cost will be automatically updated in the model's save method
        purchase_entry.save()

        messages.success(request, "Purchase record updated successfully!")
        return redirect('purchase')  

    # GET request: Prepopulate the form with existing data
    suppliers = Supplier.objects.all()
    return render(request, 'edit_purchase.html', {
        'purchase_entry': purchase_entry, 
        'suppliers': suppliers,
        'purchase':purchase
    })


def delete_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.delete()
        messages.success(request, "Purchase Order deleted successfully!")
        return redirect('purchase')
    return render(request, 'delete_purchase.html')










def add_to_temp_cart(request):
    products = Product.objects.all()
    temp_cart_items = TemporaryCart.objects.all()  # Fetch all items in the temporary cart
    total_cost = sum(item.total_price for item in temp_cart_items)  # Calculate total cost

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")

        if product_id and quantity:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)  # Ensure quantity is an integer

            # Check if enough stock is available
            if quantity > product.in_stock:
                messages.error(request, f"Not enough stock available for {product.product_name}. Current stock: {product.in_stock}.")
            else:
                # Create a new TemporaryCart item
                temp_cart_item = TemporaryCart(
                    product=product,
                    quantity=quantity  # Set the entered quantity
                )
                temp_cart_item.save()  # This sets the unit_price and total_price automatically

                # Reduce the product's stock
                product.in_stock -= quantity  # Deduct the entered quantity
                product.save()  # Save the updated product instance

                messages.success(request, f"{quantity} units of {product.product_name} added to cart successfully!")

                # Redirect to a success page or back to the form
                return redirect("add_to_temp_cart")  # Change to your desired URL

    return render(request, "add_to_temp_cart.html", {
        "products": products,
        "temp_cart_items": temp_cart_items,
        "total_cost": total_cost,  # Pass total cost to the template
    })







def transfer_to_final_cart(request):
    if request.method == 'POST':
        temp_cart_items = TemporaryCart.objects.all()  # Fetch all items from temporary cart

        # Generate a unique transfer session ID for this batch of transfers
        session_id = uuid.uuid4()

        for item in temp_cart_items:
            # Create a new FinalCart item for each temporary cart item, including the transfer session ID
            final_cart_item = FinalCart(
                product=item.product,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,  # Ensure total_price is set correctly
                transfer_session_id=session_id  # Assign the session ID to each item in this transfer batch
            )
            final_cart_item.save()  # Save the final cart item to the database

            # Reduce the stock of the product
            item.product.in_stock -= item.quantity
            item.product.save()  # Save the updated product

        # Clear the temporary cart after transfer
        TemporaryCart.objects.all().delete()

        return redirect('final_cart')  # Redirect to the final cart view

    return render(request, 'transfer_to_final_cart.html')  # For GET request



def final_cart(request):
    # Group items by transfer_session_id
    final_cart_items = FinalCart.objects.all().order_by('-date_added')
    grouped_cart_items = defaultdict(list)

    for item in final_cart_items:
        # Group items by transfer_session_id
        grouped_cart_items[item.transfer_session_id].append(item)

    # Prepare the context with grouped items and their subtotals
    context = {
        'grouped_cart_items': [],
    }

    # Calculate subtotal for each transfer session and prepare context
    for session_id, items in grouped_cart_items.items():
        subtotal = sum(item.total_price for item in items)
        context['grouped_cart_items'].append({
            'session_id': session_id,
            'items': items,
            'subtotal': subtotal,
        })

    return render(request, 'final_cart.html', context)




def receipt_detail(request, session_id):
    # Retrieve all items for the given transfer session ID
    items = FinalCart.objects.filter(transfer_session_id=session_id)

    # Check if there are any items
    if not items.exists():
        return render(request, 'receipt_detail.html', {'error': 'No items found for this session.'})

    # Calculate subtotal
    subtotal = sum(item.total_price for item in items)

    # Prepare context with items and subtotal
    context = {
        'items': items,
        'session_id': session_id,
        'subtotal': subtotal,
    }

    return render(request, 'receipt_detail.html', context)

# def receipt_detail(request):
#     return render(request, 'receipt_detail.html')


def report(request):

    return render(request, 'report.html')




def sales_report_by_date(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        # Parse the start and end dates exactly as provided
        start_date = parse_date(start_date)
        end_date = parse_date(end_date) + timedelta(days=1)  # Extend end_date by one day

        # Filter FinalCart entries with date_added from start_date up to (but not including) the next day after end_date
        sales_data = FinalCart.objects.filter(date_added__gte=start_date, date_added__lt=end_date)

        # Calculate the total sales amount
        total_sales = sales_data.aggregate(Sum('total_price'))['total_price__sum'] or 0
    else:
        # No date range provided, set empty data and total sales as 0
        sales_data = []
        total_sales = 0

    # Pass data to the template
    context = {
        'sales_data': sales_data,
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': end_date - timedelta(days=1),  # Revert end_date for display in the template
    }
    return render(request, 'sales_report_by_date.html', context)


def total_sales_report(request):
    # Query all FinalCart entries to get total sales
    sales_data = FinalCart.objects.all()

    # Aggregate the total sales based on the total_price field
    total_sales = sales_data.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Pass data to the template
    context = {
        'sales_data': sales_data,
        'total_sales': total_sales,
    }
    return render(request, 'total_sales_report.html', context)
