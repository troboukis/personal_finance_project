import sqlite3
import pandas as pd
import datetime
# from expenses import ExpensesFrame
# from income import IncomeFrame
            
new_db = "/Users/troboukis/Code/EAP/PLHPRO/final-project/FINANCE-DATABASE/new_db.db"

income_list = ["Μισθός", "Ενοίκια", "Πωλήσεις", "Τόκοι τραπεζικών καταθέσεων", "Δικαιώματα πνευματικής ιδιοκτησίας", "Κέρδη από μετοχές", "Αποζημιώσεις", "Συντάξεις", "Παροχές από ασφαλιστικά ταμεία", "Επιδοτήσεις", "Εισοδήματα από freelance εργασίες", "Άλλα έκτακτα έσοδα", "Πρόσθεσε νέο έσοδο"]
expenses_list = ["Μισθοδοσία προσωπικού", "Ενοίκια για επαγγελματικές στεγάσεις", "Αγορές αγαθών", "Κόστος υπηρεσιών", "Διαφημιστικές δαπάνες", "Τηλεπικοινωνίες", "Δαπάνες για ενέργεια (ηλεκτρισμός, νερό, καύσιμα)", "Ασφάλειες", "Φόροι και τέλη", "Διοικητικά έξοδα", "Ταξιδιωτικά έξοδα", "Δαπάνες για αυτοκίνητα και μεταφορικά μέσα", "Τόκοι δανείων", "Συντήρηση και επισκευές", "Έξοδα νομικών υπηρεσιών και συμβούλων", "Άλλα έξοδα λειτουργίας", "Πρόσθεσε νέο έξοδο"]

def current_date():
    # Return the current date as a string
    return datetime.datetime.now().strftime("%Y-%m-%d")

def return_index(string, data):
    for item in data:
        if string == item[1]:
            return item[0]
    return 12
        
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
income_sql = '''
    CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER NOT NULL UNIQUE,
        date DATE,
        name TEXT,
        amount INTEGER NOT NULL,
        frequency INTEGER NOT NULL,
        category INTEGER NOT NULL,
        PRIMARY KEY(income_id),
        FOREIGN KEY(frequency) REFERENCES frequency_table(freq_id),
        FOREIGN KEY(category) REFERENCES category_table(category_id)
    )
    '''

expenses_sql = '''
    CREATE TABLE IF NOT EXISTS expenses (
        expenses_id INTEGER NOT NULL UNIQUE,
        date DATE,
        name TEXT,
        amount INTEGER NOT NULL,
        frequency INTEGER NOT NULL,
        category INTEGER NOT NULL,
        PRIMARY KEY(expenses_id),
        FOREIGN KEY(frequency) REFERENCES frequency_table(freq_id),
        FOREIGN KEY(category) REFERENCES category_table(category_id)
    )
    '''

