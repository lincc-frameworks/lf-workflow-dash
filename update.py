import requests
import sys

if __name__ == "__main__":
    token = sys.argv[1]
    url = "https://api.github.com/repos/lincc-frameworks/tape/actions/runs"
    
    payload = {}
    headers = {
      'accept': 'application/vnd.github+json',
      'Authorization': f'Bearer {token}'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    print(response.json()[total_count])
