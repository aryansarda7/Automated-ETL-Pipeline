import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

USER_API_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raises an error if the HTTP response was not OK
        data = response.json()
        logging.info(f"Successfully fetched {len(data)} records from {url}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {url}: e")
        return []
    
def main():
    user_data = fetch_data(USER_API_URL)
    posts_data = fetch_data(POSTS_API_URL)

    with open("user.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=4)
    
    with open("posts.json", "w", encoding= "utf-8") as f:
        json.dump(posts_data, f, indent=4)
if __name__ == "__main__":
    main()