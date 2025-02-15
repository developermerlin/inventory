from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('clerk/', views.clerk, name='clerk'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('category/', views.category, name='category'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    
    
    path('product/', views.product, name='product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('view_product/<int:product_id>/', views.view_product, name='view_product'),
    
    
    path('customer/', views.customer, name='customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    
    
    path('supplier/', views.supplier, name='supplier'),
    path('edit_supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),

    path('purchase/', views.purchase, name='purchase'),
    path('edit_purchase/<int:purchase_id>/', views.edit_purchase, name='edit_purchase'),
    path('delete_purchase/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
    # path('view_product/<int:product_id>/', views.view_product, name='view_product'),
    
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    # path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    # path('view_product/<int:product_id>/', views.view_product, name='view_product'),
    path("add_to_temp_cart/", views.add_to_temp_cart, name="add_to_temp_cart"),
    path("transfer_to_final_cart/", views.transfer_to_final_cart, name="transfer_to_final_cart"),

    path("final_cart/", views.final_cart, name="final_cart"),
    # path('receipt/<uuid:session_id>/', views.receipt_detail, name='receipt_detail'),  # New URL pattern
    path('receipt_detail/<uuid:session_id>/',views.receipt_detail, name='receipt_detail'),

    path('report/', views.report, name='report'),
    path('sales-report-by-date/', views.sales_report_by_date, name='generate_sales_report_by_date'),
    path('total-sales-report/', views.total_sales_report, name='generate_total_sales_report'),

    path('chart-data/', views.chart_data, name='chart_data'),
]