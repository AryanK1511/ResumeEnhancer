import os
import logging
import re
from docx import Document
from colorama import Fore, Style
from PyPDF2 import PdfReader

# Custom formatter for colorized logging
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
    }

    def format(self, record):
        color=self.COLORS.get(record.levelname, Fore.WHITE)
        message=super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

def write_to_file(file_path, content):
    extension = os.path.splitext(file_path)[1].lower()

    if extension=='.txt':
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    elif extension=="":
        with open(file_path+'.txt', 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        raise ValueError(f"Unsupported outfile type: {extension}, only .txt files are supported")


def read_txt_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as f:
        content=f.read()
    return content

def read_pdf_file(file_path):
    content=""
    with open(file_path, "rb") as f:
        reader=PdfReader(f)
        for page in range(len(reader.pages)):
            content+=reader.pages[page].extract_text()
    return content

def read_word_file(file_path):
    doc=Document(file_path)
    content="\n".join([para.text for para in doc.paragraphs])
    return content

def read_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension=='.txt':
        return read_txt_file(file_path)
    elif extension=='.pdf':
        return read_pdf_file(file_path)
    elif extension in ['.doc', '.docx']:
        return read_word_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

# set up logger
def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) 

    formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
