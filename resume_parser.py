import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    text = ""
    try:
        pdf_document = fitz.open(pdf_path)  # Open the PDF using fitz.open()
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()  # It's good practice to close the document
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

# Test it
if __name__ == "__main__":
    path = "D:/programming/pythonvenv/smart_career_recommender/resumes/Manojit_Karar.pdf" # Update with your actual path
    extracted = extract_text_from_pdf(path)
    print(f"\n--- Extracted Resume Text ---\n")
    print(extracted[:1000]) # Print first 1000 characters