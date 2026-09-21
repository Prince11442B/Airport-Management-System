import mysql.connector as conn
from prettytable import PrettyTable

con = conn.connect(
    host="localhost",
    user="root",
    password="admin",
    database="aerodb"
)
auth = False

def create_tables():
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS runway_maintenance (
            maint_id INT PRIMARY KEY AUTO_INCREMENT,
            runway_no VARCHAR(5),
            maint_date DATE,
            status VARCHAR(20)
        )""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS departures (
            flight_no VARCHAR(10) PRIMARY KEY,
            airlines VARCHAR(50),
            destination VARCHAR(20),
            d_time DATETIME,
            gate VARCHAR(10),
            status VARCHAR(15))""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS arrivals (
            flight_no VARCHAR(10) PRIMARY KEY,
            airlines VARCHAR(50),
            origin VARCHAR(20),
            a_time DATETIME,
            gate VARCHAR(10),
            status VARCHAR(15))""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jetfuel (
            fuel_id INT PRIMARY KEY AUTO_INCREMENT,
            flight_no VARCHAR(10),
            fuel_quantity FLOAT,
            price DECIMAL(10,2),
            total DECIMAL(10,2),
            fueling_time DATETIME)""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pax (
            p_id INT PRIMARY KEY AUTO_INCREMENT,
            p_name VARCHAR(40),
            p_gender VARCHAR(2),
            p_flight_no VARCHAR(10),
            p_age INT,
            p_nationality VARCHAR(10))""")
    con.commit()
    cur.close()
    print("Tables Created Successfully!")

def admin():
    global auth
    pwd = input("Enter admin password: ")
    if pwd == "admin":
        auth = True
        print("Admin access granted.")
        return True
    else:
        print("Wrong password.")
        return False

def view_departures():
    cur = con.cursor()
    try:
        cur.execute("SELECT flight_no, airlines, destination, d_time, gate, status FROM departures")
        rows = cur.fetchall()
        if not rows:
            print("No departing flights found.")
            return
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cur.description]
        for row in rows:
            table.add_row(row)
        print(table)
    except conn.Error as err:
        print("Error viewing departures:", err)
    finally:
        cur.close()

def add_dept():
    if not auth:
        print("You must be logged in as admin to add departing flights.")
        return
    flight_no = input("Enter Flight Number: ")
    airlines = input("Enter Airlines: ")
    destination = input("Enter Destination: ")
    d_time = input("Enter Departure Time (YYYY-MM-DD HH:MM:SS): ")
    gate = input("Enter Gate: ")
    status = input("Enter Status (On Time / Delayed / Departed): ")
    try:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO departures (flight_no, airlines, destination, d_time, gate, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (flight_no, airlines, destination, d_time, gate, status))
        con.commit()
        print("Departing flight added.")
    except conn.Error as err:
        print("Error inserting departure:", err)
    finally:
        cur.close()

def departures():
    print("Welcome to the Departures Module!")
    print("1. View Departing Flights")
    print("2. Add Departing Flight")
    print("3. Delete Entry")
    try:
        choice = int(input("Your Choice: "))
    except ValueError:
        print("Invalid input!")
        return

    if choice == 1:
        view_departures()
    elif choice == 2:
        if not auth:
            if not admin():
                return
        add_dept()
    elif choice == 3:
        if not auth:
            if not admin():
                return
        flight_no = input("Enter Flight Number to delete: ")
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM departures WHERE flight_no = %s", (flight_no,))
            con.commit()
            print("Flight deleted.")
        except conn.Error as err:
            print("Error deleting flight:", err)
        finally:
            cur.close()
    else:
        print("Invalid option.")

def view_arrivals():
    try:
        cur = con.cursor()
        cur.execute("SELECT flight_no, airlines, origin, a_time, gate, status FROM arrivals")
        rows = cur.fetchall()
        cur.close()
        if not rows:
            print("No arrival flights found.")
            return
        table = PrettyTable()
        table.field_names = ["Flight No.", "Airlines", "Origin", "Arr Time", "Gate", "Status"]
        for r in rows:
            table.add_row(r)
        print(table)
    except conn.Error as err:
        print("Error viewing arrivals:", err)

def add_arrival():
    if not auth:
        print("You must be logged in as admin to add arrival flights.")
        return
    flight_no = input("Enter Flight Number: ")
    airlines = input("Enter Airline Name: ")
    origin = input("Enter Origin City: ")
    arrival_time = input("Enter Arrival Time (YYYY-MM-DD HH:MM:SS): ")
    gate = input("Enter Gate: ")
    status = input("Enter Status (On Time / Delayed / Landed): ")
    try:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO arrivals (flight_no, airlines, origin, a_time, gate, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (flight_no, airlines, origin, arrival_time, gate, status))
        con.commit()
        cur.close()
        print("Arrival flight added.")
    except conn.Error as err:
        print("Error inserting arrival:", err)

def delete_arrival():
    if not auth:
        print("You must be logged in as admin to delete arrival flights.")
        return
    flight_no = input("Enter Flight Number to delete: ")
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM arrivals WHERE flight_no = %s", (flight_no,))
        con.commit()
        cur.close()
        print(f"Arrival flight {flight_no} deleted.")
    except conn.Error as err:
        print("Error deleting arrival:", err)

def arrivals():
    print("=== Arrivals Module ===")
    print("1. View Arrival Flights")
    print("2. Add Arrival Flight")
    print("3. Delete Arrival Flight")
    try:
        choice = int(input("Your Choice: "))
    except ValueError:
        print("Invalid input!")
        return

    if choice == 1:
        view_arrivals()
    elif choice == 2:
        if not auth and not admin():
            return
        add_arrival()
    elif choice == 3:
        if not auth and not admin():
            return
        delete_arrival()
    else:
        print("Invalid option.")

def view_maintenance():
    try:
        cur = con.cursor()
        cur.execute("SELECT maint_id, runway_no, maint_date, status FROM runway_maintenance")
        rows = cur.fetchall()
        cur.close()
        if not rows:
            print("No runway maintenance records found.")
            return
        table = PrettyTable()
        table.field_names = ["ID", "Runway No.", "Date", "Status"]
        for r in rows:
            table.add_row(r)
        print(table)
    except conn.Error as err:
        print("Error viewing maintenance:", err)

def add_maintenance():
    if not auth and not admin():
        return
    runway_no = input("Enter Runway No. (e.g. 09L): ")
    maint_date = input("Enter Maintenance Date (YYYY-MM-DD): ")
    status = input("Enter Status (Scheduled / In Progress / Completed): ")
    try:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO runway_maintenance (runway_no, maint_date, status)
            VALUES (%s, %s, %s)
        """, (runway_no, maint_date, status))
        con.commit()
        cur.close()
        print("Maintenance record added.")
    except conn.Error as err:
        print("Error inserting maintenance:", err)

