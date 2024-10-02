# CyberAuditGen

CyberAuditGen is a cutting-edge solution designed to streamline the analysis of unstructured cybersecurity audit reports. By leveraging Generative AI, CyberAuditGen automatically processes PDF files, extracts key information using NLP techniques, and stores the structured data in AlloyDB for easy querying and analysis.

## Technologies Used
- Google Cloud Storage
- AlloyDB
- PyMuPDF
- pdfplumber
- Natural Language Processing (NLP)
- Named Entity Recognition (NER)
- Vector embeddings
- Google Cloud Functions
- Google Cloud IAM
- Python
- SQL

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/CyberAuditGen.git
    ```
2. Navigate to the project directory:
    ```bash
    cd CyberAuditGen
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables (see `.env.example`).

## Usage
1. Upload a PDF to Google Cloud Storage.
2. The Cloud Function will automatically process the PDF, extract data, and store it in AlloyDB.
3. Use the chat interface to interact with the stored data.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
