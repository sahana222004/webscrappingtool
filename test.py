import sqlite3

def fetch_all_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()

fetch_all_books()  # Call to see all the scraped books in the database
