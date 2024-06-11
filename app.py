import sqlite3
import pandas as pd
import datetime
import os

new_db = f"{os.path.dirname(os.path.abspath(__file__))}/new_db.db"

# Βασική λίστα κατηγοριών εσόδων - εξόδων
income_list = ["Άλλα έσοδα", "Μισθός", "Είσπραξη ενοικίου", "Πωλήσεις", "Τόκοι τραπεζικών καταθέσεων", "Κέρδη από μετοχές", "Αποζημιώσεις", "Σύνταξη"]
expenses_list = ["Άλλα έξοδα", "Ενοίκια", "Τρόφιμα","Δαπάνες για ενέργεια", "Νερό", "Καύσιμα", "Τηλεπικοινωνίες", "Ασφάλειες", "Φόροι και τέλη", "Δόση δανείου", "Συντήρηση και επισκευές"]

def current_date():
    # Επιστροφή της τρέχουσας ημερομηνίας ως συμβολοσειρά
    return datetime.datetime.now().strftime("%Y-%m-%d")

def return_index(string, data):
    '''
    Επιστρέφει το index της κατηγορίας. 
    :string: η περιγραφή της κατηγορίας.
    :data: τα δεδομένα όπως έρχονται από το self.indb.showData() π.χ. self.indb.showData('category_table')
    '''
    for item in data:
        if string == item[1]:
            return item[0]
    return 0
        
def unstuck_frequency(text):
    '''
    Συνάρτηση που επιστρέφει το index της συχνότητας όταν λαμβάνει ως όρισμα string με την περιγραφή της συχνότητας.
    :text: string με την περιγραφή της συχνότητας εσόδου - εξόδου
    '''
    if text=='Έκτακτο':
        return 2
    elif text == "Ετήσιο":
        return 1
    elif text =="Μηνιαίο":
        return 0
    
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

