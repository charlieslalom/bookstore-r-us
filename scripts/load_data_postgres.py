#!/usr/bin/env python3
"""
Data loader for Bookstore-R-Us Python microservices.
Creates PostgreSQL tables and loads sample product data from products.json.
"""

import json
import os
import random
import sys
from urllib.parse import urlparse

import psycopg2
from psycopg2.extras import execute_values

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5433/postgres")

# Parse database URL
parsed = urlparse(DATABASE_URL)
DB_CONFIG = {
    "host": parsed.hostname or "localhost",
    "port": parsed.port or 5432,
    "database": parsed.path.lstrip("/") or "postgres",
    "user": parsed.username or "postgres",
    "password": parsed.password or "password",
}

# SQL to create tables
CREATE_TABLES_SQL = """
-- Products table
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    brand TEXT,
    categories JSONB DEFAULT '[]',
    imurl TEXT,
    price FLOAT,
    title TEXT,
    description TEXT,
    also_bought JSONB DEFAULT '[]',
    also_viewed JSONB DEFAULT '[]',
    bought_together JSONB DEFAULT '[]',
    buy_after_viewing JSONB DEFAULT '[]',
    num_reviews INT,
    num_stars FLOAT,
    avg_stars FLOAT
);

-- Product rankings table
CREATE TABLE IF NOT EXISTS product_rankings (
    asin TEXT NOT NULL,
    category TEXT NOT NULL,
    sales_rank INT,
    title TEXT,
    price FLOAT,
    imurl TEXT,
    num_reviews INT,
    num_stars FLOAT,
    avg_stars FLOAT,
    PRIMARY KEY (asin, category)
);

-- Product inventory table
CREATE TABLE IF NOT EXISTS product_inventory (
    asin TEXT PRIMARY KEY,
    quantity INT
);

-- Shopping cart table
CREATE TABLE IF NOT EXISTS shopping_cart (
    cart_key TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    asin TEXT NOT NULL,
    time_added TEXT,
    quantity INT DEFAULT 1
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id INT,
    order_details TEXT,
    order_time TEXT,
    order_total FLOAT
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_product_rankings_category ON product_rankings(category);
CREATE INDEX IF NOT EXISTS idx_shopping_cart_user ON shopping_cart(user_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
"""


def connect_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"Connected to database: {DB_CONFIG['database']} on {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        return conn
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)


def create_tables(conn):
    """Create all required tables."""
    print("Creating tables...")
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLES_SQL)
    conn.commit()
    print("Tables created successfully.")


