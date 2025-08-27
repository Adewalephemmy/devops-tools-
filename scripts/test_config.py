import yaml
import os

CONFIG_FILE = os.path.join("config", "test_config.yaml")

if not os.path.exists(CONFIG_FILE):
    print("❌ Config file missing:", CONFIG_FILE)
else:
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    print("✅ Config loaded successfully:", config)
