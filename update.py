import requests

if __name__ == "__main__":
    url = "https://api.github.com/repos/lincc-frameworks/tape/actions/runs"
    
    payload = {}
    headers = {
      'accept': 'application/vnd.github+json',
      'Authorization': 'Bearer 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'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    print(response.text)
