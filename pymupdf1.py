import fitz  # PyMuPDF
import time
import os

def pdf_to_text():
    # Ask the user for the PDF file path
    pdf_path = input("Enter the path of the PDF file: ")

    try:
        start_time = time.time()  # Start the timer

        # Validate if the PDF file exists
        if not os.path.exists(pdf_path):
            print("The specified PDF file does not exist.")
            return

        # Determine the directory and name for the output file
        output_dir = os.path.dirname(pdf_path)
        output_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
        txt_output_path = os.path.join(output_dir, output_name)

        # Open the PDF file using PyMuPDF
        doc = fitz.open(pdf_path)

        # Extract text from each page
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        # Save the extracted text to a TXT file
        with open(txt_output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        end_time = time.time()  # End the timer
        runtime = end_time - start_time  # Calculate runtime

        print(f"Text extracted and saved to: {txt_output_path}")
        print(f"Runtime: {runtime:.2f} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
pdf_to_text()