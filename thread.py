import threading
from PyPDF2 import PdfReader
import os
import time

# Function to extract text from a single page
def extract_text_from_page(pdf_path, page_number, results, thread_name):
    try:
        print(f"{thread_name}: Extracting text from page {page_number + 1}...")
        reader = PdfReader(pdf_path)
        page = reader.pages[page_number]
        text = page.extract_text()
        results[page_number] = text  # Store result in shared dictionary
        print(f"{thread_name}: Finished page {page_number + 1}")
    except Exception as e:
        print(f"{thread_name}: Error occurred - {e}")

# Function to handle the uploaded PDF
def process_pdf(pdf_path):
    try:
        # Read the PDF and determine the number of pages
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"Total pages in PDF: {total_pages}")

        # Dictionary to store extracted text from each page
        results = {}

        # Create and start threads for each page
        threads = []
        for i in range(total_pages):
            thread = threading.Thread(
                target=extract_text_from_page, args=(pdf_path, i, results, f"Thread-{i+1}")
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Combine results
        full_text = "".join(results[i] for i in sorted(results.keys()))
        print("Text extraction complete.")
        return full_text

    except Exception as e:
        print(f"Error processing PDF: {e}")

# Main program
if __name__ == "__main__":
    # Replace this with the path to your PDF file
    pdf_path = r"C:\Users\Yogendthira VK\Downloads\AI_Russell_Norvig.pdf  "

    # Check if file exists
    if os.path.exists(pdf_path):
        start_time = time.time()  # Start the timer

        extracted_text = process_pdf(pdf_path)

        end_time = time.time()  # End the timer
        execution_time = end_time - start_time  # Calculate execution time

        # Save or print the extracted text
        output_path = "extracted_text.txt"
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        print(f"Extracted text saved to {output_path}")
        print(f"Execution Time: {execution_time:.2f} seconds")
    else:
        print("PDF file not found. Please provide a valid path.")
import threading
from PyPDF2 import PdfReader
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Function to extract text from a single page
def extract_text_from_page(pdf_path, page_number):
    try:
        reader = PdfReader(pdf_path)
        page = reader.pages[page_number]
        return page.extract_text()
    except Exception as e:
        print(f"Error occurred - {e}")
        return ""

# Function to handle the uploaded PDF
def process_pdf(pdf_path):
    try:
        # Read the PDF and determine the number of pages
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"Total pages in PDF: {total_pages}")

        # Create and start threads for each page
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda page_number: extract_text_from_page(pdf_path, page_number), range(total_pages)))

        # Combine results
        full_text = "".join(results)
        print("Text extraction complete.")
        return full_text

    except Exception as e:
        print(f"Error processing PDF: {e}")

# Main program
if __name__ == "__main__":
    # Replace this with the path to your PDF file
    pdf_path = r"entr file"

    # Check if file exists
    if os.path.exists(pdf_path):
        start_time = time.time()  # Start the timer

        extracted_text = process_pdf(pdf_path)

        end_time = time.time()  # End the timer
        execution_time = end_time - start_time  # Calculate execution time

        # Save or print the extracted text
        output_path = "extracted_text.txt"
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        print(f"Extracted text saved to {output_path}")
        print(f"Execution Time: {execution_time:.2f} seconds")
    else:
        print("PDF file not found. Please provide a valid path.")