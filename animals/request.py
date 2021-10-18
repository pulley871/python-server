from models import Animal, Location, Customer
import sqlite3
import json

db_connect = "./kennel.db"

def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect(db_connect) as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            c.password customer_password
        FROM animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            location = Location(row["id"], row["location_name"], row["location_address"])
            customer = Customer(row["id"], row["customer_name"], row["customer_address"], row["customer_email"], row["customer_password"])
            animal.location = location.__dict__
            animal.customer = customer.__dict__
            animals.append(animal.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)

# Function with a single parameter
def get_single_animal(id, ):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
            
        FROM animal a
        WHERE a.id = ? 
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        try:
            animal = Animal(data['id'], data['name'], data['breed'],
                                data['status'], data['location_id'],
                                data['customer_id'])

            return json.dumps(animal.__dict__)
        #item not found
        except TypeError:
            return "Animal Not Found"
def get_animals_by_location(location_id):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
            
        FROM animal a
        WHERE a.location_id = ? 
        """, ( location_id, ))
        animals = []
        data = db_cursor.fetchall()
        for row in data:
            animals.append(Animal(row["id"], row["name"], row["breed"], row["status"], row["location_id"], row["customer_id"]).__dict__)
        return json.dumps(animals)
def get_animals_by_status(status):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
            
        FROM animal a
        WHERE LOWER(a.status) = ?
        """, ( status.lower(), ))
        animals = []
        data = db_cursor.fetchall()
        for row in data:
            animals.append(Animal(row["id"], row["name"], row["breed"], row["status"], row["location_id"], row["customer_id"]).__dict__)
        return json.dumps(animals)
def create_animal(animal):
    with sqlite3.connect(db_connect) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            (name, breed, status, location_id, customer_id)
        VALUES
            (?,?,?,?,?)
        """, (animal['name'], animal['breed'], animal['status'], animal['location_id'], animal['customer_id'],))
        animal['id'] = db_cursor.lastrowid

def delete_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))



def update_animal(id, new_animal):
    with sqlite3.connect(db_connect) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """,(new_animal["name"], new_animal["breed"], new_animal["status"], new_animal["location_id"], new_animal["customer_id"], id))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True
    
