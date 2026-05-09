import fitz
from docx import Document


# PDF PARSER
def extract_text_from_pdf(file_path):

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    return text



# DOCX PARSER
def extract_text_from_docx(file_path):

    doc = Document(file_path)

    text = "\n".join(
        [para.text for para in doc.paragraphs]
    )

    return text



# MAIN PARSER
def parse_resume(file_path):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        return "Unsupported File Format"