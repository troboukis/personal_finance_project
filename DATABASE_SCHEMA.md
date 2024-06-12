# Database Schema

## Tables

### `category_table`
- **category_id** (INTEGER, NOT NULL, UNIQUE): Ένα μοναδικό αναγνωριστικό για κάθε κατηγορία.
- **name** (TEXT): Το όνομα της κατηγορίας.
- **type** (INTEGER, NOT NULL): Αναφορά στον τύπο της κατηγορίας, που συνδέεται με τον πίνακα `type_table`.
- **Primary Key**: `category_id`
- **Foreign Key**: `type` references `type_table(type_id)`

### `expenses`
- **expenses_id** (INTEGER, NOT NULL, UNIQUE): Μοναδικό αναγνωριστικό για κάθε εγγραφή εξόδων.
- **date** (DATE): Η ημερομηνία της δαπάνης.
- **name** (TEXT): Η ονομασία ή η περιγραφή της δαπάνης.
- **amount** (INTEGER, NOT NULL): Το ποσό της δαπάνης.
- **frequency** (INTEGER, NOT NULL): Αναφορά στη συχνότητα της δαπάνης, συνδεδεμένη με τον πίνακα `frequency_table`.
- **category** (INTEGER, NOT NULL): Αναφορά στην κατηγορία της δαπάνης, συνδεδεμένη με τον πίνακα `category_table`.
- **Primary Key**: `expenses_id`
- **Foreign Keys**:
  - `frequency` references `frequency_table(freq_id)`
  - `category` references `category_table(category_id)`

### `frequency_table`
- **freq_id** (INTEGER, NOT NULL, UNIQUE): Ένα μοναδικό αναγνωριστικό για κάθε τύπο συχνότητας.
- **name** (TEXT): Το όνομα της συχνότητας (π.χ. μηνιαία, ετήσια).
- **Primary Key**: `name`

### `income`
- **income_id** (INTEGER, NOT NULL, UNIQUE): Μοναδικό αναγνωριστικό για κάθε καταχώρηση εσόδου.
- **date** (DATE): Η ημερομηνία του εσόδου.
- **name** (TEXT): Το όνομα ή η περιγραφή της πηγής εσόδου.
- **amount** (INTEGER, NOT NULL): Το ποσό του εσόδου.
- **frequency** (INTEGER, NOT NULL): Αναφορά στη συχνότητα του εισοδήματος, συνδεδεμένη με τον πίνακα `frequency_table`.
- **category** (INTEGER, NOT NULL): Αναφορά στην κατηγορία του εισοδήματος, που συνδέεται με τον πίνακα `category_table`.
- **Primary Key**: `income_id`
- **Foreign Keys**:
  - `frequency` references `frequency_table(freq_id)`
  - `category` references `category_table(category_id)`

### `type_table`
- **type_id** (INTEGER, NOT NULL, UNIQUE): Ένα μοναδικό αναγνωριστικό για κάθε τύπο κατηγορίας.
- **name** (TEXT): Το όνομα του τύπου (Έσοδο, Έξοδο).
- **Primary Key**: `type_id`