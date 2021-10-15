from models import Customer
import sqlite3
import json

db_connect = "./kennel.db"

def get_all_customers():
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
        FROM customer a
        """)
        customers = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            customer = Customer(row["id"], row["name"], row["address"], row["email"], row["password"])
            customers.append(customer.__dict__)
        return json.dumps(customers)
def get_single_customer(id):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password

        FROM customer a
        WHERE a.id = ?
        """,(id,))

        data = db_cursor.fetchone()
        try:
            customer = Customer(data["id"], data["name"], data["address"], data["email"], data["password"])
            return json.dumps(customer.__dict__)
        except:
            return "No customer found"

def post_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    new_id = max_id + 1
    customer["id"] = new_id
    CUSTOMERS.append(customer)
    return customer

def delete_customer(id):
    item_index = -1
    for index, item in enumerate(CUSTOMERS):
        if item["id"] == id:
            item_index = index
    if item_index >= 0:
        CUSTOMERS.pop(item_index)

def update_customer(id, new_customer):
    for index, item in enumerate(CUSTOMERS):
        if item["id"] == id:
            CUSTOMERS[index] = new_customer
            break