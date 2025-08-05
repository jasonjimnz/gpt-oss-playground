import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()

def generate_banking_data(num_customers=2000, num_accounts=2500, num_transactions=5000):
    """
    Generates synthetic data for the banking service.

    Args:
        num_customers (int): The number of customers to generate.
        num_accounts (int): The number of bank accounts to generate.
        num_transactions (int): The number of transactions to generate.

    Returns:
        tuple: A tuple containing three pandas DataFrames:
               (bank_customers, bank_accounts, bank_transactions).
    """
    # Generate Customers
    customers_data = []
    for _ in range(num_customers):
        customers_data.append({
            'customer_id': fake.unique.random_number(digits=10),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.unique.email(),
            'phone_number': fake.phone_number(),
            'address_line1': fake.street_address().replace(',', ' '),
            'address_line2': fake.secondary_address().replace(',', ' '),
            'city': fake.city(),
            'state': fake.state(),
            'postal_code': fake.zipcode(),
            'country': fake.country(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=90),
            'gender': random.choice(['M', 'F', 'O']),
            'created_at': fake.date_time_this_decade()
        })
    bank_customers = pd.DataFrame(customers_data)

    # Generate Accounts
    accounts_data = []
    customer_ids = bank_customers['customer_id'].tolist()
    # Ensure each customer has at least one account
    for customer_id in customer_ids:
        accounts_data.append({
            'account_id': fake.unique.random_number(digits=12),
            'customer_id': customer_id,
            'account_type': random.choice(['CHECKING', 'SAVINGS', 'LOAN']),
            'balance': round(random.uniform(0, 100000), 2),
            'currency': 'USD',
            'status': random.choice(['ACTIVE', 'INACTIVE', 'CLOSED']),
            'opened_at': fake.date_time_this_decade(),
            'closed_at': None
        })
    
    # Add additional accounts if needed
    remaining_accounts = num_accounts - len(customer_ids)
    if remaining_accounts > 0:
        for _ in range(remaining_accounts):
            accounts_data.append({
                'account_id': fake.unique.random_number(digits=12),
                'customer_id': random.choice(customer_ids),
                'account_type': random.choice(['CHECKING', 'SAVINGS', 'LOAN']),
                'balance': round(random.uniform(0, 100000), 2),
                'currency': 'USD',
                'status': random.choice(['ACTIVE', 'INACTIVE', 'CLOSED']),
                'opened_at': fake.date_time_this_decade(),
                'closed_at': None
            })
    bank_accounts = pd.DataFrame(accounts_data)

    # Generate Transactions
    transactions_data = []
    account_ids = bank_accounts['account_id'].tolist()
    
    # Ensure each account has at least one transaction
    for account_id in account_ids:
        transactions_data.append({
            'transaction_id': fake.unique.random_number(digits=15),
            'account_id': account_id,
            'type': random.choice(['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']),
            'amount': round(random.uniform(10, 5000), 2),
            'currency': 'USD',
            'transaction_date': fake.date_time_between(start_date='-2y', end_date='now'),
            'description': fake.sentence()
        })
    
    # Add additional transactions if needed
    remaining_transactions = num_transactions - len(account_ids)
    if remaining_transactions > 0:
        for _ in range(remaining_transactions):
            transactions_data.append({
                'transaction_id': fake.unique.random_number(digits=15),
                'account_id': random.choice(account_ids),
                'type': random.choice(['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']),
                'amount': round(random.uniform(10, 5000), 2),
                'currency': 'USD',
                'transaction_date': fake.date_time_between(start_date='-2y', end_date='now'),
                'description': fake.sentence()
            })
    bank_transactions = pd.DataFrame(transactions_data)

    return bank_customers, bank_accounts, bank_transactions

