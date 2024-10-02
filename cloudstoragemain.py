import os
import fitz  # PyMuPDF
import pdfplumber
import spacy
from google.cloud import storage
from sqlalchemy import create_engine, text
from google.cloud import secretmanager

# Load environment variables
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
alloydb_instance = os.getenv('ALLOYDB_INSTANCE_CONNECTION_NAME')

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Initialize Spacy NLP model
nlp = spacy.load('en_core_web_sm')

# Initialize SQLAlchemy engine for AlloyDB
engine = create_engine(f'postgresql+pg8000://{alloydb_instance}')

def process_pdf(event, context):
    bucket_name = event['bucket']
    file_name = event['name']

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    pdf_content = blob.download_as_bytes()

    # Extract text from PDF using PyMuPDF
    pdf_text = ""
    with fitz.open(stream=pdf_content, filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()

    # Use pdfplumber as a backup
    if not pdf_text.strip():
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                pdf_text += page.extract_text()

    # NLP processing
    doc = nlp(pdf_text)
    title, date, author, findings, recommendations = extract_information(doc)

    # Store data in AlloyDB
    with engine.connect() as connection:
        connection.execute(text("""
            INSERT INTO audit_reports (title, date, author, findings, recommendations)
            VALUES (:title, :date, :author, :findings, :recommendations)
        """), {"title": title, "date": date, "author": author, "findings": findings, "recommendations": recommendations})

def extract_information(doc):
    title = ""
    date = ""
    author = ""
    findings = ""
    recommendations = ""

    for ent in doc.ents:
        if ent.label_ == "TITLE":
            title = ent.text
        elif ent.label_ == "DATE":
            date = ent.text
        elif ent.label_ == "AUTHOR":
            author = ent.text
        elif ent.label_ == "FINDINGS":
            findings = ent.text
        elif ent.label_ == "RECOMMENDATIONS":
            recommendations = ent.text

    return title, date, author, findings, recommendations
