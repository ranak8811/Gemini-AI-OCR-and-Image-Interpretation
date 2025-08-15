import google.generativeai as genai
import os
import pandas as pd
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace 'your_api_key' with your actual Google API key
API_KEY = os.getenv('GEMINI_AI_API_KEY')
if not API_KEY:
    raise ValueError("GEMINI_AI_API_KEY not found in environment variables or .env file.")
genai.configure(api_key=API_KEY)

def upload_file_to_gemini(file_path):
    """Uploads a file to Gemini and returns the File object."""
    try:
        sample_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path))
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
        file = genai.get_file(name=sample_file.name)
        print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
        return sample_file
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def extract_text_from_document(gemini_file_object, prompt):
    """Extracts text from a document using the Gemini model."""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    try:
        response = model.generate_content([gemini_file_object, prompt])
        return response.text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def parse_mcq_text(text):
    """Parses the extracted text to create the MCQ dataset."""
    dataset = []
    # Split the text into potential question blocks.
    # This regex looks for 'Q.' followed by text, then options a-e with (T) or (F)
    question_blocks = re.findall(r'Q\.\s*(.*?)(?=\s*Q\.|\Z)', text, re.DOTALL)

    for block in question_blocks:
        # Find the start of the options (e.g., 'a.', 'b.', etc.)
        option_start_match = re.search(r'\n\s*[a-e]\.', block)
        
        question_raw = ""
        options_text = ""

        if option_start_match:
            # Everything before the first option is the question
            question_raw = block[:option_start_match.start()].strip()
            options_text = block[option_start_match.start():].strip()
        else:
            # If no options found, the whole block might be a question or malformed
            question_raw = block.strip()
            options_text = "" # No options to parse

        # Remove the "()" part from the question, being robust to malformed parentheses.
        # This regex looks for "(" and then matches any characters non-greedily until
        # a closing parenthesis or the end of the string/line, making the closing parenthesis optional.
        question = re.sub(r'\s*\([^)]*\)?', '', question_raw).strip()
        # Remove any trailing hyphens or colons from the question
        question = re.sub(r'[-:]\s*$', '', question).strip()
        
        # Extract options and their T/F status from the options_text
        # Use re.DOTALL to allow '.*?' to match across newlines for multi-line options.
        options = re.findall(r'([a-e])\.\s*(.*?)\s*\((T|F)\)', options_text, re.DOTALL)

        for option_char, option_text, answer_char in options:
            # Clean up option_text: remove leading/trailing whitespace and replace internal newlines with a space
            option_text_cleaned = option_text.strip().replace('\n', ' ')
            full_question_option = f"{question}: {option_text_cleaned}"
            answer = "TRUE" if answer_char == "T" else "FALSE"
            dataset.append({"Question_Option": full_question_option, "Answer": answer})
    return dataset

def main():
    pdf_path = 'Biochemistry.pdf'
    
    # Upload the PDF file to Gemini
    gemini_file = upload_file_to_gemini(pdf_path)
    if not gemini_file:
        print("Failed to upload PDF. Exiting.")
        return

    # Extract text from the PDF
    # The prompt is crucial here. We need to instruct Gemini to preserve the structure,
    # especially the T/F indicators and the two-column layout.
    prompt = """
    Extract all questions and their options from this PDF. 
    Each question starts with 'Q.' and has options labeled a, b, c, d, e. 
    Each option is followed by (T) for True or (F) for False.
    Preserve the exact text of the question and each option.
    If there are two columns of questions on a page, extract them in order from left to right, top to bottom.
    Return the extracted text verbatim, maintaining line breaks and the original formatting as much as possible.
    """
    extracted_text = extract_text_from_document(gemini_file, prompt)

    if extracted_text:
        print("\n--- Extracted Text ---")
        print(extracted_text)
        print("----------------------\n")

        # Parse the extracted text and create the dataset
        dataset = parse_mcq_text(extracted_text)
        
        if dataset:
            df = pd.DataFrame(dataset)
            output_csv_path = 'mcq_dataset.csv'
            df.to_csv(output_csv_path, index=False)
            print(f"Dataset successfully created and saved to {output_csv_path}")
        else:
            print("No data extracted or parsed from the PDF.")
    else:
        print("Failed to extract text from the PDF.")

if __name__ == "__main__":
    main()
