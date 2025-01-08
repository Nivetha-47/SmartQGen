from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import logging
import time

# Start measuring execution time
start_time = time.time()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main function to process text and generate MCQs
def generate_mcqs_from_file(input_file, output_file):
    try:
        # Step 1: Read text from file
        logger.info("Reading text from input file...")
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()

        # Step 2: Initialize the Llama model via Ollama
        logger.info("Initializing Llama model...")
        llama_llm = ChatOllama(model="llama3.2")

        # Step 3: Create the prompt template
        template = """
        You are a highly skilled college professor and examination expert specializing in creating multiple-choice questions (MCQs) for college-level examinations. 
        
        Your task is to generate logically challenging and examination-focused MCQs for the provided unit. Follow these guidelines:
        1. Identify key topics in the unit and prioritize important topics.
        2. Generate  15 MCQs for each topic, ensuring questions test understanding, application, and analysis skills.
        3. Provide each MCQ with:
           - A question
           - Four answer options (a, b, c, d)
           - Clearly marked correct answer

        Here is the content of the unit:
        {text}

        Generate a comprehensive set of MCQs for this unit.
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
    input_file = r"C:\Users\Yogendthira VK\Downloads\artificial_intelligence book.txt"
    output_file = "mcq_output1.txt"
    generate_mcqs_from_file(input_file, output_file)
