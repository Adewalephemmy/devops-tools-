import os
import sys

def main():
    # 1. Get environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ Error: API_KEY environment variable not set")
        sys.exit(1)

    # 2. Get filename argument
    if len(sys.argv) < 2:
        print("❌ Error: Missing filename argument")
        print("Usage: python scripts/env_demo.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # 3. Print confirmation
    print(f"✅ Using API_KEY={api_key[:4]}*** and file={filename}")

if __name__ == "__main__":
    main()
