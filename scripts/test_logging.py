import logging
import os

LOG_FILE = os.path.join("logs", "test.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("🚀 Logging system is working!")

print("✅ Check logs/test.log for output")
