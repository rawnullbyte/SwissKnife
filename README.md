<h1 align="center">
    SwissKnife
</h1>

<p align="center">
  A general purpose API with random utilities.
</p>

<p align="center">
  Auto generated documentation is at: <strong>docs</strong>
</p>

---

## Available modules

You can disabe any module by adding `.disabled` at the end of the module folder.

- **auth** — account and authorization stuff
- **hash** — hashlib related utilities for hashing data
- **hello** — welcome message at /
- **http** — returning any status code
- **jwt** — decrypting JWT token data
- **matrix** — matrix effect in terminal using curl
- **password** — password generator
- **pastes** — pastebin like api
- **qr** — qr code generator
- **time** — get time in timezones, countries, states
- **uuid** — generate uuid4

---

## Running

```
pip install -r requirements.txt
python3 main.py
```

---

## Testing

Test all endpoints at once:

```
python3 test.py
```
