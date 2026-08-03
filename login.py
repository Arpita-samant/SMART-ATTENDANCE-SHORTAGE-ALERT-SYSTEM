#!C:\Users\HP\AppData\Local\Programs\Python\Python313\python.exe
import os
import sys
import urllib.parse

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def parse_post_data():
    content_length = int(os.environ.get("CONTENT_LENGTH", 0))
    body = sys.stdin.read(content_length)
    return urllib.parse.parse_qs(body)

def main():
    data = parse_post_data()

    username = data.get("username", [""])[0].strip()
    password = data.get("password", [""])[0].strip()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        print("Content-Type: text/html")
        print()
        print("""
<html>
<head>
<meta http-equiv="refresh" content="0; url=/dashboard.html">
</head>
<body>Redirecting to dashboard...</body>
</html>
""")
    else:
        print("Content-Type: text/html")
        print()
        print("""
<html>
<head>
<meta http-equiv="refresh" content="0; url=/login.html?error=1">
</head>
<body>Invalid credentials. Redirecting...</body>
</html>
""")

main()