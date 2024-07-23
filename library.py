import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_date TEXT,
    isbn TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Borrowers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS BorrowingHistory (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    borrower_id INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES Books (id),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers (id)
)
''')

# Commit the changes and close the connection
conn.commit()

# Insert sample data into Books table
try:
    cursor.execute('''
    INSERT INTO Books (title, author, published_date, isbn)
    VALUES
    ('Data Structure', 'Srinivas', '1960-07-11', '978-0-06-112008-4'),
    ('Python', 'George Orwell', '1949-06-08', '978-0-452-28423-4'),
    ('Web programming', 'F. Scott Fitzgerald', '1925-04-10', '978-0-7432-7356-5')
    ''')
except sqlite3.IntegrityError as e:
    print(f"Error inserting data into Books table: {e}")

# Insert sample data into Borrowers table
try:
    cursor.execute('''
    INSERT INTO Borrowers (name, email)
    VALUES
    ('John Doe', 'john.doe@example.com'),
    ('Jane Smith', 'jane.smith@example.com')
    ''')
except sqlite3.IntegrityError as e:
    print(f"Error inserting data into Borrowers table: {e}")

# Insert sample data into BorrowingHistory table
try:
    cursor.execute('''
    INSERT INTO BorrowingHistory (book_id, borrower_id, borrow_date, return_date)
    VALUES
    (1, 1, '2024-07-01', '2024-07-15'),
    (2, 2, '2024-07-05', NULL)
    ''')
except sqlite3.IntegrityError as e:
    print(f"Error inserting data into BorrowingHistory table: {e}")

# Commit the changes
conn.commit()

# Query and display all books
cursor.execute('SELECT * FROM Books')
books = cursor.fetchall()
print("Books:")
for book in books:
    print(book)

# Query and display all borrowers
cursor.execute('SELECT * FROM Borrowers')
borrowers = cursor.fetchall()
print("\nBorrowers:")
for borrower in borrowers:
    print(borrower)

# Query and display borrowing history
cursor.execute('''
SELECT b.title, br.name, bh.borrow_date, bh.return_date
FROM BorrowingHistory bh
JOIN Books b ON bh.book_id = b.id
JOIN Borrowers br ON bh.borrower_id = br.id
''')
history = cursor.fetchall()
print("\nBorrowing History:")
for record in history:
    print(record)

# Close the connection
conn.close()
