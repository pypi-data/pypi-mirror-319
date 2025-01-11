import requests

PATH_LOGIN = "http://192.168.5.195:7004/api/auth/login"
BASIC_TOKEN = "Y2NpYjpjY2li"


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
