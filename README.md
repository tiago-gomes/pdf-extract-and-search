PDF Text Extraction and Search Tool
===================================

This project provides a streamlined way to parse PDF files, convert the text into structured JSON items per page, and perform efficient text searches within the extracted data.

Features
--------

-   **PDF Parsing**: Extracts text content from PDF files and converts it into a structured JSON format.
-   **Search Functionality**: Allows for full-text searches in the extracted data, with highlighted search terms and contextual display.

Requirements
------------

Ensure that Python is installed and the following packages are available:

-   `PyPDF2`
-   `sqlite3`
-   `re`
-   `json`
-   `logging`
-   `sys`

Usage
-----

### Step 1: Parse a PDF and Extract Data

To extract text content from a PDF and save it as a JSON file:

bash

Copy code

`py extract_to_json.py`

This will parse the PDF and create a JSON file containing the text content organized by page.

### Step 2: Search the Extracted Data

To search for specific terms in the JSON data and view highlighted results:

bash

Copy code

`py search.py "your search query"`

Replace `"your search query"` with the desired text to search.

How It Works
------------

1.  **PDF Parsing**: The script reads the PDF file and extracts text content page by page, saving it as a JSON file.
2.  **Database Creation**: The extracted data is loaded into an SQLite database with an FTS (Full-Text Search) table for optimized searching.
3.  **Search Tool**: The `search.py` script performs a full-text search in the database, highlights the search term in the results, and displays text excerpts from relevant pages.

Customization
-------------

-   Modify the file paths for input/output as needed.
-   Adjust the number of search results or the formatting in the `search.py` script.

Example
-------

Run the extraction and search using the following commands:

bash

Copy code

`# Extract text from PDF
py extract_to_json.py

# Search the extracted content
py search.py "artigo 1.º"`

Notes
-----

-   Ensure that your input PDF is properly formatted and encoded for text extraction.
-   The scripts handle UTF-8 encoding to manage special characters in the text.

Troubleshooting
---------------

If you encounter any errors during parsing or searching, check that:

-   The PDF file is not password-protected or corrupted.
-   Required packages are installed and up to date.
-   The database file is accessible and not locked by another process.

License
-------

This project is open-source and free to use under the MIT License.
