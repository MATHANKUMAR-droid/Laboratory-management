import tkinter as tk
from tkinter import messagebox
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
dbname="postgres",
user="postgres",
password="123",
host="localhost",
port="5432"
)
cursor = conn.cursor()

# Create the equipment table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS equipment (
id SERIAL PRIMARY KEY,
name VARCHAR(255),
quantity INTEGER
)
''')
conn.commit()

def insert_equipment():
name = entry_name.get()
quantity = entry_quantity.get()

try:
quantity = int(quantity)
except ValueError:
messagebox.showerror("Error", "Quantity must be a valid integer.")
return

cursor.execute('''
INSERT INTO equipment (name, quantity) VALUES (%s, %s)
''', (name, quantity))
conn.commit()
messagebox.showinfo("Success", "Equipment inserted successfully!")

def delete_equipment():
equipment_id = entry_id.get()

try:
equipment_id = int(equipment_id)
except ValueError:
messagebox.showerror("Error", "Equipment ID must be a valid integer.")
return

cursor.execute('''
DELETE FROM equipment WHERE id = %s
''', (equipment_id,))
conn.commit()
messagebox.showinfo("Success", "Equipment deleted successfully!")

def update_equipment():
equipment_id = entry_id.get()
new_quantity = entry_quantity.get()

try:
equipment_id = int(equipment_id)
new_quantity = int(new_quantity)
except ValueError:
messagebox.showerror("Error", "Equipment ID and Quantity must be valid integers.")
return

cursor.execute('''
UPDATE equipment SET quantity = %s WHERE id = %s
''', (new_quantity, equipment_id))
conn.commit()
messagebox.showinfo("Success", "Equipment updated successfully!")

def display_equipment():
cursor.execute('SELECT * FROM equipment')
equipment_list = cursor.fetchall()
if not equipment_list:
messagebox.showinfo("Info", "No equipment found.")
else:
equipment_str = "ID\tName\tQuantity\n"
for equipment in equipment_list:
equipment_str += f"{equipment[0]}\t{equipment[1]}\t{equipment[2]}\n"
messagebox.showinfo("Equipment List", equipment_str)

# GUI Setup
root = tk.Tk()
root.title("Laboratory Management System")

# Entry fields
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)
entry_quantity = tk.Entry(root, width=30)
entry_quantity.grid(row=1, column=1, padx=10, pady=5)
entry_id = tk.Entry(root, width=30)
entry_id.grid(row=2, column=1, padx=10, pady=5)

# Labels
label_name = tk.Label(root, text="Equipment Name")
label_name.grid(row=0, column=0, padx=10, pady=5)
label_quantity = tk.Label(root, text="Quantity")
label_quantity.grid(row=1, column=0, padx=10, pady=5)
label_id = tk.Label(root, text="Equipment ID")
label_id.grid(row=2, column=0, padx=10, pady=5)

# Buttons
insert_button = tk.Button(root, text="Insert Equipment", command=insert_equipment)
insert_button.grid(row=3, column=0, columnspan=2, pady=10)
delete_button = tk.Button(root, text="Delete Equipment", command=delete_equipment)
delete_button.grid(row=4, column=0, columnspan=2, pady=10)
update_button = tk.Button(root, text="Update Equipment", command=update_equipment)
update_button.grid(row=5, column=0, columnspan=2, pady=10)
display_button = tk.Button(root, text="Display Equipment", command=display_equipment)
display_button.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
