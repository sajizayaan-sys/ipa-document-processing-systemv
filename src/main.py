from pathlib import Path
from datetime import datetime
import logging

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

 
def process_files():
    results = []

    for file in INPUT_DIR.iterdir():
        try:
            if not file.is_file():
                continue

            text = extract_text_from_file(file)

            info = {
                "filename": file.name,
                "size_bytes": file.stat().st_size,
                "text_length": len(text),
                "processed_at": datetime.utcnow().isoformat()
            }

            results.append(info)

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

if __name__ == "__main__":
    logging.info("Automation started")

    data = process_files()
    report = generate_report(data)

    logging.info(f"Processed {len(data)} files")
    logging.info(f"Report saved to: {report}")

    print(f"Processed {len(data)} files.")
    print(f"Report saved to: {report}")

