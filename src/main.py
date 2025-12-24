from processors.pdf_extractor import extract_text_from_pdf
import json
import argparse
from pathlib import Path
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


load_dotenv()  # loads .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SUPPORTED_TEXT_EXTENSIONS = [".txt", ".pdf"]

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "automation.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

print("RUNNING UPDATED VERSION")



from pathlib import Path
from datetime import datetime

<<<<<<< HEAD
# Define directories
=======
 
#Define directories

# Define directories
 
>>>>>>> 072278f8a637b5ec0a37749d9bd178f8b608f6b4
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

<<<<<<< HEAD
=======
 
>>>>>>> 072278f8a637b5ec0a37749d9bd178f8b608f6b4
#Create Directories if they dont exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

TEXT_OUTPUT_DIR = OUTPUT_DIR / "extracted_text"
TEXT_OUTPUT_DIR.mkdir(exist_ok=True)


def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

<<<<<<< HEAD
def analyze_document(text: str) -> dict:
    if not text or len(text.strip()) < 50:
        logging.warning("Text too short for AI analysis")
        return {}

    prompt = f"""
You are a document analysis system.

Return ONLY valid JSON in this exact structure:

{{
  "document_type": "invoice | contract | form | report | other",
  "summary": "one short paragraph summary"
}}

Text:
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You only return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        logging.error(f"LLM analysis failed: {e}")
        return {}
=======
from processors.text_extractor import extract_text_from_file
>>>>>>> 072278f8a637b5ec0a37749d9bd178f8b608f6b4

def process_files(recursive=False) :
    results = []

    iterator = INPUT_DIR.rglob("*") if recursive else INPUT_DIR.iterdir()
    
    for file in iterator:
        try:
            if not file.is_file():
                continue

            # Choose extraction method
            if file.suffix.lower() == ".pdf":
                text = extract_text_from_pdf(file)
            else:
                text = extract_text_from_file(file)

            # Skip empty text
            if not text or not text.strip():
                logging.warning(f"No text found in file: {file.name}")
                continue

            # 3️⃣ AI ANALYSIS (THIS IS THE LINE YOU ASKED ABOUT)
            analysis = analyze_document(text)

            # Metadata
            info = {
                "filename": file.name,
                "extension": file.suffix.lower(),
                "size_bytes": file.stat().st_size,
<<<<<<< HEAD
                "text_length": len(text),
                "processed_at": datetime.utcnow().isoformat(),
                "document_type": analysis.get("document_type"),
                "summary": analysis.get("summary")
}

=======
                "processed_at": datetime.utcnow().isoformat()
            }
           
>>>>>>> 072278f8a637b5ec0a37749d9bd178f8b608f6b4
            results.append(info)

            # Save extracted text
            text_output_path = TEXT_OUTPUT_DIR / f"{file.stem}.txt"
            text_output_path.write_text(text, encoding="utf-8")

            logging.info(f"Processed file: {file.name}")

        except Exception as e:
            logging.error(f"Failed processing {file}: {e}")

    return results

<<<<<<< HEAD
=======
 
>>>>>>> 072278f8a637b5ec0a37749d9bd178f8b608f6b4
def generate_report(results):
    report_path = OUTPUT_DIR / "document_analysis_report.pdf"

    try:
<<<<<<< HEAD
        c = canvas.Canvas(str(report_path), pagesize=A4)
        width, height = A4
=======
        with report_path.open("w", encoding="utf-8") as f:
            for item in results:
                f.write(
                    f"File: {item['filename']} | "
                    f"Size: {item['size_bytes']} bytes | "
                    f"Processed: {item['processed_at']}\n"
                )
>>>>>>> 072278f8a637b5ec0a37749d9bd178f8b608f6b4

        y = height - 2 * cm

        # Report title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(2 * cm, y, "Document Processing & AI Analysis Report")

        y -= 1.5 * cm
        c.setFont("Helvetica", 11)
        c.drawString(2 * cm, y, f"Generated on: {datetime.utcnow().isoformat()}")

        y -= 2 * cm

        for idx, item in enumerate(results, start=1):
            if y < 4 * cm:
                c.showPage()
                y = height - 2 * cm

            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y, f"{idx}. File: {item['filename']}")
            y -= 0.8 * cm

            c.setFont("Helvetica", 11)
            c.drawString(2 * cm, y, f"Type: {item.get('document_type', 'unknown')}")
            y -= 0.8 * cm

            summary = item.get("summary", "No summary available")
            text_obj = c.beginText(2 * cm, y)
            text_obj.setFont("Helvetica", 11)

            for line in summary.splitlines():
                text_obj.textLine(line)

            c.drawText(text_obj)
            y = text_obj.getY() - 1.2 * cm

        c.save()
        logging.info("PDF report generated successfully")

    except Exception as e:
        logging.error(f"Failed to generate PDF report: {e}")

    return report_path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Document Processing Automation"
    )

    parser.add_argument(
        "--input",
        type=str,
        default="src/input",
        help="Input folder path"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="src/output",
        help="Output folder path"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan subdirectories"
    )

    return parser.parse_args()

if __name__ == "__main__":
   
    args = parse_args()

    INPUT_DIR = Path(args.input).resolve()
    OUTPUT_DIR = Path(args.output).resolve()

    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    logging.info("Automation started")
    logging.info(f"Input directory: {INPUT_DIR}")
    logging.info(f"Output directory: {OUTPUT_DIR}")
    logging.info(f"Recursive scan: {args.recursive}")

    if not any(INPUT_DIR.iterdir()):
        logging.warning("Input directory is empty")

    data = process_files(recursive=args.recursive)
    report = generate_report(data)

    logging.info(f"Processed {len(data)} files")
    logging.info(f"Report saved to: {report}")

    print(f"Processed {len(data)} files.")
    print(f"Report saved to: {report}")
