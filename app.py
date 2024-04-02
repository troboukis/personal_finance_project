import numpy as np
import json
import sqlite3
import pandas as pd

def prettify_data(rows):
    category_dict = {}
    for row in rows:
        # Using 'id' as the key, and storing 'name' and 'type' in a sub-dictionary
        category_dict[row[0]] = {'name': row[1], 'type': row[2]}
    return category_dict
    
type_sql = '''
    CREATE TABLE IF NOT EXISTS type_table (
        type_id INTEGER NOT NULL UNIQUE, 
        name TEXT,
        PRIMARY KEY(type_id)
    )
    '''
freq_sql = '''
    CREATE TABLE IF NOT EXISTS frequency_table (
            freq_id INTEGER NOT NULL UNIQUE,
            name TEXT,
            PRIMARY KEY(name)
        )
'''

category_sql = '''
    CREATE TABLE IF NOT EXISTS category_table (
        category_id INTEGER NOT NULL UNIQUE,
        name TEXT,
        type INTEGER NOT NULL,
        PRIMARY KEY(category_id AUTOINCREMENT),
        FOREIGN KEY(type) REFERENCES type_table(type_id)
    )
    '''
records_sql = '''
    CREATE TABLE IF NOT EXISTS records (
        records_id INTEGER NOT NULL UNIQUE,
        name TEXT,
        type INTEGER NOT NULL,
        frequency INTEGER NOT NULL,
        category INTEGER NOT NULL,
        PRIMARY KEY(records_id),
        FOREIGN KEY(type) REFERENCES type_table(type_id)
        FOREIGN KEY(frequency) REFERENCES frequency_table(freq_id)
        FOREIGN KEY(category) REFERENCES category_table(category_id)
    )
    '''

commands = [type_sql, freq_sql, category_sql, records_sql]
new_db = "/Users/troboukis/Code/EAP/PLHPRO/final-project/FINANCE-DATABASE/new_db.db"

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON;')
        print("Συνδεθήκατε στη βάση δεδομένων.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def create_table(self, sql_command):
        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.cursor.execute(sql_command)
        self.conn.commit()

    def get_index(self, table_name, column_name, category_name):
        """
        Retrieves the ID for a given category name from the specified table.
        
        :param table_name: The name of the table to search.
        :param column_name: The name of the ID column to retrieve.
        :param category_name: The category name to search for.
        """
        # Validate or sanitize table_name and column_name if necessary
        allowed_tables = {"category_table": ["category_id"]}
        if table_name in allowed_tables and column_name in allowed_tables[table_name]:
            query = f"SELECT {column_name} FROM {table_name} WHERE name = ?"
            self.cursor.execute(query, (category_name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                print(f"No category found with the name '{category_name}'.")
                return None
        else:
            raise ValueError("Invalid table name or column name specified.")

class showDatabase(DatabaseConnection):
    def __init__(self, db_path):
        super().__init__(db_path)
    
    def get_tables(self):
        '''
        Επιστρέφει τα ονόματα των πινάκων της βάσης δεδομένων.
        '''
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cursor.fetchall()
        list_tables = [table[0] for table in self.tables]
        return list_tables
        

    def showData(self, table, dataframe=False):
        '''
        Επιστρέφει τα δεδομένα της βάσης δεδομένων. Εάν columns=True, τότε επιστρέφει ένα πλαίσιο δεδομένων. Διαφορετικά επιστρέφει ένα λεξικό.
        '''
        parameter = f"SELECT * FROM {table}"
        self.cursor.execute(parameter)
        data = self.cursor.fetchall()
        if not dataframe:
            return prettify_data(data)
        else:
            columns = [description[0] for description in self.cursor.description]
            # Use pandas DataFrame for prettifying and easy manipulation of data and column names
            df = pd.DataFrame(data, columns=columns)
            return df

class enterRecords(DatabaseConnection):
    def __init__(self, db_path):
        super().__init__(db_path)
    
    def open_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON;')
            print("Συνδεθήκατε στη βάση δεδομένων.")

    def close_connection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            print("Αποσυνδεθήκατε από τη βάση δεδομένων.")

    def insert_category(self):
        self.open_connection()  # Ensure the connection is open
        type_id = int(input("Πατήστε '0' εάν η νέα κατηγορία είναι έξοδο και '1' εάν είναι έσοδο. "))
        if type_id == 0:
            name = input("Εισάγετε την κατηγορία εσόδου.")
        else:
            name = input("Εισάγετε την κατηγορία εξόδου.")
        insert_query = '''INSERT INTO category_table (name, type) VALUES (?, ?)'''
        try:
            self.cursor.execute(insert_query, (name, type_id))
            self.conn.commit()  # Commit changes to the database
            print("Η κατηγορία εισήχθη επιτυχώς.")
            return name
        except sqlite3.IntegrityError as e:
            print("Εμφανίστηκε σφάλμα:", e)
        finally:
            self.close_connection()  # Close the connection when done

    def insert_record(self, categ_id, freq_id, type_id):
        self.open_connection()  # Ensure the connection is open
        if type_id == 0:
            name = input("Εισάγετε τo έσοδο.")
        else:
            name = input("Εισάγετε το έξοδο.")
        insert_query = '''INSERT INTO records (name, type, frequency, category) VALUES (?, ?, ?, ?)'''
        try:
            self.cursor.execute(insert_query, (name, type_id, freq_id, categ_id))
            self.conn.commit()  # Commit changes to the database
            print("Η εγγραφή εισήχθη επιτυχώς.")
        except sqlite3.IntegrityError as e:
            print("Εμφανίστηκε σφάλμα:", e)
        finally:
            self.close_connection()  # Close the connection when done