# Λίστα με τις εντολές της SQL
commands = [type_sql, freq_sql, category_sql, income_sql, expenses_sql]

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.date = current_date()
        self.cursor = None

    def __enter__(self):
        '''Είσοδος στη βάση δεδομένων'''
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON;')
            print("Συνδεθήκατε στη βάση δεδομένων.")
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Έξοδος από τη βάση δεδομένων '''
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn=None

    def create_table(self, sql_command):
        '''Δημιουργία πίνακα
        :sql_commant: η εντολή της SQL
        '''
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
    
    def get_all_data(self):
        ''' Επιστρέφει όλα τα έξοδα και τα έσοδα'''
        try:
            data1 = pd.DataFrame(self.printData("income"))
            data2 = pd.DataFrame(self.printData("expenses"))
            df = pd.concat([data1, data2])
            df=df[[1, 10, 2, 3, 9, 7]].copy()
            df.columns=['Ημερομηνία', 'Τύπος', 'Περιγραφή', 'Ποσό', 'Κατηγορία', 'Συχνότητα']
            df['Τύπος'] = df['Τύπος'].replace(0, 'Έξοδο').replace(1, 'Έσοδο')

            df['Ημερομηνία'] = pd.to_datetime(df['Ημερομηνία'])

            df = df.sort_values(by="Ημερομηνία").reset_index(drop=True).copy()
            df.to_csv("all_data.csv", index=False)
            return df
        except:
            return pd.DataFrame({
    'Ημερομηνία': current_date(),  # or np.nan if you prefer
    'Τύπος': [None],
    'Περιγραφή': [None],
    'Ποσό': [0],
    'Κατηγορία': [None],
    'Συχνότητα': [None]
})
    
    def printData(self, table):
        '''
        Επιστρέφει τα δεδομένα της βάσης δεδομένων. 
        :table: Ο πίνακας που θέλουμε να εμφανίσουμε
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
        self.__exit__(None, None, None)
        return data

    def showData(self, table, dataframe=False):
        '''
        Επιστρέφει τα δεδομένα της βάσης δεδομένων
        :table: ο πίνακας που θέλουμε να πάρουμε τα δεδομένα.
        :dataframe: Boolean μεταβλητή για το εάν θέλουμε να λάβουμε pandas dataframe ή όχι
        '''
        self.__enter__()
        parameter = f"SELECT * FROM {table}" 
        self.cursor.execute(parameter)
        data = self.cursor.fetchall()
        if not dataframe:
            return data
        else:
            columns = [description[0] for description in self.cursor.description]
            # Δημιουργία Pandas DataFrame
            df = pd.DataFrame(data, columns=columns)
            self.__exit__(None, None, None)
            return df



    def initializeTable(self, sql_code, table_name, column1, column2, value1, value2):
        ''' Αρχικοποιεί τους πίνακες για συχνότητα και τύπο εγγραφής
        π.χ  db.initializeTable(freq_sql, 'frequency_table', 'freq_id', 'name', 0, 'Μηνιαίο')
        :sql_code: Το σκριπτ της SQL 
        :table_name:ο πίνακας που θέλουμε να αρχικοποιήσουμε
        :column1:το όνομα της πρώτης στήλης (π.χ. name)
        :column2: το όνομα της δεύτερης στήλης (π.χ. frequency_id)
        :value1: η τιμή της πρώτης στήλης
        :value2: η τιμή της δεύτερης στήλης
        '''
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
        

    def GetCategoryIndex(self, category_term):
        existing_categories = [cat for cat in self.showData('category_table', dataframe=False)]
        for category in existing_categories:
            if category_term == category[1]:
                return category[0]

        
    def InsertCategory(self, category_name):
        """
        Εισάγει μια νέα κατηγορία στον πίνακα 'category_table'. 
        Η μέθοδος ζητά από τον χρήστη να καθορίσει εάν η νέα κατηγορία είναι έσοδο (1) ή έξοδο (0), και στη συνέχεια το όνομα της κατηγορίας. 
        Στη συνέχεια, προσπαθεί να εισάγει αυτές τις τιμές στη βάση δεδομένων. Εάν η εισαγωγή είναι επιτυχής, εκτυπώνει μήνυμα επιτυχίας. Σε περίπτωση που εμφανιστεί σφάλμα, εκτυπώνει το σχετικό μήνυμα.
        :category_name: το όνομα της κατηγορίας
        """
        # Σύνδεση στη βάση
        self.__enter__()  # Ensure the connection is open

        # Ελέγχουμε τις υπάρχουσες κατηγορίες για να δούμε εάν υπάρχει ήδη η κατηγορία που προσπαθούμε να περάσουμε
        existing_categories = [cat[1] for cat in self.showData('category_table', dataframe=False)]
        if category_name in existing_categories:
            print(f"Η κατηγορία εσόδων που προσπαθείτε να εισάγετε υπάρχει ήδη.")
            self.__exit__(None, None, None)

            return 0

        # Καταχώρηση νέας κατηγορίας
        else:
            insert_query = "INSERT INTO category_table (name, type) VALUES (?, ?)"
            try:
                if category_name in income_list:
                    self.cursor.execute(insert_query, (category_name, 1))  # 
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
        '''
        Ανάκτηση του id της εγγραφής εσόδου
        :or_description: H περιγραφή της εγγραφής όπως έχει μπει από τον χρήστη
        :or_date: Ημερομηνία
        :or_amount: Ποσό
        '''
        self.__enter__()  # Ensure the connection is open

        self.cursor.execute("""
            SELECT income_id
            FROM income
            WHERE name = ? AND date = ? AND amount = ?;
        """, (or_description, or_date, or_amount))
        
        record_id = self.cursor.fetchone()
        
        if not record_id:
            print("Δεν βρέθηκε εγγραφή που να ταιριάζει με τα κριτήρια.")
            self.__exit__(None, None, None)
            return
        else:
            self.__exit__(None, None, None)
            return record_id
        
    def GetExpensesID(self, or_description, or_date, or_amount):
        '''
        Ανάκτηση του id της εγγραφής εξόδου
        :or_description: H περιγραφή της εγγραφής όπως έχει μπει από τον χρήστη
        :or_date: Ημερομηνία
        :or_amount: Ποσό
        '''
        self.__enter__()  # Ensure the connection is open

        self.cursor.execute("""
            SELECT expenses_id
            FROM expenses
            WHERE name = ? AND date = ? AND amount = ?;
        """, (or_description, or_date, or_amount))
        
        record_id = self.cursor.fetchone()
        
        if not record_id:
            print("Δεν βρέθηκε εγγραφή που να ταιριάζει με τα κριτήρια.")
            self.__exit__(None, None, None)
            return
        else:
            self.__exit__(None, None, None)
            return record_id
        
    def UpdateIncome(self, n_description, n_date, n_amount, n_frequency, n_category, id):

        self.__enter__()

        self.cursor.execute("""
            UPDATE income
            SET name = ?, date = ?, amount = ?, frequency = ?, category = ?
            WHERE income_id = ?;
        """, (n_description, n_date, n_amount, n_frequency, n_category, id))
        
        self.conn.commit()
        print("Income record updated successfully, ID:", id)
        self.__exit__(None, None, None)

    def UpdateExpenses(self, n_description, n_date, n_amount, n_frequency, n_category, id):
        self.__enter__()

        self.cursor.execute("""
            UPDATE expenses
            SET name = ?, date = ?, amount = ?, frequency = ?, category = ?
            WHERE expenses_id = ?;
        """, (n_description, n_date, n_amount, n_frequency, n_category, id))
        
        self.conn.commit()
        print("Η εγγραφή εξόδων ενημερώθηκε επιτυχώς, ID:", id)
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
            print(f"Η εγγραφή εσόδων διαγράφηκε επιτυχώς, ID: {income_id}")

        except Exception as e:
            print(f"Σφάλμα: {e}")
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

        except Exception as e:
            print(f"Σφάλμα: {e}")
            self.conn.rollback()  # Rollback the transaction in case of error

        finally:
            self.__exit__(None, None, None)  # Ensure resources are cleaned up properly

    
    def AddCategory(self, category_name, category_type):
        """
        Προσθέτει μια νέα κατηγορία στον πίνακα 'category_table'.
    
        :param category_name: Το όνομα της νέας κατηγορίας.
        :param category_type: Ο τύπος της κατηγορίας (π.χ. έξοδα ή έσοδα).
        """
        self.__enter__()
        try:
            # Ελέγχος αν η κατηγορία υπάρχει ήδη με τον ίδιο τύπο
            check_query = "SELECT EXISTS(SELECT 1 FROM category_table WHERE name = ? AND type = ?)"
            self.cursor.execute(check_query, (category_name, category_type))
            exists = self.cursor.fetchone()[0]

            if exists:
                return f"Η κατηγορία '{category_name}' με τύπο '{category_type}' υπάρχει ήδη."

            # Προσθήκη της νέας κατηγορίας
            insert_query = "INSERT INTO category_table (name, type) VALUES (?, ?)"
            self.cursor.execute(insert_query, (category_name, category_type))
            self.conn.commit()
            return f"Η κατηγορία '{category_name}' προστέθηκε επιτυχώς."
        except sqlite3.IntegrityError as e:
            return f"Παρουσιάστηκε σφάλμα στη Βάση Δεδομένων: {e}"
        except Exception as e:
            return f"Σφάλμα: {e}"
        finally:
            self.__exit__(None, None, None)
           
       
    def DeleteCategory(self, category_name, category_type, force=False):
        """
        Διαγράφει μια κατηγορία από τον πίνακα 'category_table'.
        
        :param category_name: Το όνομα της κατηγορίας που θα διαγραφεί.
        :param category_type: Ο τύπος της κατηγορίας (π.χ. έξοδα ή έσοδα).
        :param force: Εάν True, διαγράφει την κατηγορία ακόμα και αν χρησιμοποιείται σε συναλλαγές. Προεπιλογή είναι False.
        """
        self.__enter__()
        try:
            # Διαγραφή της κατηγορίας
            delete_query = "DELETE FROM category_table WHERE name = ? AND type = ?"
            self.cursor.execute(delete_query, (category_name, category_type))
            
            self.conn.commit()
            return f"Η κατηγορία '{category_name}' διαγράφηκε επιτυχώς."
        except sqlite3.IntegrityError as e:
            return f"Η κατηγορία δεν μπορεί να διαγραφεί διότι χρησιμοποιείται."
        except Exception as e:
            return f"Σφάλμα: {e}"
        finally:
            self.__exit__(None, None, None)