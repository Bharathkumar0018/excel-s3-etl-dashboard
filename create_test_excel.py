import pandas as pd

# Table 1: Employees (different columns, currency symbols, and messy spaces)
employees_data = {
    "Employee ID": ["E01", "E02", "E03", None, "E04", "E05"],
    "Full Name": [
        "  Karthik Subramanian",
        "Ananya Rao  ",
        "Vikram Desai",
        None,
        "Meera Krishnan",
        "Rohan Verma",
    ],
    "Department": [
        "Engineering",
        "Marketing",
        "Engineering",
        None,
        "Finance",
        "Marketing",
    ],
    "Location": [
        "Chennai",
        "Bengaluru",
        "Hyderabad",
        None,
        "Mumbai",
        "Chennai",
    ],
    "Annual Salary": [
        "₹14,50,000",
        "₹9,20,000",
        "₹16,00,000",
        None,
        "₹11,50,000",
        "₹8,80,000",
    ],
}

# Table 2: Projects (completely different schema)
projects_data = {
    "Project Code": ["PRJ-101", "PRJ-102", "PRJ-103", "PRJ-104"],
    "Project Title": [
        "Cloud Migration",
        "Mobile App Redesign",
        "AI Chatbot",
        "Payroll Automation",
    ],
    "Department": ["Engineering", "Marketing", "Engineering", "Finance"],
    "Budget": ["₹25,00,000", "₹12,00,000", "₹18,50,000", "₹7,50,000"],
    "Hours Logged": [420, 210, 340, 150],
}

df_emp = pd.DataFrame(employees_data)
df_proj = pd.DataFrame(projects_data)

with pd.ExcelWriter("company_data.xlsx", engine="openpyxl") as writer:
  df_emp.to_excel(writer, sheet_name="Employees", index=False)
  df_proj.to_excel(writer, sheet_name="Projects", index=False)

print("Done! company_data.xlsx is ready to upload.")