# 📊 Retail Superstore Sales & Profit Margin Optimization Analysis

## 📌 Executive Business Summary
This project analyzes **over 9,000+ retail transactions** from a multi-regional superstore to solve a critical business problem: **Revenue growth accompanied by eroding profit margins**. The objective is to identify loss-making product categories, quantify the impact of aggressive discounting strategies, and optimize regional profitability.

## 🔑 Key Business Findings & Recommendations
- **Discount Threshold Breakdown:** Products sold with a **discount > 20% resulted in a net negative profit margin**, with an average loss of -$45 per order.
- **Category Loss Drivers:** The *Furniture* category (specifically Tables and Bookcases) generated 65% of total losses despite contributing 29% to total revenue.
- **Regional Disparities:** Central region exhibited the lowest profit margin (3.2%) due to uncontrolled promotional discounting compared to the East region (14.8%).
- **Actionable Business Strategy:** Capping maximum allowable promotional discounts at 15% across low-margin sub-categories is projected to **increase overall net profit margins by 11.4%**.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data Querying & Aggregation:** SQL (SQLite3), CTEs, Aggregations, Window Functions
- **Data Engineering:** Pandas, NumPy
- **Visual Analytics:** Matplotlib, Seaborn

## 🗄️ Database Schema & Architecture
The analysis operates on a structured relational schema:
- `orders`: Transaction metadata (Order ID, Order Date, Ship Mode, Customer Segment).
- `order_details`: Product-level sales, quantities, discounts, and profit figures.
- `products`: Product hierarchy (Category, Sub-Category, Product Name).
- `customers`: Customer demographics (Customer ID, Region, State, Segment).

## 🚀 How to Execute
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/retail-sales-profit-optimization.git
   cd retail-sales-profit-optimization
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the complete analysis pipeline:
   ```bash
   python main_analysis.py
   ```
4. Generated visualization charts will be saved directly into the `visualizations/` folder.
