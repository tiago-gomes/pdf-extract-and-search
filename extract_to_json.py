import pdfplumber  # Use pdfplumber for better text extraction
import json

def extract_text_from_pdf(input_path):
    """Extracts text from a PDF file using pdfplumber."""
    text_content = []
    try:
        with pdfplumber.open(input_path) as pdf:
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                text = page.extract_text() or ""  # Extract text or use an empty string
                if text:  # Only append if text is not None or empty
                    text_content.append(text)  # Collect all text in a list
    except Exception as e:
        print(f"An error occurred during text extraction: {e}")
    return text_content  # Return the list of text per page

def save_text_to_json(text_content, output_file):
    """Saves the extracted text content to a JSON file."""
    try:
        # Create a dictionary to structure the data
        json_data = {
            "pages": [
                {"page_number": i + 1, "text": page_text} for i, page_text in enumerate(text_content)
            ]
        }
        # Save the structured data as JSON
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"Created {output_file} with the extracted text in JSON format.")
    except Exception as e:
        print(f"An error occurred during JSON file creation: {e}")

def extract_pdf_text_to_json(input_path, output_file):
    """Extracts all text from a PDF and saves it to a JSON file."""
    text_content = extract_text_from_pdf(input_path)
    save_text_to_json(text_content, output_file)

# Example usage
input_pdf_path = 'ccp_limiares_2024_2025_portarias-318.pdf'  # Replace with your PDF path
output_json_path = 'pdf_output.json'  # Specify your output JSON file path
extract_pdf_text_to_json(input_pdf_path, output_json_path)