commands = [type_sql, freq_sql, category_sql, income_sql, expenses_sql]
new_db = "/Users/troboukis/Code/EAP/PLHPRO/final-project/FINANCE-DATABASE/new_db.db"

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.date = current_date()
        self.cursor = None

    def __enter__(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON;')
            print("Συνδεθήκατε στη βάση δεδομένων.")
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn=None

    def create_table(self, sql_command):
        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.cursor.execute(sql_command)
        self.conn.commit()


    def get_tables(self):
        '''
        Επιστρέφει τα ονόματα των πινάκων της βάσης δεδομένων.
        '''
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cursor.fetchall()
        list_tables = [table[0] for table in self.tables]
        return list_tables
    
    def printData(self, table):
        '''
        Επιστρέφει τα δεδομένα της βάσης δεδομένων. Εάν columns=True, τότε επιστρέφει ένα πλαίσιο δεδομένων. Διαφορετικά επιστρέφει ένα λεξικό.
        '''
        self.__enter__()
        parameter = f'''
        SELECT *
        FROM {table} AS t
        INNER JOIN frequency_table AS f ON t.frequency = f.freq_id
        INNER JOIN category_table AS c ON t.category = c.category_id;
        '''
        self.cursor.execute(parameter)
        data = self.cursor.fetchall()
        return data

    def showData(self, table, dataframe=False):
        '''
        Επιστρέφει τα δεδομένα της βάσης δεδομένων. Εάν columns=True, τότε επιστρέφει ένα πλαίσιο δεδομένων. Διαφορετικά επιστρέφει ένα λεξικό.
        '''
        self.__enter__()
        parameter = f"SELECT * FROM {table}" # SELECT * FROM {table} JOIN frequency_table ON freq_id = frequency
        
        self.cursor.execute(parameter)
        data = self.cursor.fetchall()
        if not dataframe:
            return data
        else:
            columns = [description[0] for description in self.cursor.description]
            # Use pandas DataFrame for prettifying and easy manipulation of data and column names
            df = pd.DataFrame(data, columns=columns)
            self.__exit__(None, None, None)
            return df



    def initializeTable(self, sql_code, table_name, column1, column2, value1, value2):
        ''' Αρχικοποιοεί τους πίνακες για συχνότητα και τύπο εγγραφής'''
        try:
            self.create_table(sql_code)  # Assuming this is correctly defined to execute the SQL command
            # Proper SQL string format with table and column names inserted directly (vulnerable to SQL injection if variables are not controlled)
            insert_query = f"INSERT INTO {table_name} ({column1}, {column2}) VALUES (?, ?)"
            self.cursor.execute(insert_query, (value1, value2))
            self.conn.commit()  # Commit changes to the database
            print("Η κατηγορία εισήχθη επιτυχώς.")
            
        except sqlite3.IntegrityError as e:
            print("Εμφανίστηκε σφάλμα:", e)


class Income(DatabaseConnection):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.income_id=None
        self.name=None
        self.category_name = None
        self.frequency=None
        self.category=None

    def InsertCategory(self, category_name):
        """
        Εισάγει μια νέα κατηγορία στον πίνακα 'category_table'. 
        Η μέθοδος ζητά από τον χρήστη να καθορίσει εάν η νέα κατηγορία είναι έσοδο (1) ή έξοδο (0), και στη συνέχεια το όνομα της κατηγορίας. 
        Στη συνέχεια, προσπαθεί να εισάγει αυτές τις τιμές στη βάση δεδομένων. Εάν η εισαγωγή είναι επιτυχής, εκτυπώνει μήνυμα επιτυχίας. Σε περίπτωση 
        που εμφανιστεί σφάλμα, εκτυπώνει το σχετικό μήνυμα.
        """
        # ΣΥΝΔΕΣΗ ΣΤΗ ΒΑΣΗ
        self.__enter__()  # Ensure the connection is open

        # ΕΛΕΓΧΟΣ ΤΩΝ ΥΠΑΡΧΟΝΤΩΝ ΚΑΤΗΓΟΡΙΩΝ
        existing_categories = [cat[1] for cat in self.showData('category_table', dataframe=False)]
        if category_name in existing_categories:
            print(f"Η κατηγορία εσόδων που προσπαθείτε να εισάγετε υπάρχει ήδη.")
            self.__exit__(None, None, None)

            return 0

        # ΚΑΤΑΧΩΡΗΣΗ ΝΕΑΣ ΚΑΤΗΓΟΡΙΑΣ
        else:
            insert_query = "INSERT INTO category_table (name, type) VALUES (?, ?)"
            try:
                if category_name in income_list:
                    self.cursor.execute(insert_query, (category_name, 1))  # Correctly using placeholders
                    self.conn.commit()  # Commit changes to the database
                    print(f"Η κατηγορία {category_name} εισήχθη επιτυχώς.")
                else:
                    self.cursor.execute(insert_query, (category_name, 0))  # Correctly using placeholders
                    self.conn.commit()  # Commit changes to the database
                    print(f"Η κατηγορία {category_name} εισήχθη επιτυχώς.")
                
            except sqlite3.IntegrityError as e:
                print("Εμφανίστηκε σφάλμα:", e)
            finally:
                self.__exit__(None, None, None)  # Close the connection when done



    def InsertIncome(self, income_description, amount, category_id, date, frequency_id):
        """
        Εισάγει μια νέα εγγραφή στον πίνακα 'records'. Η μέθοδος αρχικά ζητά από τον χρήστη να εισάγει το έσοδο ή το έξοδο 
        βάσει του τύπου της εγγραφής (0 για έξοδο, 1 για έσοδο). Στη συνέχεια, προσπαθεί να εισάγει την εγγραφή με τα δοθέντα 
        στοιχεία στη βάση δεδομένων. Εάν η εισαγωγή είναι επιτυχής, εκτυπώνει μήνυμα επιτυχίας. Σε περίπτωση σφάλματος 
        της βάσης δεδομένων, εκτυπώνει το αντίστοιχο μήνυμα.

        :param categ_id: Το ID της κατηγορίας όπου ανήκει η εγγραφή. Αντιστοιχεί σε μια υπάρχουσα εγγραφή στον πίνακα 'category_table'.
        :param freq_id: Το ID της συχνότητας με την οποία συμβαίνει η εγγραφή (π.χ., μηνιαία, ετήσια). Αντιστοιχεί σε μια υπάρχουσα εγγραφή στον πίνακα 'frequency_table'.
        :param type_id: Ο τύπος της εγγραφής (0 για έξοδο, 1 για έσοδο), καθορίζοντας αν αυτή είναι έσοδο ή έξοδο.
        """
        self.__enter__()  # Βεβαιωθείτε ότι η σύνδεση είναι ανοιχτή
        insert_query = '''INSERT INTO income (name, amount , category, date, frequency) VALUES (?, ?, ?, ?, ?)'''
        try:
            self.cursor.execute(insert_query, (income_description, amount, category_id, date, frequency_id))
            self.conn.commit()  # Δέσμευση αλλαγών στη βάση δεδομένων
            print(f"Η εγγραφή {income_description} εισήχθη επιτυχώς.")
        except sqlite3.IntegrityError as e:
            print("Εμφανίστηκε σφάλμα:", e)
        finally:
            self.__exit__(None, None, None)  # Κλείστε τη σύνδεση όταν τελειώσετε
            print("Aποσυνδεθήκατε από τη βάση δεδομένων")

    def InsertExpense(self, expense_description, amount, category_id, date, frequency_id):
        """
        Εισάγει μια νέα εγγραφή στον πίνακα 'records'. Η μέθοδος αρχικά ζητά από τον χρήστη να εισάγει το έσοδο ή το έξοδο 
        βάσει του τύπου της εγγραφής (0 για έξοδο, 1 για έσοδο). Στη συνέχεια, προσπαθεί να εισάγει την εγγραφή με τα δοθέντα 
        στοιχεία στη βάση δεδομένων. Εάν η εισαγωγή είναι επιτυχής, εκτυπώνει μήνυμα επιτυχίας. Σε περίπτωση σφάλματος 
        της βάσης δεδομένων, εκτυπώνει το αντίστοιχο μήνυμα.

        :param categ_id: Το ID της κατηγορίας όπου ανήκει η εγγραφή. Αντιστοιχεί σε μια υπάρχουσα εγγραφή στον πίνακα 'category_table'.
        :param freq_id: Το ID της συχνότητας με την οποία συμβαίνει η εγγραφή (π.χ., μηνιαία, ετήσια). Αντιστοιχεί σε μια υπάρχουσα εγγραφή στον πίνακα 'frequency_table'.
        :param type_id: Ο τύπος της εγγραφής (0 για έξοδο, 1 για έσοδο), καθορίζοντας αν αυτή είναι έσοδο ή έξοδο.
        """
        self.__enter__()  # Βεβαιωθείτε ότι η σύνδεση είναι ανοιχτή
        insert_query = '''INSERT INTO expenses (name, amount , category, date, frequency) VALUES (?, ?, ?, ?, ?)'''
        try:
            self.cursor.execute(insert_query, (expense_description, amount, category_id, date, frequency_id))
            self.conn.commit()  # Δέσμευση αλλαγών στη βάση δεδομένων
            print(f"Η εγγραφή {expense_description} εισήχθη επιτυχώς.")
        except sqlite3.IntegrityError as e:
            print("Εμφανίστηκε σφάλμα:", e)
        finally:
            self.__exit__(None, None, None)  # Κλείστε τη σύνδεση όταν τελειώσετε
            print("Aποσυνδεθήκατε από τη βάση δεδομένων")
    
    def GetID(self, or_description, or_date, or_amount):
        self.__enter__()  # Ensure the connection is open

        self.cursor.execute("""
            SELECT income_id
            FROM income
            WHERE name = ? AND date = ? AND amount = ?;
        """, (or_description, or_date, or_amount))
        
        record_id = self.cursor.fetchone()
        
        if not record_id:
            print("No record found matching the criteria.")
            self.__exit__(None, None, None)
            return
        else:
            self.__exit__(None, None, None)
            return record_id
        
    def GetExpensesID(self, or_description, or_date, or_amount):
        self.__enter__()  # Ensure the connection is open

        self.cursor.execute("""
            SELECT expenses_id
            FROM expenses
            WHERE name = ? AND date = ? AND amount = ?;
        """, (or_description, or_date, or_amount))
        
        record_id = self.cursor.fetchone()
        
        if not record_id:
            print("No record found matching the criteria.")
            self.__exit__(None, None, None)
            return
        else:
            self.__exit__(None, None, None)
            return record_id
        
    def UpdateIncome(self, n_description, n_date, n_amount, id):
        self.__enter__()

        self.cursor.execute("""
            UPDATE income
            SET name = ?, date = ?, amount = ?
            WHERE income_id = ?;
        """, (n_description, n_date, n_amount, id))
        
        self.conn.commit()
        print("Income record updated successfully, ID:", id)
        self.__exit__(None, None, None)

    def UpdateExpenses(self, n_description, n_date, n_amount, id):
        self.__enter__()

        self.cursor.execute("""
            UPDATE expenses
            SET name = ?, date = ?, amount = ?
            WHERE expenses_id = ?;
        """, (n_description, n_date, n_amount, id))
        
        self.conn.commit()
        print("Expenses record updated successfully, ID:", id)
        self.__exit__(None, None, None)

    def DeleteIncome(self, income_id):
        self.__enter__()  # Start transaction or acquire database resources

        try:
            # Execute the DELETE SQL command
            self.cursor.execute("""
                DELETE FROM income
                WHERE income_id = ?;
            """, (income_id,))

            self.conn.commit()  # Commit the transaction
            print(f"Income record deleted successfully, ID: {income_id}")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()  # Rollback the transaction in case of error

        finally:
            self.__exit__(None, None, None)  # Ensure resources are cleaned up properly

    def DeleteExpense(self, expense_id):
        self.__enter__()  # Start transaction or acquire database resources

        try:
            # Execute the DELETE SQL command
            self.cursor.execute("""
                DELETE FROM expenses
                WHERE expenses_id = ?;
            """, (expense_id,))

            self.conn.commit()  # Commit the transaction
            print(f"Expense record deleted successfully, ID: {expense_id}")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()  # Rollback the transaction in case of error

        finally:
            self.__exit__(None, None, None)  # Ensure resources are cleaned up properly


    def UpdateCategory(self):
        pass

        
    def DeleteCategory(self):
        pass

    def DeleteRecord(self):
        pass

class Expenses(DatabaseConnection):
    def __init__(self, db_path):
        super().__init__(db_path)
        pass