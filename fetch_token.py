import httpx
import base64
import re

# Base64-encoded values (hidden)
encoded_url = "aHR0cHM6Ly90di52YWFuYW0yNC5jb20vbGl2ZS5tM3U4P2M9WkVFVEhJUkFJSEQy"
encoded_host = "dHYudmFhbmFtMjQuY29t"
encoded_origin = "aHR0cHM6Ly90di52YWFuYW0yNC5jb20v"
encoded_referer = "aHR0cHM6Ly90di52YWFuYW0yNC5jb20v"

# Decode Base64
url = base64.b64decode(encoded_url).decode()
host = base64.b64decode(encoded_host).decode()
origin = base64.b64decode(encoded_origin).decode()
referer = base64.b64decode(encoded_referer).decode()

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; Pixel 4 Build/RD2A.211001.002)",
    "Connection": "keep-alive",
    "Host": host,
    "Origin": origin,
    "Referer": referer
}

cookie_file = "cookie.txt"

with httpx.Client(http2=True, headers=headers, follow_redirects=True, timeout=20) as client:
    response = client.get(url)

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        exit(1)

    # Extract all ?token=… entries (case-insensitive)
    tokens = re.findall(r"\?token=[A-Za-z0-9\-]+", response.text)
    if tokens:
        with open(cookie_file, "w") as f:
            for t in tokens:
                f.write(t + "\n")
        print(f"{len(tokens)} token(s) saved to {cookie_file}")
    else:
        print("Token not found in playlist")
        # Save full playlist for debugging
        with open(cookie_file, "w") as f:
            f.write(response.text)
