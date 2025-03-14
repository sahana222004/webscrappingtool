import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to fetch the webpage content
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors (4xx, 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

# Function to parse the book data
def parse_books(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    books = []
    
    # Loop through each book on the page and extract data
    for book in soup.find_all('article', class_='product_pod'):
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').text
        rating = book.find('p', class_='star-rating')['class'][1]  # Rating is in the class name
        book_url = book.find('h3').find('a')['href']
        
        # Save data to list
        books.append((title, price, rating, book_url))
    
    return books

# Function to store data in the database
def save_data_to_db(data):
    # Connect to SQLite (or create database)
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    # Create the books table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        title TEXT,
        price TEXT,
        rating TEXT,
        url TEXT
    )''')
    
    # Insert the data
    cursor.executemany('''
    INSERT INTO books (title, price, rating, url)
    VALUES (?, ?, ?, ?)
    ''', data)
    
    conn.commit()  # Commit changes
    conn.close()  # Close the connection

# Main function to scrape and store data
def scrape_books():
    url = 'http://books.toscrape.com'
    page_content = fetch_page(url)
    
    if page_content:
        # Parse the books data
        books = parse_books(page_content)
        # Save the data to the database
        save_data_to_db(books)
        print(f"Successfully saved {len(books)} books to the database.")
    else:
        print("Failed to retrieve page content.")

# Run the script
if __name__ == "__main__":
    scrape_books()
