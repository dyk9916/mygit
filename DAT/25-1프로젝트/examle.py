from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://exolyt.com")

    print("🔐 수동으로 로그인하세요. 완료 후 이 창 닫지 마세요.")
    input("✅ 로그인 후 Enter 키를 누르세요...")

    context.storage_state(path="exolyt_login_state.json")
    print("💾 세션 저장 완료: exolyt_login_state.json")

    browser.close()

# Ctrl + Shift + P → Python: Select Interpreter (3.12.6 64bit 선택)
# 터미널에 cd Desktop/
# 이후 터미널에 python examle.py