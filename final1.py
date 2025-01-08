from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import logging
import time
import fitz  # PyMuPDF

# Start measuring execution time
start_time = time.time()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pdf_to_text(pdf_path):
    """Convert PDF to text using PyMuPDF."""
    try:
        logger.info("Converting PDF to text...")
        text = ""
        # Open the PDF file
        with fitz.open(pdf_path) as pdf_document:
            # Iterate through each page
            for page_num in range(pdf_document.page_count):
                # Get the page
                page = pdf_document[page_num]
                # Extract text from the page
                text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error converting PDF to text: {e}")
        raise

# Main function to process PDF and generate MCQs
def generate_mcqs_from_pdf(input_pdf, output_file):
    try:
        # Step 1: Convert PDF to text
        text = pdf_to_text(input_pdf)
        
        # Step 2: Initialize the Llama model via Ollama
        logger.info("Initializing Llama model...")
        llama_llm = ChatOllama(model="llama3.2")

        # Step 3: Create the prompt template
        template = """
     SYSTEM INSTRUCTION:
You are an MCQ generator that MUST process ALL chapters in sequence. You cannot stop until all chapters are complete. After each chapter, you must explicitly continue to the next one.

FORMAT RULES:
1. Process chapters one by one
2. Generate exactly 5 MCQs per chapter
3. Do not stop until all chapters are done
4. Signal the start and end of each chapter clearly

CHAPTER PROCESSING REQUIREMENTS:
- Before starting: List the total number of chapters you detect in the text
- After each chapter: Confirm "Moving to next chapter..."
- After every 3 chapters: State "Continuing processing..."
- At the very end: State "All chapters completed"

GENERATE MCQs IN THIS EXACT FORMAT:

===== CHAPTER [NUMBER]: [TITLE] =====

Q1: [Question]
a) [Option]
b) [Option]
c) [Option]
d) [Option]
Correct: [Letter]

[Repeat for Q2-Q5]

END CHAPTER [NUMBER]
CONTINUING TO NEXT CHAPTER...

===== CHAPTER [NUMBER+1]: [TITLE] =====
[Continue pattern]

CRITICAL RULES:
- You MUST complete all chapters
- You MUST generate exactly 5 questions per chapter
- You MUST NOT stop until all chapters are done
- You MUST confirm progress after each chapter
- You MUST maintain consistent formatting throughout

Begin NOW by:
1. Stating total chapters detected
2. Processing Chapter 1
3. Moving systematically through ALL chapters
4. Confirming completion
```
        {text}

        Generate  set of MCQs for each and every unit/chapter as i said. i need 5 mcq's for chapter1, 5 mcqs for chapter 2 , and so on. i need the complete output of all the units in single output. 
        """
        prompt = PromptTemplate(input_variables=["text"], template=template)
        mcq_chain = LLMChain(llm=llama_llm, prompt=prompt)

        # Step 4: Generate MCQs for the entire text
        logger.info("Generating MCQs...")
        result = mcq_chain.run({"text": text})

        # Step 5: Save the output to a file
        logger.info(f"Saving MCQs to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(result)

        logger.info(f"MCQs saved successfully to {output_file}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        # Record the end time and calculate the elapsed time
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution time: {execution_time:.2f} seconds")

# Example usage
if __name__ == "__main__":
    input_pdf = r"C:\Users\Yogendthira VK\Downloads\TEST PDF's\Software-Engineering-9th-Edition-by-Ian-Sommerville.pdf"
    output_file = "mcq_output4.txt"
    generate_mcqs_from_pdf(input_pdf, output_file)