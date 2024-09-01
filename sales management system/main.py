from tkinter import *
import sqlite3

# Database setup
def connect():
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customer(id),
            FOREIGN KEY (product_id) REFERENCES product(id)
        )
    """)
    conn.commit()
    conn.close()

def insert_customer(name, phone):
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO customer (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    view_customers()

def insert_product(name, price, quantity):
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO product (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
    conn.commit()
    conn.close()
    view_products()

def view_customers():
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer")
    rows = cur.fetchall()
    conn.close()
    customer_listbox.delete(0, END)
    for row in rows:
        customer_listbox.insert(END, row)

def view_products():
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()
    conn.close()
    product_listbox.delete(0, END)
    for row in rows:
        product_listbox.insert(END, row)

def add_sale(customer_id, product_id, quantity):
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO sales (customer_id, product_id, quantity) VALUES (?, ?, ?)",
                (customer_id, product_id, quantity))
    cur.execute("UPDATE product SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
    conn.commit()
    conn.close()

def view_sales():
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, c.name, p.name, s.quantity FROM sales s
        JOIN customer c ON s.customer_id = c.id
        JOIN product p ON s.product_id = p.id
    """)
    rows = cur.fetchall()
    conn.close()
    sales_listbox.delete(0, END)
    for row in rows:
        sales_listbox.insert(END, row)

# GUI Setup
connect()
app = Tk()
app.title("Sales Management System")

# Customer Management Frame
customer_frame = Frame(app)
customer_frame.pack(pady=10)
Label(customer_frame, text="Customer Name").grid(row=0, column=0)
customer_name_entry = Entry(customer_frame)
customer_name_entry.grid(row=0, column=1)

Label(customer_frame, text="Customer Phone").grid(row=1, column=0)
customer_phone_entry = Entry(customer_frame)
customer_phone_entry.grid(row=1, column=1)

add_customer_button = Button(customer_frame, text="Add Customer", command=lambda: insert_customer(
    customer_name_entry.get(), customer_phone_entry.get()))
add_customer_button.grid(row=2, columnspan=2, pady=10)

customer_listbox = Listbox(app, height=6, width=50)
customer_listbox.pack(pady=10)
view_customers()

# Product Management Frame
product_frame = Frame(app)
product_frame.pack(pady=10)
Label(product_frame, text="Product Name").grid(row=0, column=0)
product_name_entry = Entry(product_frame)
product_name_entry.grid(row=0, column=1)

Label(product_frame, text="Price").grid(row=1, column=0)
product_price_entry = Entry(product_frame)
product_price_entry.grid(row=1, column=1)

Label(product_frame, text="Quantity").grid(row=2, column=0)
product_quantity_entry = Entry(product_frame)
product_quantity_entry.grid(row=2, column=1)

add_product_button = Button(product_frame, text="Add Product", command=lambda: insert_product(
    product_name_entry.get(), float(product_price_entry.get()), int(product_quantity_entry.get())))
add_product_button.grid(row=3, columnspan=2, pady=10)

product_listbox = Listbox(app, height=6, width=50)
product_listbox.pack(pady=10)
view_products()

# Sales Management Frame
sales_frame = Frame(app)
sales_frame.pack(pady=10)

Label(sales_frame, text="Customer ID").grid(row=0, column=0)
customer_id_entry = Entry(sales_frame)
customer_id_entry.grid(row=0, column=1)

Label(sales_frame, text="Product ID").grid(row=1, column=0)
product_id_entry = Entry(sales_frame)
product_id_entry.grid(row=1, column=1)

Label(sales_frame, text="Quantity").grid(row=2, column=0)
sales_quantity_entry = Entry(sales_frame)
sales_quantity_entry.grid(row=2, column=1)

add_sales_button = Button(sales_frame, text="Add Sale", command=lambda: add_sale(
    int(customer_id_entry.get()), int(product_id_entry.get()), int(sales_quantity_entry.get())))
add_sales_button.grid(row=3, columnspan=2, pady=10)

sales_listbox = Listbox(app, height=6, width=50)
sales_listbox.pack(pady=10)
view_sales()

app.mainloop()