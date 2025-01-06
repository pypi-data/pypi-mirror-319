import pdftotext
import base64
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image
import time
def read_pdf(pdf_path, pdf_image_start=0, pdf_image_end=1):
    """
    Read a PDF file and extract both text and images using poppler-based tools.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Dictionary containing:
            - 'text': Extracted text from all pages
            - 'images': List of base64 encoded images from all pages
    """
    text = ""
    images = []
    
    # Extract text using pdftotext (poppler)
    try:
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
            # Join pages with headers and newlines
            pages = []
            for i, page in enumerate(pdf, 1):
                pages.append(f"=== PAGE {i} ===\n{page}")
            text = "\n".join(pages)
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        text = ""

    # Convert pages to images using pdf2image (poppler)
    try:
        # Convert each page to an image
        pages = convert_from_path(pdf_path)
        
        # Convert slice indices to integers
        start = int(pdf_image_start)
        end = int(pdf_image_end)
        
        print(f"Total pages: {len(pages)}")
        print(f"Getting pages {start} to {end}")
        print(f"Slice will return {len(pages[start:end])} pages")
        
        # Process each page using integer indices
        for page in pages[start:end]:
            try:
                # Scale down image if needed
                width, height = page.size
                if width > 1000 or height > 1000:
                    # Calculate scaling factor
                    scale = min(1000/width, 1000/height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    page = page.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert PIL Image to base64
                img_buffer = BytesIO()
                page.save(img_buffer, format='PNG')
                img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                images.append("<lt_base64>" + img_str + "</lt_base64>")
            except Exception as e:
                print(f"Error processing page to image: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
    
    return {
        "text": text.strip(),
        "images": images
    }
