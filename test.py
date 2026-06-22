import httpx
import base64
import json


def sendRequest(method, path, **kwargs):
    r = method(f"http://localhost:8000/{path}", **kwargs)
    print(r.text)
    print(r.status_code)
    return r


# hello
r = sendRequest(httpx.get, "")

# auth
r = sendRequest(
    httpx.post,
    "auth/register",
    json={"username": "null", "password": "test"},
)

r = sendRequest(
    httpx.post,
    "auth/login",
    json={"username": "null", "password": "test"},
)
token = f"Bearer {r.json()['token']}"

r = sendRequest(
    httpx.get,
    "auth/account",
    headers={"authorization": token},
)

# hash
r = sendRequest(httpx.get, "hash", params={"type": "sha256", "data": "hello"})
r = sendRequest(httpx.get, "hash", params={"type": "md5", "data": "hello"})
r = sendRequest(httpx.get, "hash", params={"type": "sha512", "data": "hello"})
r = sendRequest(httpx.get, "hash", params={"type": "sha1", "data": "hello"})
r = sendRequest(httpx.get, "hash", params={"data": "hello"})  # missing type

# http
r = sendRequest(httpx.get, "http/200")
r = sendRequest(httpx.get, "http/404")
r = sendRequest(httpx.get, "http/418")
r = sendRequest(httpx.get, "http/500")
r = sendRequest(httpx.get, "http/999")  # custom unknown code
r = sendRequest(httpx.get, "http/1")  # out of range

# jwt
header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
payload = base64.urlsafe_b64encode(json.dumps({"sub": "123", "name": "John Doe", "iat": 1516239022}).encode()).rstrip(b"=").decode()
fake_token = f"{header}.{payload}.fakesignature"
r = sendRequest(httpx.get, f"jwt/{fake_token}")

# matrix
r = sendRequest(httpx.get, "matrix")  # non-curl user agent -> 418

# password
r = sendRequest(httpx.get, "password/")

# pastes
r = sendRequest(
    httpx.post,
    "pastes/",
    headers={"authorization": token},
    json={"content": "hello world", "visibility": "public"},
)
paste_id = r.json()["id"]

r = sendRequest(
    httpx.post,
    "pastes/",
    headers={"authorization": token},
    json={"content": "unlisted paste", "visibility": "unlisted"},
)

r = sendRequest(
    httpx.post,
    "pastes/",
    headers={"authorization": token},
    json={"content": "secret paste", "visibility": "private"},
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

# qr
r = sendRequest(httpx.get, "qr", params={"data": "https://example.com"})

# time
r = sendRequest(httpx.get, "time/")
r = sendRequest(httpx.get, "time/Europe/Prague")
r = sendRequest(httpx.get, "time/America/New_York")
r = sendRequest(httpx.get, "time/UTC")

# uuid
r = sendRequest(httpx.get, "uuid/")