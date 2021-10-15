from models import Location
import sqlite3
import json
db_connect = "./kennel.db"
def get_all_locations():
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address

        FROM location a
        """)
        locations = []
        data = db_cursor.fetchall()
        for row in data:
            location = Location(row["id"], row["name"], row["address"])
            locations.append(location.__dict__)
        return json.dumps(locations)

def get_single_location(id):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        WHERE a.id = ?
        """,(id,))
        data = db_cursor.fetchone()
        try:
            return json.dumps(Location(data["id"], data["name"], data["address"]).__dict__)
        except:
            return "No location found"


def post_location(location):
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location

def delete_location(id):
    item_index = -1
    for index, item in enumerate(LOCATIONS):
        if item["id"] == id:
            item_index = index
    if item_index >= 0:
        LOCATIONS.pop(item_index)

def update_location(id, new_location):
    for index, item in enumerate(LOCATIONS):
        if item["id"] == id:
            LOCATIONS[index] = new_location
            break