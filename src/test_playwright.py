from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("Chromium executable:", p.chromium.executable_path)
