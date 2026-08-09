import os
import io
import logging
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pdfplumber

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class OCRError(Exception):
    """Custom exception for OCR failures."""
    pass

# ----------------- Internal OCR function -----------------
def _perform_pdf_ocr(pdf_path, lang="eng", dpi=300):
    all_text = []
    doc = None
    basename = os.path.basename(pdf_path)

    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            logger.warning(f"PDF '{basename}' has no pages.")
            return ""

        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi, alpha=False)
            try:
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            except Exception:
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))

            page_text = pytesseract.image_to_string(img, lang=lang)
            if page_text.strip():
                all_text.append(f"\n--- Page {i + 1}/{len(doc)} ---\n{page_text.strip()}")
            else:
                logger.warning(f"No text detected on page {i + 1} of '{basename}'.")

        final_text = "\n".join(all_text).strip()
        if not final_text:
            logger.warning(f"No text extracted from PDF '{basename}'.")
        return final_text

    except FileNotFoundError:
        raise OCRError(f"PDF file not found: '{pdf_path}'")
    except pytesseract.TesseractNotFoundError:
        raise OCRError(
            "Tesseract executable not found. Ensure it is installed and added to PATH."
        )
    except Exception as e:
        raise OCRError(f"Unexpected OCR error for '{basename}': {e}")
    finally:
        if doc:
            doc.close()


# ----------------- Public function -----------------
def extract_text_from_file(file_path, lang="eng", dpi=300):
    """
    Extract text from PDF files.
    Automatically detects text-based PDFs and scanned PDFs.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()
    logger.info(f"Extracting text from '{os.path.basename(file_path)}'")

    if file_ext != ".pdf":
        raise OCRError(f"Unsupported file type '{file_ext}'. Only PDF files are supported.")

    # --- Try text-based extraction first ---
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            logger.info("Text-based PDF detected. Extraction successful.")
            return text.strip()
        else:
            logger.info("PDF appears to be scanned. Falling back to OCR...")
    except Exception as e:
        logger.warning(f"Text extraction failed: {e}. Falling back to OCR...")

    # --- Fallback to OCR ---
    return _perform_pdf_ocr(file_path, lang=lang, dpi=dpi)
