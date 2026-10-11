# Frontend preset regression check

Install Python Playwright and Chromium:

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
```

Serve the frontend from the repository root:

```sh
python3 -m http.server 3000 --bind 127.0.0.1 --directory webapp/static
```

Run the browser check:

```sh
python3 test/frontend/test_preset_wiring.py
```

Pass `--url https://your-worker.workers.dev/` to check deployed assets.
This regression check intercepts API requests and verifies that each of the
208 preset buttons submits its SQL statement rather than its display title.
It does not test database execution or modify database records.
