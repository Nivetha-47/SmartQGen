import PyPDF2
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

        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from each page
            text = ""
            for page in reader.pages:
                text += page.extract_text()

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
