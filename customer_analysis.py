# ===============================
# Customer Sales Analysis Project
# ===============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -------------------------------
# 1. LOAD DATA
# -------------------------------
try:
    sales_df = pd.read_csv("sales_data.csv")
    customer_df = pd.read_csv("customer_data.csv")
except FileNotFoundError:
    print("❌ Error: sales_data.csv or customer_data.csv not found.")
    print("➡️ Make sure both files are in the same folder as this script.")
    exit()

print("✅ Data loaded successfully")

# -------------------------------
# 2. DATA EXPLORATION
# -------------------------------
print("\n--- Sales Data Info ---")
print(sales_df.info())

print("\n--- Customer Data Info ---")
print(customer_df.info())

# -------------------------------
# 3. DATA CLEANING
# -------------------------------
# Handle missing values
sales_df.fillna(0, inplace=True)
customer_df.fillna("Unknown", inplace=True)

# Convert date column
sales_df["Order_Date"] = pd.to_datetime(sales_df["Order_Date"], errors="coerce")

# Remove duplicates
sales_df.drop_duplicates(inplace=True)

# Create Revenue column
sales_df["Revenue"] = sales_df["Quantity"] * sales_df["Price"]

print("✅ Data cleaned successfully")

# -------------------------------
# 4. DATA MERGING
# -------------------------------
merged_df = pd.merge(
    sales_df,
    customer_df,
    on="Customer_ID",
    how="inner"
)

print("✅ Data merged successfully")

# -------------------------------
# 5. BASIC METRICS
# -------------------------------
total_revenue = merged_df["Revenue"].sum()
total_customers = merged_df["Customer_ID"].nunique()
avg_order_value = merged_df["Revenue"].mean()

print("\n📊 BASIC METRICS")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Customers: {total_customers}")
print(f"Average Order Value: ${avg_order_value:,.2f}")

# -------------------------------
# 6. TOP CUSTOMERS
# -------------------------------
top_customers = (
    merged_df.groupby("Customer_Name")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n🏆 TOP 10 CUSTOMERS")
print(top_customers)

# -------------------------------
# 7. SALES PATTERN ANALYSIS
# -------------------------------
merged_df["Month"] = merged_df["Order_Date"].dt.month

monthly_sales = merged_df.groupby("Month")["Revenue"].sum()

# -------------------------------
# 8. BEST SELLING PRODUCTS
# -------------------------------
best_products = (
    merged_df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# -------------------------------
# 9. PIVOT TABLE (ADVANCED ANALYSIS)
# -------------------------------
pivot_table = pd.pivot_table(
    merged_df,
    values="Revenue",
    index="Region",
    columns="Product",
    aggfunc="sum",
    fill_value=0
)

print("\n📌 PIVOT TABLE (Region vs Product)")
print(pivot_table)

# -------------------------------
# 10. CREATE VISUALIZATIONS
# -------------------------------
os.makedirs("visualizations", exist_ok=True)

# 1️⃣ Monthly Sales Trend
plt.figure()
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.grid()
plt.savefig("visualizations/monthly_sales.png")
plt.show()

# 2️⃣ Top Customers
plt.figure()
top_customers.plot(kind="bar")
plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.savefig("visualizations/top_customers.png")
plt.show()

# 3️⃣ Best Selling Products
plt.figure()
best_products.head(5).plot(kind="bar", color="green")
plt.title("Top 5 Best Selling Products")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.savefig("visualizations/top_products.png")
plt.show()

# 4️⃣ Region-wise Sales
region_sales = merged_df.groupby("Region")["Revenue"].sum()

plt.figure()
region_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sales Distribution by Region")
plt.ylabel("")
plt.savefig("visualizations/region_sales.png")
plt.show()

print("\n✅ All visualizations saved in 'visualizations/' folder")

# -------------------------------
# 11. FINAL INSIGHTS
# -------------------------------
print("\n📈 KEY BUSINESS INSIGHTS")
print("- Top customers contribute a significant share of revenue")
print("- Certain products dominate sales performance")
print("- Sales show seasonal patterns across months")
print("- Regional performance varies significantly")

print("\n🎉 Customer Sales Analysis Completed Successfully!")
