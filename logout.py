#!/usr/bin/env python3
import http.cookies

cookie = http.cookies.SimpleCookie()
cookie["session"] = ""
cookie["session"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
cookie["session"]["path"] = "/"

print(cookie.output())
print("Content-Type: text/html")
print("Location: /login.html")
print()