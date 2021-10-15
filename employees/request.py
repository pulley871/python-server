from models import Employee
import sqlite3
import json
db_connect = "./kennel.db"
def get_all_employees():
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id
        FROM employee a
        """)
        employees = []
        data = db_cursor.fetchall()
        for row in data:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)
        return json.dumps(employees)
def get_single_employee(id):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id
        FROM employee a
        WHERE a.id = ?
        """, (id,))
        data = db_cursor.fetchone()
        try:
            employee = Employee(data["id"], data["name"], data["address"], data["location_id"])
            return json.dumps(employee.__dict__)
        except:
            return "No Employee Found"
def post_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee

def delete_employee(id):
    item_index = -1
    for index, item in enumerate(EMPLOYEES):
        if item["id"] == id:
            item_index = index
    if item_index >= 0:
        EMPLOYEES.pop(item_index)

def update_employee(id, new_employee):
    for index, item in enumerate(EMPLOYEES):
        if item["id"] == id:
            EMPLOYEES[index] = new_employee
            break