def load_products(conn, products_file):
    """Load products from JSON file into database."""
    print(f"Loading products from {products_file}...")

    # Use dicts to deduplicate by key
    products_dict = {}
    rankings_dict = {}
    inventory_dict = {}

    with open(products_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                product = json.loads(line.strip())

                # Generate random review data
                num_reviews = random.randint(100, 1000)
                num_stars = round((random.random() * 2 * num_reviews + 3 * num_reviews), 2)
                avg_stars = round(num_stars / num_reviews, 2)
                default_price = round(random.uniform(20, 800), 2)

                # Only process products with description (matching original logic)
                if "description" not in product:
                    continue

                asin = product.get("asin")
                if not asin:
                    continue

                # Skip if already seen (deduplicate)
                if asin in products_dict:
                    continue

                # Extract related products
                related = product.get("related", {})

                # Categories - flatten the nested list
                categories = []
                if "categories" in product and product["categories"]:
                    categories = product["categories"][0] if isinstance(product["categories"][0], list) else product["categories"]

                # Product data (deduplicate by asin)
                products_dict[asin] = (
                    asin,
                    product.get("brand"),
                    json.dumps(categories),
                    product.get("imUrl"),
                    product.get("price", default_price),
                    product.get("title"),
                    product.get("description"),
                    json.dumps(related.get("also_bought", [])),
                    json.dumps(related.get("also_viewed", [])),
                    json.dumps(related.get("bought_together", [])),
                    json.dumps(related.get("buy_after_viewing", [])),
                    num_reviews,
                    num_stars,
                    avg_stars
                )

                # Inventory data (deduplicate by asin)
                inventory_dict[asin] = (
                    asin,
                    random.randint(100, 1000)
                )

                # Rankings data (if salesRank exists)
                if "salesRank" in product:
                    for category, rank in product["salesRank"].items():
                        # Deduplicate by (asin, category) key
                        key = (asin, category)
                        if key not in rankings_dict:
                            rankings_dict[key] = (
                                asin,
                                category,
                                rank,
                                product.get("title"),
                                product.get("price", default_price),
                                product.get("imUrl"),
                                num_reviews,
                                num_stars,
                                avg_stars
                            )

            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse line {line_num}: {e}")
                continue

    # Convert dicts to lists
    products_data = list(products_dict.values())
    inventory_data = list(inventory_dict.values())
    rankings_data = list(rankings_dict.values())

    # Insert data
    with conn.cursor() as cur:
        # Clear existing data
        print("Clearing existing product data...")
        cur.execute("TRUNCATE products, product_rankings, product_inventory CASCADE")

        # Insert products
        if products_data:
            print(f"Inserting {len(products_data)} products...")
            execute_values(
                cur,
                """INSERT INTO products
                   (id, brand, categories, imurl, price, title, description,
                    also_bought, also_viewed, bought_together, buy_after_viewing,
                    num_reviews, num_stars, avg_stars)
                   VALUES %s
                   ON CONFLICT (id) DO UPDATE SET
                    brand = EXCLUDED.brand,
                    categories = EXCLUDED.categories,
                    imurl = EXCLUDED.imurl,
                    price = EXCLUDED.price,
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    also_bought = EXCLUDED.also_bought,
                    also_viewed = EXCLUDED.also_viewed,
                    bought_together = EXCLUDED.bought_together,
                    buy_after_viewing = EXCLUDED.buy_after_viewing,
                    num_reviews = EXCLUDED.num_reviews,
                    num_stars = EXCLUDED.num_stars,
                    avg_stars = EXCLUDED.avg_stars""",
                products_data
            )

        # Insert inventory
        if inventory_data:
            print(f"Inserting {len(inventory_data)} inventory records...")
            execute_values(
                cur,
                """INSERT INTO product_inventory (asin, quantity)
                   VALUES %s
                   ON CONFLICT (asin) DO UPDATE SET quantity = EXCLUDED.quantity""",
                inventory_data
            )

        # Insert rankings
        if rankings_data:
            print(f"Inserting {len(rankings_data)} ranking records...")
            execute_values(
                cur,
                """INSERT INTO product_rankings
                   (asin, category, sales_rank, title, price, imurl, num_reviews, num_stars, avg_stars)
                   VALUES %s
                   ON CONFLICT (asin, category) DO UPDATE SET
                    sales_rank = EXCLUDED.sales_rank,
                    title = EXCLUDED.title,
                    price = EXCLUDED.price,
                    imurl = EXCLUDED.imurl,
                    num_reviews = EXCLUDED.num_reviews,
                    num_stars = EXCLUDED.num_stars,
                    avg_stars = EXCLUDED.avg_stars""",
                rankings_data
            )

    conn.commit()
    print(f"Data loaded successfully!")
    print(f"  - Products: {len(products_data)}")
    print(f"  - Inventory: {len(inventory_data)}")
    print(f"  - Rankings: {len(rankings_data)}")


def main():
    """Main entry point."""
    # Find products.json file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    products_file = os.path.join(repo_root, "resources", "products.json")

    if not os.path.exists(products_file):
        print(f"Error: Products file not found: {products_file}")
        sys.exit(1)

    print("=" * 50)
    print("Bookstore-R-Us Data Loader")
    print("=" * 50)
    print(f"Database URL: {DATABASE_URL}")
    print(f"Products file: {products_file}")
    print()

    conn = connect_db()
    try:
        create_tables(conn)
        load_products(conn, products_file)
        print()
        print("=" * 50)
        print("Database initialization complete!")
        print("=" * 50)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
