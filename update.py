import requests
import sys

if __name__ == "__main__":
    token = sys.argv[1]
    url = "https://api.github.com/repos/OliviaLynn/gh-actions/dash/actions/runs"
    
    payload = {}
    headers = {
      'accept': 'application/vnd.github+json',
      'Authorization': f'Bearer {token}'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()
    for key, value in json_response.items():
            print(key, ":", value)
