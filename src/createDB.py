import sqlite3

# Connect to (or create) ecommerce.db
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# 1. Create Tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    city TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);
""")

# 2. Insert 10 Customers
customers_data = [
    ('John', 'Doe', 'john.doe@example.com', 'New York'),
    ('Jane', 'Smith', 'jane.smith@example.com', 'Los Angeles'),
    ('Michael', 'Johnson', 'michael.j@example.com', 'Chicago'),
    ('Emily', 'Davis', 'emily.davis@example.com', 'Houston'),
    ('David', 'Wilson', 'david.w@example.com', 'Phoenix'),
    ('Sarah', 'Brown', 'sarah.b@example.com', 'Philadelphia'),
    ('James', 'Taylor', 'james.t@example.com', 'San Antonio'),
    ('Amanda', 'Anderson', 'amanda.a@example.com', 'San Diego'),
    ('Robert', 'Thomas', 'robert.t@example.com', 'Dallas'),
    ('Jessica', 'Jackson', 'jessica.j@example.com', 'San Jose')
]
cursor.executemany("""
INSERT INTO customers (first_name, last_name, email, city) 
VALUES (?, ?, ?, ?)
""", customers_data)

# 3. Insert Products
products_data = [
    ('Wireless Laptop Mouse', 'Electronics', 25.99),
    ('Mechanical Keyboard', 'Electronics', 79.99),
    ('Noise Canceling Headphones', 'Electronics', 199.99),
    ('Ergonomic Desk Chair', 'Furniture', 249.50),
    ('Stainless Steel Water Bottle', 'Accessories', 15.00)
]
cursor.executemany("""
INSERT INTO products (product_name, category, price) 
VALUES (?, ?, ?)
""", products_data)

# 4. Insert 10 Orders
orders_data = [
    (1, 1, '2026-03-01', 1),
    (2, 3, '2026-03-01', 1),
    (3, 2, '2026-03-02', 2),
    (4, 5, '2026-03-02', 3),
    (5, 4, '2026-03-03', 1),
    (6, 1, '2026-03-04', 1),
    (7, 3, '2026-03-05', 1),
    (8, 2, '2026-03-05', 1),
    (9, 5, '2026-03-06', 2),
    (10, 4, '2026-03-07', 1)
]
cursor.executemany("""
INSERT INTO orders (customer_id, product_id, order_date, quantity) 
VALUES (?, ?, ?, ?)
""", orders_data)

conn.commit()
conn.close()

print("ecommerce.db created successfully!")