import pandas as pd

# Table 1: Customers (with some messy spaces and missing values)
customers_data = {
    "Customer ID": [101, 102, 103, None, 104],
    "Customer Name": [
        "  Rahul Sharma ",
        "Priya Nair",
        "Arjun Mehta  ",
        None,
        "Sneha Iyer",
    ],
    "City": ["Chennai", "Bengaluru", "Mumbai", None, "Chennai"],
    "Signup Date": [
        "2026-01-15",
        "2026-02-10",
        "2026-03-05",
        None,
        "2026-04-12",
    ],
}

# Table 2: Orders (with currency symbols to clean)
orders_data = {
    "Order ID": [5001, 5002, 5003, 5004, 5005],
    "Customer ID": [101, 102, 101, 103, 104],
    "Product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"],
    "Amount": ["₹55,000", "₹1,200", "₹3,500", "₹18,000", "₹4,500"],
    "Status": ["Delivered", "Delivered", "Pending", "Delivered", "Cancelled"],
}

df_customers = pd.DataFrame(customers_data)
df_orders = pd.DataFrame(orders_data)

# Write both tables as separate sheets in one Excel workbook
with pd.ExcelWriter("sales_data.xlsx", engine="openpyxl") as writer:
  df_customers.to_excel(writer, sheet_name="Customers", index=False)
  df_orders.to_excel(writer, sheet_name="Orders", index=False)

print("Success! sales_data.xlsx has been created.")