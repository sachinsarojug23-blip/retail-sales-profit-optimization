import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_superstore_dataset(n_samples=4000):
    """Generates a realistic Superstore Retail dataset mirroring real-world business dynamics."""
    np.random.seed(42)
    
    categories = {
        'Technology': ['Phones', 'Chairs', 'Machines', 'Accessories'],
        'Furniture': ['Bookcases', 'Chairs', 'Furnishings', 'Tables'],
        'Office Supplies': ['Appliances', 'Art', 'Binders', 'Paper', 'Storage']
    }
    
    regions = ['East', 'West', 'Central', 'South']
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    cat_list = []
    subcat_list = []
    for _ in range(n_samples):
        c = np.random.choice(list(categories.keys()), p=[0.3, 0.3, 0.4])
        sc = np.random.choice(categories[c])
        cat_list.append(c)
        subcat_list.append(sc)
        
    discounts = np.random.choice([0.0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7], size=n_samples, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.08, 0.05, 0.02])
    prices = np.random.uniform(20, 800, size=n_samples).round(2)
    quantities = np.random.randint(1, 10, size=n_samples)
    
    sales = (prices * quantities * (1 - discounts)).round(2)
    
    base_margin = np.where(np.array(cat_list) == 'Technology', 0.25, np.where(np.array(cat_list) == 'Office Supplies', 0.20, 0.10))
    profit_margin = base_margin - (discounts * 0.8)
    profit = (sales * profit_margin).round(2)
    
    orders_df = pd.DataFrame({
        'order_id': [f'CA-2023-{10000+i}' for i in range(n_samples)],
        'customer_id': [f'CUST-{np.random.randint(100, 999)}' for _ in range(n_samples)],
        'order_date': pd.date_range('2023-01-01', periods=n_samples, freq='2h').astype(str),
        'ship_mode': np.random.choice(['Standard Class', 'Second Class', 'First Class', 'Same Day'], size=n_samples)
    })
    
    customers_df = pd.DataFrame({
        'customer_id': orders_df['customer_id'],
        'segment': np.random.choice(segments, size=n_samples, p=[0.5, 0.3, 0.2]),
        'region': np.random.choice(regions, size=n_samples, p=[0.3, 0.3, 0.25, 0.15])
    })
    
    details_df = pd.DataFrame({
        'order_id': orders_df['order_id'],
        'category': cat_list,
        'sub_category': subcat_list,
        'sales': sales,
        'quantity': quantities,
        'discount': discounts,
        'profit': profit
    })
    
    return orders_df, customers_df, details_df

def setup_sqlite_db():
    """Sets up and populates SQLite database."""
    conn = sqlite3.connect('superstore_analytics.db')
    orders, customers, details = generate_superstore_dataset()
    
    orders.to_sql('orders', conn, if_exists='replace', index=False)
    customers.to_sql('customers', conn, if_exists='replace', index=False)
    details.to_sql('order_details', conn, if_exists='replace', index=False)
    
    print("✅ Superstore SQLite Database successfully created and populated.")
    return conn

def execute_business_sql_queries(conn):
    """Runs core SQL queries addressing business problems."""
    print("\n" + "="*65)
    print("📌 BUSINESS ANALYSIS 1: Discount Impact on Profitability & Margins")
    print("="*65)
    
    query1 = """
    SELECT 
        CASE 
            WHEN discount = 0 THEN '0% (No Discount)'
            WHEN discount <= 0.15 THEN '1% - 15% (Low Discount)'
            WHEN discount <= 0.30 THEN '16% - 30% (Medium Discount)'
            ELSE '> 30% (High Discount)'
        END AS discount_bracket,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
    FROM order_details
    GROUP BY discount_bracket
    ORDER BY profit_margin_pct DESC;
    """
    df1 = pd.read_sql_query(query1, conn)
    print(df1.to_string(index=False))
    
    print("\n" + "="*65)
    print("📌 BUSINESS ANALYSIS 2: Loss-Making Sub-Categories (Bottom Performers)")
    print("="*65)
    
    query2 = """
    WITH CategoryPerformance AS (
        SELECT 
            category,
            sub_category,
            ROUND(SUM(sales), 2) AS category_sales,
            ROUND(SUM(profit), 2) AS category_profit,
            ROUND(AVG(discount) * 100, 1) AS avg_discount_pct,
            DENSE_RANK() OVER (ORDER BY SUM(profit) ASC) AS loss_rank
        FROM order_details
        GROUP BY category, sub_category
    )
    SELECT 
        category,
        sub_category,
        category_sales,
        category_profit,
        avg_discount_pct,
        loss_rank
    FROM CategoryPerformance
    LIMIT 6;
    """
    df2 = pd.read_sql_query(query2, conn)
    print(df2.to_string(index=False))
    
    print("\n" + "="*65)
    print("📌 BUSINESS ANALYSIS 3: Regional Sales vs Profitability Breakdown")
    print("="*65)
    
    query3 = """
    SELECT 
        c.region,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(d.sales), 2) AS total_sales,
        ROUND(SUM(d.profit), 2) AS total_profit,
        ROUND((SUM(d.profit) / SUM(d.sales)) * 100, 2) AS profit_margin_pct
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_details d ON o.order_id = d.order_id
    GROUP BY c.region
    ORDER BY profit_margin_pct DESC;
    """
    df3 = pd.read_sql_query(query3, conn)
    print(df3.to_string(index=False))
    
    return df1, df2, df3

def generate_visualizations(conn):
    """Generates Seaborn visualization charts for portfolio presentation."""
    os.makedirs('visualizations', exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    query = """
    SELECT discount, profit, sales, category 
    FROM order_details;
    """
    df = pd.read_sql_query(query, conn)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='discount', y='profit', hue='category', marker='o', errorbar=None, palette="Set1")
    plt.axhline(0, color='red', linestyle='--', linewidth=1.5, label='Zero Profit Baseline')
    plt.title('Impact of Discount Rate on Order Profitability by Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Discount Rate (0.0 = 0%, 0.5 = 50%)', fontsize=11)
    plt.ylabel('Profit / Loss ($)', fontsize=11)
    plt.legend(title='Category')
    plt.tight_layout()
    chart_path = 'visualizations/discount_vs_profitability.png'
    plt.savefig(chart_path, dpi=300)
    plt.close()
    
    print("🎨 Visualizations saved successfully in 'visualizations/' folder.")

if __name__ == "__main__":
    db_conn = setup_sqlite_db()
    execute_business_sql_queries(db_conn)
    generate_visualizations(db_conn)
