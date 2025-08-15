# Gemini AI OCR and Image Interpretation

This repository contains a Python script that demonstrates how to perform Optical Character Recognition (OCR) and image interpretation using the Google Gemini AI API. It allows you to extract text verbatim from images and also interpret information from diagrams, including specific details like costs.

## Table of Contents

- [What is this?](#what-is-this)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [File Structure](#file-structure)
- [Libraries Used](#libraries-used)
- [Understanding the Code](#understanding-the-code)
- [Examples](#examples)

## What is this?

This project provides a simple yet powerful way to interact with Google's Gemini AI model for image-based tasks. Specifically, it focuses on:

1. **Verbatim Text Extraction (OCR):** Extracting all visible text from an image as accurately as possible.
2. **Image Interpretation:** Analyzing diagrams or images to understand their content and extract specific information based on a given prompt.

This is particularly useful for automating data entry from scanned documents, analyzing charts, or extracting details from complex visual information.

## Features

- Extract text directly from images.
- Interpret information from diagrams and images based on custom prompts.
- Easy integration with Google Gemini AI.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.x:** You can download it from [python.org](https://www.python.org/downloads/).
- **Conda (Recommended):** For easy environment and package management. Download Miniconda or Anaconda from [conda.io](https://docs.conda.io/en/latest/miniconda.html).
- **Google Gemini AI API Key:** You will need an API key from Google AI Studio. Visit [Google AI Studio](https://aistudio.google.com/) to get your key.

## Installation

Follow these steps to set up the project:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ranak8811/Gemini-AI-OCR-and-Image-Interpretation.git
    cd Gemini-AI-OCR-and-Image-Interpretation
    ```

2.  **Create a Conda environment (recommended):**

    ```bash
    conda create -n gemini-ocr python=3.9
    conda activate gemini-ocr
    ```

3.  **Install the required library:**

    ```bash
    conda install -c conda-forge google-generativeai
    ```

    Alternatively, if you prefer `pip`:

    ```bash
    pip install google-generativeai
    ```

4.  **Set up your Google Gemini AI API Key:**
    The script uses an environment variable to store your API key. It's crucial for security not to hardcode your API key directly into the script.

    **For macOS/Linux:**
    Open your terminal and add the following line to your `~/.bashrc`, `~/.zshrc`, or `~/.profile` file:

    ```bash
    export GEMINI_AI_API_KEY='your_api_key_here'
    ```

    Replace `'your_api_key_here'` with your actual API key. After adding, save the file and run `source ~/.bashrc` (or your respective file) to apply the changes.

    **For Windows:**
    Open Command Prompt as Administrator and run:

    ```cmd
    setx GEMINI_AI_API_KEY "your_api_key_here"
    ```

    Replace `"your_api_key_here"` with your actual API key. You might need to restart your terminal or computer for the changes to take effect.

## How to Use

Once you have installed the prerequisites and set up your API key, you can run the main script:

1.  **Activate your Conda environment (if you created one):**

    ```bash
    conda activate gemini-ocr
    ```

2.  **Run the Python script:**
    ```bash
    python Gemini_OCR_SDK.py
    ```

The script will:

- Upload `jetpack.jpg` and extract text verbatim.
- Upload `jetpack2.jpg` and interpret information, including the cost of the item.
  The extracted or interpreted text will be printed to your console.

## File Structure

- `Gemini_OCR_SDK.py`: The main Python script that interacts with the Google Gemini AI API for OCR and image interpretation.
- `jetpack.jpg`: An example image used for verbatim text extraction.
- `jetpack2.jpg`: Another example image used for image interpretation (e.g., extracting cost from a diagram).
- `README.md`: This file, providing documentation for the project.
- `.gitignore`: Specifies intentionally untracked files that Git should ignore.
- `Biochemistry.pdf`: An example PDF file (not directly used by the Python script, but present in the repository).
- `Gemini_OCR_SDK.ipynb`: A Jupyter Notebook version of the `Gemini_OCR_SDK.py` script, useful for interactive development and testing.
- `mcq_dataset.csv`: An example CSV dataset (not directly used by the Python script, but present in the repository).
- `pdf_ocr_dataset_generator.py`: A Python script for generating PDF OCR datasets (not directly used by the main OCR functionality).

## Libraries Used

The core functionality of this project relies on the following Python library:

- `google-generativeai`: This is the official Google Generative AI SDK for Python, used to interact with the Gemini models.
- `os`: A standard Python library used for interacting with the operating system, specifically for accessing environment variables (like your API key).
- `base64`: A standard Python library used for encoding and decoding data in Base64 format (though `google-generativeai` handles image uploads directly, this library might be useful for other image processing tasks).

## Understanding the Code

Let's break down the `Gemini_OCR_SDK.py` script:

- **`import google.generativeai as genai`**: Imports the necessary library for interacting with Gemini.
- **`import os`**: Imports the OS module to access environment variables.
- **`os.environ['GEMINI_AI_API_KEY']`**: This line attempts to retrieve your API key from the environment variable `GEMINI_AI_API_KEY`.
- **`genai.configure(api_key=API_KEY)`**: Configures the `google-generativeai` library with your API key, allowing it to authenticate with the Gemini service.
- **`prep_image(image_path)` function**:
  - Takes an `image_path` as input.
  - Uses `genai.upload_file()` to upload the image to Google's services. This is a crucial step as Gemini models work with uploaded files rather than local file paths directly.
  - Prints confirmation of the upload and retrieves the file object.
  - Returns the `sample_file` object, which contains the URI needed for the model.
- **`extract_text_from_image(image_path, prompt)` function**:
  - Takes the `image_path` (which is actually the uploaded file object from `prep_image`) and a `prompt` string.
  - **`model = genai.GenerativeModel(model_name="gemini-1.5-pro")`**: Initializes the Gemini model. `gemini-1.5-pro` is a powerful model capable of handling multimodal inputs (like images and text).
  - **`response = model.generate_content([image_path, prompt])`**: This is where the magic happens. It sends both the uploaded image and your text prompt to the Gemini model. The model then processes both inputs to generate a relevant response.
  - Returns the `response.text`, which is the model's output.
- **Example Usage**: The script then demonstrates how to use these functions with `jetpack.jpg` for verbatim text extraction and `jetpack2.jpg` for interpreted information, including cost.

## Examples

The `Gemini_OCR_SDK.py` script includes two examples:

1.  **Verbatim Text Extraction:**

    ```python
    sample_file = prep_image('jetpack.jpg')
    text = extract_text_from_image(sample_file, "Extract the text in the image verbatim")
    if text:
        print("Extracted Text:")
        print(text)
    else:
        print("Failed to extract text from the image.")
    ```

    This will attempt to read all text from `jetpack.jpg` and print it.

2.  **Image Interpretation with Specific Information:**
    ```python
    sample_file = prep_image('jetpack2.jpg')
    text = extract_text_from_image(sample_file, "Analyze the given diagram and carefully extract the information. Include the cost of the item")
    if text:
        print("Interpreted Image:")
        print(text)
    else:
        print("Failed to extract text from the image.")
    ```
    This will analyze `jetpack2.jpg` (presumably a diagram with cost information) and extract relevant details based on the prompt.
