import json
import argparse
from pathlib import Path
from datetime import datetime
import logging

SUPPORTED_TEXT_EXTENSIONS = [".txt", ".pdf"]


LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "automation.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

print("RUNNING UPDATED VERSION")

from processors.text_extractor import extract_text_from_file

from pathlib import Path
from datetime import datetime


#Define directories

# Define directories

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"


#Create Directories if they dont exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Create directories if they don't exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def process_files(recursive=False) :

    results = []

    iterator = INPUT_DIR.rglob("*") if recursive else INPUT_DIR.iterdir()
    
    for file in iterator:

        try:
            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_TEXT_EXTENSIONS:
                logging.warning(f"Skipped unsupported file: {file.name}")
                continue

            text = extract_text_from_file(file)
            
            if not text.strip():
                logging.warning(f"No text found in file: {file.name}")          
            
            info = {
                "filename": file.name,
                "extension": file.suffix.lower(),
                "size_bytes": file.stat().st_size,
                "text_length": len(text),
                "processed_at": datetime.utcnow().isoformat()
            }
           
            results.append(info)
            logging.info(f"Processed file: {file.name}")

        except Exception as e:
            logging.error(f"Failed processing {file}: {e}")

    return results


def generate_report(results):
    report_path = OUTPUT_DIR / "report.txt"

    try:
        with report_path.open("w", encoding="utf-8") as f:
            for item in results:
                f.write(
                    f"File: {item['filename']} | "
                    f"Size: {item['size_bytes']} bytes | "
                    f"Text length: {item['text_length']} characters\n"
                )

        logging.info("Report generated successfully")

    except Exception as e:
        logging.error(f"Failed to generate report: {e}")

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
