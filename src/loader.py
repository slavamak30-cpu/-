from pypdf import PdfReader
import docx 

def load_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n" # Добавляем два переноса, чтобы разделять абзацы
    return text

def load_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_document(file_path):
    if file_path.endswith('.pdf'):
        return load_pdf(file_path)
    elif file_path.endswith('.docx'):
        return load_docx(file_path)
    elif file_path.endswith('.txt'):
        return load_txt(file_path)
    else:
        raise ValueError("Неподдерживаемый формат")
