import requests
import json

def _get_info() -> dict:
    url = "https://api.github.com/BtbN/FFmpeg-Builds/releases/latest"
    # response = requests.get(url)
    # return response.json()
    with open("info.json") as f:
        return json.loads(f.read())

result = _get_info()
filenames = []
print(f"Release Name: {result['name']}")
for d in result["assets"]:
    print(f"  - {d['name']}")
    filenames.append(d["name"])

