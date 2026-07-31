import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_sales_dataset(num_records=10000):
    os.makedirs('dataset', exist_ok=True)
    
    # 1. Customer Pool (approx 1,200 unique customers to create repeat buyers & segments)
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
                   "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
                   "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra",
                   "Mark", "Ashley", "Paul", "Kimberly", "Steven", "Emily", "Andrew", "Donna", "Kenneth", "Michelle",
                   "Joshua", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa", "Edward", "Deborah"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                  "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                  "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]

    genders = ["Male", "Female"]
    
    customers = []
    for i in range(1, 1201):
        cust_id = f"CUST-{i:04d}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        name = f"{fn} {ln}"
        gender = random.choice(genders)
        age = random.randint(18, 70)
        customers.append({"Customer ID": cust_id, "Customer Name": name, "Gender": gender, "Age": age})
    
    # 2. Location Mapping
    locations = [
        {"City": "Los Angeles", "State": "California", "Region": "West"},
        {"City": "San Francisco", "State": "California", "Region": "West"},
        {"City": "Seattle", "State": "Washington", "Region": "West"},
        {"City": "San Diego", "State": "California", "Region": "West"},
        {"City": "Phoenix", "State": "Arizona", "Region": "West"},
        
        {"City": "New York City", "State": "New York", "Region": "East"},
        {"City": "Philadelphia", "State": "Pennsylvania", "Region": "East"},
        {"City": "Boston", "State": "Massachusetts", "Region": "East"},
        {"City": "Newark", "State": "New Jersey", "Region": "East"},
        {"City": "Pittsburgh", "State": "Pennsylvania", "Region": "East"},
        
        {"City": "Chicago", "State": "Illinois", "Region": "Central"},
        {"City": "Detroit", "State": "Michigan", "Region": "Central"},
        {"City": "Columbus", "State": "Ohio", "Region": "Central"},
        {"City": "Minneapolis", "State": "Minnesota", "Region": "Central"},
        {"City": "Dallas", "State": "Texas", "Region": "Central"},
        {"City": "Houston", "State": "Texas", "Region": "Central"},
        
        {"City": "Atlanta", "State": "Georgia", "Region": "South"},
        {"City": "Miami", "State": "Florida", "Region": "South"},
        {"City": "Charlotte", "State": "North Carolina", "Region": "South"},
        {"City": "Tampa", "State": "Florida", "Region": "South"},
        {"City": "Nashville", "State": "Tennessee", "Region": "South"}
    ]
    
    # 3. Product Catalog Definition
    products_catalog = [
        # Technology
        {"Product ID": "PROD-TEC-1001", "Category": "Technology", "Sub Category": "Laptops", "Product Name": "Dell XPS 15 Laptop", "Base Price": 1499.00, "Base Margin": 0.22},
        {"Product ID": "PROD-TEC-1002", "Category": "Technology", "Sub Category": "Laptops", "Product Name": "Apple MacBook Pro 16", "Base Price": 2399.00, "Base Margin": 0.25},
        {"Product ID": "PROD-TEC-1003", "Category": "Technology", "Sub Category": "Phones", "Product Name": "iPhone 15 Pro Max", "Base Price": 1199.00, "Base Margin": 0.20},
        {"Product ID": "PROD-TEC-1004", "Category": "Technology", "Sub Category": "Phones", "Product Name": "Samsung Galaxy S24 Ultra", "Base Price": 1299.00, "Base Margin": 0.18},
        {"Product ID": "PROD-TEC-1005", "Category": "Technology", "Sub Category": "Accessories", "Product Name": "Logitech MX Master 3S Mouse", "Base Price": 99.00, "Base Margin": 0.35},
        {"Product ID": "PROD-TEC-1006", "Category": "Technology", "Sub Category": "Accessories", "Product Name": "Anker USB-C Multiport Hub", "Base Price": 59.00, "Base Margin": 0.40},
        {"Product ID": "PROD-TEC-1007", "Category": "Technology", "Sub Category": "Copiers", "Product Name": "Canon ImageCLASS Laser Copier", "Base Price": 899.00, "Base Margin": 0.15},
        {"Product ID": "PROD-TEC-1008", "Category": "Technology", "Sub Category": "Machines", "Product Name": "Epson EcoTank Pro Printer", "Base Price": 649.00, "Base Margin": 0.12},
        
        # Furniture
        {"Product ID": "PROD-FUR-2001", "Category": "Furniture", "Sub Category": "Chairs", "Product Name": "Herman Miller Ergonomic Chair", "Base Price": 699.00, "Base Margin": 0.18},
        {"Product ID": "PROD-FUR-2002", "Category": "Furniture", "Sub Category": "Chairs", "Product Name": "Executive Leather Office Chair", "Base Price": 349.00, "Base Margin": 0.15},
        {"Product ID": "PROD-FUR-2003", "Category": "Furniture", "Sub Category": "Tables", "Product Name": "Standing Electric Desk 60x30", "Base Price": 549.00, "Base Margin": 0.08},
        {"Product ID": "PROD-FUR-2004", "Category": "Furniture", "Sub Category": "Tables", "Product Name": "Conference Wooden Table 8ft", "Base Price": 1199.00, "Base Margin": 0.05},
        {"Product ID": "PROD-FUR-2005", "Category": "Furniture", "Sub Category": "Bookcases", "Product Name": "5-Shelf Modular Bookcase", "Base Price": 229.00, "Base Margin": 0.10},
        {"Product ID": "PROD-FUR-2006", "Category": "Furniture", "Sub Category": "Furnishings", "Product Name": "LED Desk Lamp with Wireless Charging", "Base Price": 49.00, "Base Margin": 0.30},
        
        # Office Supplies
        {"Product ID": "PROD-OFF-3001", "Category": "Office Supplies", "Sub Category": "Paper", "Product Name": "Multipurpose Copy Paper Ream 500", "Base Price": 12.99, "Base Margin": 0.45},
        {"Product ID": "PROD-OFF-3002", "Category": "Office Supplies", "Sub Category": "Paper", "Product Name": "Premium Heavyweight Cardstock", "Base Price": 24.99, "Base Margin": 0.40},
        {"Product ID": "PROD-OFF-3003", "Category": "Office Supplies", "Sub Category": "Binders", "Product Name": "Heavy Duty 3-Ring Binder 2 inch", "Base Price": 15.49, "Base Margin": 0.38},
        {"Product ID": "PROD-OFF-3004", "Category": "Office Supplies", "Sub Category": "Storage", "Product Name": "Plastic Storage Tote Heavy Duty", "Base Price": 45.00, "Base Margin": 0.25},
        {"Product ID": "PROD-OFF-3005", "Category": "Office Supplies", "Sub Category": "Art", "Product Name": "Permanent Markers Pack of 24", "Base Price": 18.50, "Base Margin": 0.50},
        {"Product ID": "PROD-OFF-3006", "Category": "Office Supplies", "Sub Category": "Envelopes", "Product Name": "Self-Seal Security Envelopes #10", "Base Price": 14.00, "Base Margin": 0.42},
        {"Product ID": "PROD-OFF-3007", "Category": "Office Supplies", "Sub Category": "Fasteners", "Product Name": "Assorted Binder Clips & Paperclips Box", "Base Price": 8.99, "Base Margin": 0.48}
    ]

    payment_modes = ["Credit Card", "Debit Card", "PayPal", "UPI", "Net Banking"]
    payment_weights = [0.45, 0.20, 0.15, 0.12, 0.08]
    
    priorities = ["Low", "Medium", "High", "Critical"]
    priority_weights = [0.20, 0.50, 0.20, 0.10]

    discounts = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50]
    discount_weights = [0.35, 0.20, 0.15, 0.10, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01]

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range_days = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{random.randint(2023, 2025)}-{10000 + i}"
        
        # Date generation with Q4 seasonal boost
        day_offset = random.randint(0, date_range_days)
        order_date = start_date + timedelta(days=day_offset)
        # Seasonal weighting: increase probability of orders in Nov/Dec
        if order_date.month in [11, 12] and random.random() < 0.3:
            # duplicate month skew towards festive season
            pass
            
        ship_days = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[0.1, 0.25, 0.35, 0.15, 0.08, 0.04, 0.03])[0]
        ship_date = order_date + timedelta(days=ship_days)
        
        customer = random.choice(customers)
        location = random.choice(locations)
        prod = random.choice(products_catalog)
        
        quantity = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], weights=[0.30, 0.25, 0.20, 0.10, 0.05, 0.04, 0.03, 0.01, 0.01, 0.01])[0]
        unit_price = prod["Base Price"]
        discount = random.choices(discounts, weights=discount_weights)[0]
        
        # Calculate Sales
        raw_sales = quantity * unit_price
        sales = round(raw_sales * (1.0 - discount), 2)
        
        # Profit logic: Base Profit - Discount erosion - Shipping overhead impact
        # Heavy discounts (>30%) heavily erode profits, especially for Furniture (Tables, Bookcases)
        base_profit = sales * prod["Base Margin"]
        discount_penalty = raw_sales * (discount * 1.2)  # Extra margin hit for high discounts
        
        shipping_cost = round(sales * random.uniform(0.03, 0.07) + random.uniform(3.0, 12.0), 2)
        
        profit = round(base_profit - (discount_penalty * 0.5) - (shipping_cost * 0.15), 2)
        
        # Force specific realistic business edge case: Furniture with >20% discount often has negative profit
        if prod["Category"] == "Furniture" and discount >= 0.20:
            profit = round(-1 * abs(sales * random.uniform(0.05, 0.22)), 2)
        elif discount >= 0.35:
            profit = round(-1 * abs(sales * random.uniform(0.02, 0.15)), 2)
            
        payment_mode = random.choices(payment_modes, weights=payment_weights)[0]
        priority = random.choices(priorities, weights=priority_weights)[0]
        
        record = {
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Ship Date": ship_date.strftime("%Y-%m-%d"),
            "Customer ID": customer["Customer ID"],
            "Customer Name": customer["Customer Name"],
            "Gender": customer["Gender"],
            "Age": customer["Age"],
            "City": location["City"],
            "State": location["State"],
            "Region": location["Region"],
            "Product ID": prod["Product ID"],
            "Product Category": prod["Category"],
            "Sub Category": prod["Sub Category"],
            "Product Name": prod["Product Name"],
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Discount": discount,
            "Sales": sales,
            "Profit": profit,
            "Shipping Cost": shipping_cost,
            "Payment Mode": payment_mode,
            "Order Priority": priority
        }
        records.append(record)
        
    df = pd.DataFrame(records)
    # Sort chronologically by Order Date
    df = df.sort_values(by="Order Date").reset_index(drop=True)
    
    file_path = os.path.join("dataset", "sales_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Successfully generated dataset with {len(df)} records at {file_path}")
    print("Dataset Summary Head:")
    print(df.head(3))
    return df

if __name__ == "__main__":
    generate_sales_dataset(10000)