def delete_maintenance():
    if not auth and not admin():
        return
    mid = input("Enter Maintenance ID to delete: ")
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM runway_maintenance WHERE maint_id = %s", (mid,))
        con.commit()
        cur.close()
        print(f"Record {mid} deleted.")
    except conn.Error as err:
        print("Error deleting maintenance:", err)

def runway_maintenance_module():
    print("=== Runway Maintenance Module ===")
    print("1. View Records")
    print("2. Add Record")
    print("3. Delete Record")
    try:
        choice = int(input("Your Choice: "))
    except ValueError:
        print("Invalid input!")
        return

    if choice == 1:
        view_maintenance()
    elif choice == 2:
        add_maintenance()
    elif choice == 3:
        delete_maintenance()
    else:
        print("Invalid option.")

def jetfuel_module():
    print("\n--- Jet Fuel Management Module ---")
    print("1. View Fuel Records\n2. Add Fuel Record\n3. Delete Fuel Record")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    if choice == 1:
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM jetfuel")
            records = cur.fetchall()
            if not records:
                print("No fuel records found.")
                return
            table = PrettyTable(['Fuel ID', 'Flight No', 'Quantity (L)', 'Price (₹/L)', 'Total Cost', 'Fueling Time'])
            for row in records:
                table.add_row(row)
            print(table)
        except conn.Error as err:
            print("Error:", err)
        finally:
            cur.close()
    elif choice == 2:
        try:
            flight_no = input("Enter Flight Number: ")
            fuel_qty = float(input("Enter Fuel Quantity (in litres): "))
            price = float(input("Enter Price per Litre: "))
            total = fuel_qty * price
            fueling_time = input("Enter Fueling Time (YYYY-MM-DD HH:MM:SS): ")
            cur = con.cursor()
            cur.execute("""
                INSERT INTO jetfuel (flight_no, fuel_quantity, price, total, fueling_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (flight_no, fuel_qty, price, total, fueling_time))
            con.commit()
            cur.close()
            print("Fuel record added successfully!")
        except Exception as e:
            print("Error:", e)
    elif choice == 3:
        fuel_id = input("Enter Fuel ID to delete: ")
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM jetfuel WHERE fuel_id = %s", (fuel_id,))
            con.commit()
            cur.close()
            print("Record deleted successfully (if existed).")
        except conn.Error as err:
            print("Error deleting fuel record:", err)
    else:
        print("Invalid choice!")

def manage_passengers():
    print("\n====== Passenger Management ======")
    print("1. View All Passengers")
    print("2. Add a Passenger")
    print("3. Delete a Passenger")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    if choice == 1:
        cur = con.cursor()
        try:
            cur.execute("SELECT p_id, p_name, p_gender, p_flight_no, p_age, p_nationality FROM pax")
            rows = cur.fetchall()
            if not rows:
                print("No passenger records found.")
                return
            table = PrettyTable(["Passenger ID", "Name", "Gender", "Flight No", "Age", "Nationality"])
            for r in rows:
                table.add_row(r)
            print(table)
        except conn.Error as err:
            print("Error viewing passengers:", err)
        finally:
            cur.close()
    elif choice == 2:
        if not auth and not admin():
            return
        p_name = input("Enter Passenger Name: ")
        p_gender = input("Enter Gender (M/F/O): ")
        p_flight_no = input("Enter Flight Number: ")
        try:
            p_age = int(input("Enter Age: "))
        except ValueError:
            print("Invalid age entered.")
            return
        p_nationality = input("Enter Nationality: ")
        try:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO pax (p_name, p_gender, p_flight_no, p_age, p_nationality)
                VALUES (%s, %s, %s, %s, %s)
            """, (p_name, p_gender, p_flight_no, p_age, p_nationality))
            con.commit()
            cur.close()
            print("Passenger added successfully.")
        except conn.Error as err:
            print("Error inserting passenger:", err)
    elif choice == 3:
        if not auth and not admin():
            return
        pid = input("Enter Passenger ID to delete: ")
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM pax WHERE p_id = %s", (pid,))
            con.commit()
            cur.close()
            print(f"Passenger record {pid} deleted.")
        except conn.Error as err:
            print("Error deleting passenger:", err)
    else:
        print("Invalid choice!")

def main_menu():
    while True:
        print("\n========== AeroDB Airport Management ==========")
        print("1. Arrivals")
        print("2. Departures")
        print("3. Jet Fuel Management")
        print("4. Runway Maintenance")
        print("5. Passenger Management")
        print("6. Exit")
        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if choice == 1:
            arrivals()
        elif choice == 2:
            departures()
        elif choice == 3:
            jetfuel_module()
        elif choice == 4:
            runway_maintenance_module()
        elif choice == 5:
            manage_passengers()
        elif choice == 6:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1 to 6.")

create_tables()
main_menu()
con.close()