def generate_ecommerce_data(num_customers=2500, num_products=750, num_orders=6000):
    """
    Generates synthetic data for the e-commerce service.

    Args:
        num_customers (int): The number of customers to generate.
        num_products (int): The number of products to generate.
        num_orders (int): The number of orders to generate.

    Returns:
        tuple: A tuple containing pandas DataFrames for the e-commerce schema.
    """
    # Generate Customers
    ecom_customers_data = []
    for _ in range(num_customers):
        ecom_customers_data.append({
            'customer_id': fake.unique.random_number(digits=10),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.unique.email(),
            'phone_number': fake.phone_number(),
            'created_at': fake.date_time_this_decade()
        })
    ecommerce_customers = pd.DataFrame(ecom_customers_data)

    # Generate Addresses
    addresses_data = []
    customer_ids = ecommerce_customers['customer_id'].tolist()
    # Create a mapping of customer_id to their addresses for later use
    customer_addresses = {}
    
    for i in range(num_customers):
        customer_id = customer_ids[i]
        customer_addresses[customer_id] = []
        
        for _ in range(random.randint(1, 3)):
            address_id = fake.unique.random_number(digits=12)
            addresses_data.append({
                'address_id': address_id,
                'customer_id': customer_id,
                'address_line1': fake.street_address().replace(',', ' '),
                'address_line2': fake.secondary_address().replace(',', ' '),
                'city': fake.city(),
                'state': fake.state(),
                'postal_code': fake.zipcode(),
                'country': fake.country()
            })
            customer_addresses[customer_id].append(address_id)
    ecommerce_addresses = pd.DataFrame(addresses_data)

    # Generate Product Categories
    categories = ['Electronics', 'Gaming', 'Computers', 'Accessories']
    product_categories_data = [{'category_id': i+1, 'name': cat, 'parent_category_id': None} for i, cat in enumerate(categories)]
    product_categories = pd.DataFrame(product_categories_data)

    # Generate Products
    products_data = []
    category_ids = product_categories['category_id'].tolist()
    
    # Create a mapping of category_id to products for later use
    category_products = {category_id: [] for category_id in category_ids}
    
    # Ensure each category has some products
    products_per_category = num_products // len(category_ids)
    remaining_products = num_products % len(category_ids)
    
    for category_id in category_ids:
        for _ in range(products_per_category):
            cost = round(random.uniform(10, 1000), 2)
            product_id = fake.unique.random_number(digits=8)
            products_data.append({
                'product_id': product_id,
                'sku': fake.unique.ean(length=13),
                'name': fake.bs(),
                'description': fake.text(),
                'category_id': category_id,
                'price': round(cost * random.uniform(1.2, 2.0), 2),
                'cost_price': cost,
                'weight_kg': round(random.uniform(0.1, 15), 3),
                'stock_quantity': random.randint(0, 200),
                'reorder_point': random.randint(10, 50),
                'discontinued': fake.boolean(chance_of_getting_true=10)
            })
            category_products[category_id].append(product_id)
    
    # Add remaining products randomly
    for _ in range(remaining_products):
        category_id = random.choice(category_ids)
        cost = round(random.uniform(10, 1000), 2)
        product_id = fake.unique.random_number(digits=8)
        products_data.append({
            'product_id': product_id,
            'sku': fake.unique.ean(length=13),
            'name': fake.bs(),
            'description': fake.text(),
            'category_id': category_id,
            'price': round(cost * random.uniform(1.2, 2.0), 2),
            'cost_price': cost,
            'weight_kg': round(random.uniform(0.1, 15), 3),
            'stock_quantity': random.randint(0, 200),
            'reorder_point': random.randint(10, 50),
            'discontinued': fake.boolean(chance_of_getting_true=10)
        })
        category_products[category_id].append(product_id)
    ecommerce_products = pd.DataFrame(products_data)

    # Generate Orders
    orders_data = []
    
    # Ensure each customer has at least one order
    for customer_id in customer_ids:
        # Get this customer's addresses
        if customer_id in customer_addresses and customer_addresses[customer_id]:
            customer_address_ids = customer_addresses[customer_id]
            shipping_address_id = random.choice(customer_address_ids)
            billing_address_id = random.choice(customer_address_ids)  # Could be same or different
            
            orders_data.append({
                'order_id': fake.unique.random_number(digits=12),
                'customer_id': customer_id,
                'order_date': fake.date_time_between(start_date='-2y', end_date='now'),
                'status': random.choice(['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED']),
                'shipping_address_id': shipping_address_id,
                'billing_address_id': billing_address_id,
                'total_amount': 0,  # Will be calculated later
                'payment_method': random.choice(['Credit Card', 'PayPal', 'Stripe', 'Bank Transfer'])
            })
    
    # Add additional orders if needed
    remaining_orders = num_orders - len(customer_ids)
    if remaining_orders > 0:
        for _ in range(remaining_orders):
            # Select a random customer and their addresses
            customer_id = random.choice(customer_ids)
            if customer_id in customer_addresses and customer_addresses[customer_id]:
                customer_address_ids = customer_addresses[customer_id]
                shipping_address_id = random.choice(customer_address_ids)
                billing_address_id = random.choice(customer_address_ids)
                
                orders_data.append({
                    'order_id': fake.unique.random_number(digits=12),
                    'customer_id': customer_id,
                    'order_date': fake.date_time_between(start_date='-2y', end_date='now'),
                    'status': random.choice(['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED']),
                    'shipping_address_id': shipping_address_id,
                    'billing_address_id': billing_address_id,
                    'total_amount': 0,  # Will be calculated later
                    'payment_method': random.choice(['Credit Card', 'PayPal', 'Stripe', 'Bank Transfer'])
                })
    ecommerce_orders = pd.DataFrame(orders_data)

    # Generate Order Items and update order total
    order_items_data = []
    order_ids = ecommerce_orders['order_id'].tolist()
    product_price_map = ecommerce_products.set_index('product_id')['price'].to_dict()
    order_totals = {}

    # Create a list of all product IDs
    all_product_ids = list(product_price_map.keys())

    for order_id in order_ids:
        num_items = random.randint(1, 5)
        current_order_total = 0
        
        # Select random products for this order without replacement if possible
        order_products = random.sample(all_product_ids, min(num_items, len(all_product_ids)))
        
        # If we need more products than available, allow duplicates
        if num_items > len(order_products):
            additional_products = [random.choice(all_product_ids) for _ in range(num_items - len(order_products))]
            order_products.extend(additional_products)
        
        for product_id in order_products:
            quantity = random.randint(1, 3)
            unit_price = product_price_map[product_id]
            line_total = unit_price * quantity
            current_order_total += line_total
            
            order_items_data.append({
                'order_item_id': fake.unique.random_number(digits=15),
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total
            })
            
        order_totals[order_id] = round(current_order_total, 2)

    ecommerce_order_items = pd.DataFrame(order_items_data)
    ecommerce_orders['total_amount'] = ecommerce_orders['order_id'].map(order_totals)


    return (ecommerce_customers, ecommerce_addresses, product_categories,
            ecommerce_products, ecommerce_orders, ecommerce_order_items)

