import json
import os
import re
import sqlite3
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO)

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['pages']

def normalize_text(text):
    """Normalize text by converting to lowercase."""
    return text.lower() 

def database_exists(db_file='articles.db'):
    """Check if the SQLite database file exists."""
    return os.path.isfile(db_file)

def create_database(data, db_file='articles.db'):
    """Create a SQLite database and an FTS table."""
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create FTS virtual table
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING FTS5(
        page_number,
        text
    );
    """)
    
    # Insert data into the FTS table
    for page in data:
        normalized_text = normalize_text(page['text'])
        cursor.execute("INSERT INTO articles_fts (page_number, text) VALUES (?, ?)",
                       (page['page_number'], normalized_text))
        logging.info(f"Indexed page {page['page_number']} with text: {normalized_text[:50]}...")  # Log the first 50 characters
    
    conn.commit()
    conn.close()
    logging.info("Database creation and data insertion complete.")

def update_database(data, db_file='articles.db'):
    """Update the existing SQLite database with new data."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a set of existing page numbers
    cursor.execute("SELECT page_number FROM articles_fts")
    existing_pages = {row[0] for row in cursor.fetchall()}

    for page in data:
        normalized_text = normalize_text(page['text'])
        if page['page_number'] not in existing_pages:
            cursor.execute("INSERT INTO articles_fts (page_number, text) VALUES (?, ?)",
                           (page['page_number'], normalized_text))
            logging.info(f"Added new page {page['page_number']} with text: {normalized_text[:50]}...")  # Log the first 50 characters
        #else:
            #logging.info(f"Page {page['page_number']} already exists. Skipping.")

    conn.commit()
    conn.close()
    logging.info("Database update complete.")

def highlight_keywords(text, query):
    """Highlight keywords in the text using ANSI escape codes."""
    normalized_query = query.strip().lower()
    highlight_start = "\033[93m"  # Yellow text
    highlight_end = "\033[0m"  # Reset to default

    highlighted_text = re.sub(f"({re.escape(normalized_query)})", f"{highlight_start}\\1{highlight_end}", text, flags=re.IGNORECASE)
    return highlighted_text

def full_text_search(query, db_file='articles.db'):
    """Perform a full-text search on the FTS table."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    normalized_query = query.strip().lower()
    
    try:
        cursor.execute("SELECT page_number, text FROM articles_fts WHERE text MATCH ? ORDER BY page_number ASC LIMIT 1, 5", (f'"{normalized_query}"',))
        results = cursor.fetchall()
        
        if results:
            logging.info("Search Results Found.")
            highlighted_results = []
            for page_number, text in results:
                start_index = text.lower().find(normalized_query)
                if start_index != -1:
                    sliced_text = text[start_index:]  # Get text from the search term to the end
                    highlighted_text = highlight_keywords(sliced_text, query)
                    highlighted_results.append((page_number, highlighted_text))
            return highlighted_results
        else:
            logging.info("No results found.")
            return []
    except Exception as e:
        logging.error(f"Error searching: {e}")
        return []
    finally:
        conn.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python search.py 'search query'")
        return

    search_query = sys.argv[1]  # Get the query from command line argument

    json_file_path = 'pdf_output.json'
    data = load_data_from_json(json_file_path)

    # Check if the database exists and create or update accordingly
    db_file = 'articles.db'
    if not database_exists(db_file):
        logging.info("Database does not exist. Creating a new database.")
        create_database(data)
    else:
        logging.info("Database exists. Updating with new data.")
        update_database(data)

    search_results = full_text_search(search_query)

    if search_results:
        print("Search Results:")
        for page_number, text in search_results:
            print(f"Page Number: {page_number}\nText: {text}...")  # Display text with highlights
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
