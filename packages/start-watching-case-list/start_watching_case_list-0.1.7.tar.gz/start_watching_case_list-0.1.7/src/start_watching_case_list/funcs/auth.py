import requests
import os
from dotenv import load_dotenv

load_dotenv()
PATH_LOGIN = os.getenv("PATH_LOGIN")
BASIC_TOKEN = os.getenv("BASIC_TOKEN")


def login(username, password):
    headers = {"Authorization": f"Basic {BASIC_TOKEN}", "Content-Type": "application/json"}
    url = PATH_LOGIN
    cookie = ""
    data = {"email": username, "password": password}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        cookies = response.cookies
        for cookie in cookies:
            cookie = cookie.value
    return cookie