def generate_marketing_campaign_data(num_campaigns=150):
    """
    Generates synthetic data for marketing campaigns.

    Args:
        num_campaigns (int): The number of campaigns to generate.

    Returns:
        pd.DataFrame: A DataFrame containing marketing campaign data.
    """
    campaigns_data = []
    for _ in range(num_campaigns):
        spend = round(random.uniform(1000, 50000), 2)
        revenue = round(spend * random.uniform(0.8, 3.5), 2)
        campaigns_data.append({
            'campaign_id': fake.unique.random_number(digits=7),
            'channel': random.choice(['EMAIL', 'SOCIAL', 'PPC', 'AFFILIATE']),
            'month': fake.date_between(start_date='-2y', end_date='now').replace(day=1),
            'spend_amount': spend,
            'impressions': random.randint(10000, 1000000),
            'clicks': random.randint(500, 50000),
            'conversions': random.randint(50, 2000),
            'revenue_generated': revenue
        })
    marketing_campaigns = pd.DataFrame(campaigns_data)
    return marketing_campaigns


if __name__ == "__main__":
    # Create output directory
    output_dir = "synthetic_data"
    os.makedirs(output_dir, exist_ok=True)

    # Define the order of tables to generate and save based on dependencies
    table_order = [
        'bank_customer',
        'bank_account',
        'bank_transaction',
        'ecommerce_customer',
        'ecommerce_address',
        'product_category',
        'ecommerce_product',
        'ecommerce_order',
        'ecommerce_order_item',
        'analytics_customer',
        'analytics_fct_banking',
        'analytics_fct_order',
        'analytics_fct_order_item',
        'marketing_campaign'
    ]

    # Generate all data first
    bank_customers, bank_accounts, bank_transactions = generate_banking_data()
    (ecommerce_customers, ecommerce_addresses, product_categories,
     ecommerce_products, ecommerce_orders, ecommerce_order_items) = generate_ecommerce_data()
    marketing_campaigns = generate_marketing_campaign_data()

    # Create a dictionary mapping table names to their corresponding DataFrames
    data_frames = {
        'bank_customer': bank_customers,
        'bank_account': bank_accounts,
        'bank_transaction': bank_transactions,
        'ecommerce_customer': ecommerce_customers,
        'ecommerce_address': ecommerce_addresses,
        'product_category': product_categories,
        'ecommerce_product': ecommerce_products,
        'ecommerce_order': ecommerce_orders,
        'ecommerce_order_item': ecommerce_order_items,
        'marketing_campaign': marketing_campaigns
    }

    # File name mapping (some table names differ from file names)
    file_name_map = {
        'bank_customer': 'bank_customers',
        'bank_account': 'bank_accounts',
        'bank_transaction': 'bank_transactions',
        'ecommerce_customer': 'ecommerce_customers',
        'ecommerce_address': 'ecommerce_addresses',
        'product_category': 'product_categories',
        'ecommerce_product': 'ecommerce_products',
        'ecommerce_order': 'ecommerce_orders',
        'ecommerce_order_item': 'ecommerce_order_items',
        'marketing_campaign': 'marketing_campaigns'
    }

    # Save data in the specified order
    pointer = 0
    for table in table_order:
        if table in data_frames:
            file_name = file_name_map.get(table, table)
            data_frames[table].to_csv(f"{output_dir}/{pointer}_{table}.csv", index=False)
            print(f"{file_name} Generated and saved {table}.csv")
            pointer += 1
        else:
            print(f"Warning: Table '{table}' specified in order but not generated")

    print(f"Synthetic data generated and saved in '{output_dir}' directory.")