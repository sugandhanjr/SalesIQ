import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsales.settings')
django.setup()

from core.models import Product, SalesData
from django.contrib.auth.models import User

def populate():
    # Create test user if not exists
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "password123")
        print("Created superuser admin/password123")

    if not User.objects.filter(username="testuser").exists():
        User.objects.create_user("testuser", "test@example.com", "password123")
        print("Created business user testuser/password123")

    # Clear old data
    Product.objects.all().delete()
    SalesData.objects.all().delete()

    products_data = [
        {"name": "Wireless Earbuds", "category": "Electronics", "price": 2499},
        {"name": "Smart Watch", "category": "Electronics", "price": 3999},
        {"name": "Bluetooth Speaker", "category": "Electronics", "price": 1899},
        {"name": "Laptop Backpack", "category": "Accessories", "price": 1299},
        {"name": "Fitness Band", "category": "Electronics", "price": 2199},
        {"name": "USB-C Charger", "category": "Electronics", "price": 799},
        {"name": "Gaming Mouse", "category": "Electronics", "price": 1599},
        {"name": "LED Desk Lamp", "category": "Home Office", "price": 1099},
        {"name": "Phone Stand", "category": "Accessories", "price": 399},
        {"name": "Noise Cancelling Headphones", "category": "Electronics", "price": 5999},
    ]

    products = []
    for p in products_data:
        product = Product.objects.create(name=p["name"], category=p["category"], price=p["price"])
        products.append(product)
    
    print(f"Created {len(products)} products.")

    # Generate 60 days of historical sales data
    today = timezone.now().date()
    sales_to_create = []

    for i in range(60):
        sale_date = today - timedelta(days=60-i)
        
        # Determine number of sales for this day (simulate a slight upward trend)
        base_sales = 5 + int(i / 10)
        daily_transactions = random.randint(base_sales, base_sales + 5)
        
        for _ in range(daily_transactions):
            product = random.choice(products)
            qty = random.randint(1, 4)
            # Maybe a slight discount sometimes
            actual_price = float(product.price) * random.choice([1.0, 1.0, 1.0, 0.9])
            
            sales_to_create.append(SalesData(
                product=product,
                quantity=qty,
                sale_price=actual_price,
                total_revenue=qty * actual_price,
                sale_date=sale_date
            ))

    SalesData.objects.bulk_create(sales_to_create)
    print(f"Created {len(sales_to_create)} historical sales records.")

if __name__ == '__main__':
    populate()
