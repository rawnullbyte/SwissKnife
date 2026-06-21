import httpx

import httpx

def sendRequest(method, path, **kwargs):
    r = method(f"http://localhost:8000/{path}", **kwargs)

    print(r.text)
    print(r.status_code)
    return r

r = sendRequest(
    httpx.post,
    "auth/register",
    json={
        "username": "null",
        "password": "test"
    }
)

r = sendRequest(
    httpx.post,
    "auth/login",
    json={
        "username": "null",
        "password": "test"
    }
)
token = f"Bearer {r.json()["token"]}"

r = sendRequest(
    httpx.get,
    "auth/account",
    headers={
        "authorization": token
    }    
)