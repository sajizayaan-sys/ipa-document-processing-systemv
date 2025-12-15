from pathlib import Path
from datetime import datetime

 HEAD
#Define directories
=======
# Define directories
 1a4834df67452a77a9a167e9f87cac4c2bab25f4
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

 HEAD
#Create Directories if they dont exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Create directories if they don't exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

 1a4834df67452a77a9a167e9f87cac4c2bab25f4
def process_files():
    results = []

    for file in INPUT_DIR.iterdir():
        if file.is_file():
            info = {
                "filename": file.name,
                "size_bytes": file.stat().st_size,
                "processed_at": datetime.utcnow().isoformat()
            }
            results.append(info)
 HEAD
        return results


    return results

 1a4834df67452a77a9a167e9f87cac4c2bab25f4
def generate_report(results):
    report_path = OUTPUT_DIR / "report.txt"
    with report_path.open("w", encoding="utf-8") as f:
        for item in results:
            f.write(
                f"File: {item['filename']} | "
                f"Size: {item['size_bytes']} bytes | "
                f"Processed: {item['processed_at']}\n"
            )
    return report_path
if __name__ == "__main__":
    data = process_files()
    report = generate_report(data)
    print(f"Processed {len(data)} files.")
    print(f"Report saved to: {report}")
