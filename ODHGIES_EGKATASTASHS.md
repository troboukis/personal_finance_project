# Οδηγίες Εγκαταστασης

### Κατεβάζουμε το πρόγραμμα από το `Github`
Για να κατεβάσετε ένα project από το GitHub, μπορείτε να ακολουθήσετε τα παρακάτω βήματα. 

#### Επισκεφθείτε τη σελίδα του Project
- Μεταβείτε στη σελίδα του GitHub repository `https://github.com/troboukis/personal_finance_project`.

#### Λήψη του Repository
- Κλικ στο κουμπί "Code" και επιλέξτε "Download ZIP".
- Αποθηκεύστε το αρχείο ZIP στον υπολογιστή σας και αποσυμπιέστε το.

### Εγκατάσταση του προγράμματος

Για να εγκαταστήσουμε το πρόγραμμα, θα πρέπει πρώτα να δημιουργήσουμε ένα εικονικό περιβάλλον ώστε να εγκαταστήσουμε τις απαραίτητες βιβλιοθήκες της Python. Παρακάτω θα παρουσιάσουμε τα βήματα για τη δημιουργία ενός εικονικού περιβάλλοντος με τη χρήση της βιβλιοθήκης ‘virtualenv’, περιγράφοντας οδηγίες τόσο για macOS όσο και για Windows.

#### Εγκατάσταση του `virtualenv`

1. **Άνοιξε το Terminal (macOS) ή Command Prompt (Windows).**
2. **Εκτέλεσε την παρακάτω εντολή:**
   ```bash
   pip install virtualenv
   ```

#### Δημιουργία Εικονικού Περιβάλλοντος

Μόλις ολοκληρωθεί η εγκατάσταση του `virtualenv`:

1. **Πλοηγούμαστε μέσω Terminal/Command Prompt στον φάκελο που θα αποθηκευτεί το πρόγραμμα χρησιμοποιώντας την εντολή αλλαγής καταλόγου cd. Το path/to/your/project είναι η διεύθυνση του φακέλου που θα αποθηκευτεί το πρόγραμμα.**

   ```bash
   cd path/to/your/project
   ```
2. **Δημιούργησε το εικονικό περιβάλλον με την εντολή:**
   ```bash
   virtualenv env
   ```
   Ως `env` ορίζουμε το όνομα του εικονικού περιβάλλοντος.

#### Ενεργοποίηση του Εικονικού Περιβάλλοντος

Για να ενεργοποιήσουμε το `env` ώστε να εγκαταστήσουμε τις βιβλιοθήκες θα τρέξουμε τις παρακάτω εντολές ενώ βρισκόμαστε μέσα στον φάκελο του πρότζεκτ.

**macOS:**
   ```bash
   source env/bin/activate
   ```

**Windows:**
   ```cmd
   .\env\Scripts\activate
   ```
Το περιβάλλον είναι ενεργοποιημένο εάν υπάρχει πρόθεμα με το όνομα του περιβάλλοντος σε παρένθεση στη γραμμή εντολών του Termina/Command Prompt. 

**macOS:**
   ```bash
   (env) username@hostname:~/path/to/project$
   ```

**Windows:**
   ```cmd
   (env) C:\Users\YourName\>
```

#### Εγκατάσταση Βιβλιοθηκών

**Εγκατέστησε τις εξαρτώμενες βιβλιοθήκες με την εντολή:**
   ```bash
   pip install -r requirements.txt
   ```

### Ανοίγουμε το πρόγραμμα
Για να ανοίξουμε το πρόγραμμα από το Terminal/Command Prompt θα πρέπει να τρέξουμε την παρακάτω εντολή:
``` bash
python main.py

**Εάν είστε σε υπολογιστή Mac ενδέχεται να υπάρξει το παρακάτω σφάλμα. 
`locale.Error: unsupported locale setting`.
Ανοίξτε το αρχείο που βρίσκεται στο `/Users/username/path_to_your_project/lib/your_python_version/site-packages/ttkbootstrap/dialogs/dialogs.py` και αντικαταστήστε στη γραμμή 566 τον εξής κώδικα `locale.setlocale(locale.LC_ALL, locale.setlocale(locale.LC_TIME, ""))` με αυτόν`locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')`. ***
