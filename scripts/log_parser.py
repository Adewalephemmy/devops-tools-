import logging
import os
import yaml
import json
import csv
from collections import Counter

# Setup logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ensure logs and reports directories exist
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)

# Configure logging to project logs folder
log_file = os.path.join(BASE_DIR, "logs", "log_parser.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    cfg_path = os.path.join(BASE_DIR, "config", "settings.yaml")
    if not os.path.exists(cfg_path):
        logging.error(f"Config file {cfg_path} not found.")
        raise FileNotFoundError(f"Config file {cfg_path} not found.")
    with open(cfg_path) as f:
        return yaml.safe_load(f)

def parse_log(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Log file {file_path} not found.")
        return None

    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    counts = Counter()

    with open(file_path) as f:
        for line in f:
            for lvl in levels:
                if lvl in line:
                    counts[lvl] += 1

    logging.info(f"Parsed log file {file_path}: {dict(counts)}")
    return counts

def export_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    logging.info(f"Results exported to {output_path}")

def export_csv(data, output_path):
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Level", "Count"])
        for key, value in data.items():
            writer.writerow([key, value])
    logging.info(f"Results exported to {output_path}")

if __name__ == "__main__":
    cfg = load_config()
    log_file = cfg["log_file"]

    counts = parse_log(log_file)
    if counts:
        export_json(counts, cfg["output_json"])
        export_csv(counts, cfg["output_csv"])
        print("✅ Log parsing complete. Results saved.")
