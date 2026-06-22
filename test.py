import httpx

import httpx

def sendRequest(method, path, **kwargs):
    r = method(f"http://localhost:8000/{path}", **kwargs)

    print(r.text)
    print(r.status_code)
    return r

r = sendRequest(
    httpx.get,
    "",
)

# Auth
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

# Pastes
r = sendRequest(
    httpx.post,
    "pastes/",
    headers={"authorization": token},
    json={
        "content": "hello world",
        "visibility": "public"
    }
)
paste_id = r.json()["id"]

r = sendRequest(
    httpx.post,
    "pastes/",
    headers={"authorization": token},
    json={
        "content": "unlisted paste",
        "visibility": "unlisted"
    }
)

r = sendRequest(
    httpx.post,
    "pastes/",
    headers={"authorization": token},
    json={
        "content": "secret paste",
        "visibility": "private"
    }
)

r = sendRequest(
    httpx.get,
    "pastes/?page=1",
    headers={"authorization": token},
)

r = sendRequest(
    httpx.get,
    "pastes/?page=1&only_own=true",
    headers={"authorization": token},
)

r = sendRequest(
    httpx.get,
    f"pastes/{paste_id}",
    headers={"authorization": token},
)

r = sendRequest(
    httpx.delete,
    f"pastes/{paste_id}",
    headers={"authorization": token},
)

r = sendRequest(
    httpx.get,
    f"pastes/{paste_id}",
    headers={"authorization": token},
)