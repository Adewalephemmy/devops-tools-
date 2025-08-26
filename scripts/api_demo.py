import os
import sys
import requests

def main():
    # 1. Get API Key from environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ Error: API_KEY not set. Please export/set it first.")
        sys.exit(1)

    # 2. Public test API (JSONPlaceholder)
    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raise error for bad response
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        sys.exit(1)

    # 3. Show result
    data = response.json()
    print("✅ API Response:")
    print(f"Title: {data['title']}")
    print(f"Body: {data['body']}")

if __name__ == "__main__":
    main()
