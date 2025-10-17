from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import gdown
#import torch
import re


file_id = "14ip6gCW1pqXR5jQQ3jy5Si1yWo5GY7A8"
url = f"https://drive.google.com/file/d/{file_id}/view?usp=drive_link"

# Output file path
output_path = "local_file.pdf"

# Download the file
gdown.download(url, output_path, quiet=False)

print(f"File downloaded to: {output_path}")

# Read the PDF
#reader = PdfReader(url)
#for page in reader.pages:
 #   print(page.extract_text())

