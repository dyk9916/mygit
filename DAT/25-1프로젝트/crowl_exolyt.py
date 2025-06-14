import pandas as pd
from bs4 import BeautifulSoup
import time
from playwright.sync_api import sync_playwright

def get_usernames():
    excel_path = r'D:/김동영/11_Github/mygit-1/DAT/25-1프로젝트/소셜핸들.xlsx'
    df = pd.read_excel(excel_path)
    return df['Username'].dropna().apply(lambda x: x.lstrip('@')).tolist()

def extract_stats(soup):
    stats = {"Likes": None}
    label_map = {
        "Likes": "Likes"
    }

    for key, label in label_map.items():
        label_div = soup.find("div", string=lambda text: text and label.lower() in text.lower())
        if label_div:
            value_div = label_div.find_next_sibling("div")
            if value_div:
                stats[key] = value_div.get_text(strip=True)

    return stats

def crawl():
    usernames = get_usernames()
    usernames = usernames[:1]  # 첫 번째 사용자만 크롤링
    print("사용할 usernames:", usernames)

    result_df = pd.DataFrame(columns=["username", "Likes"])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="exolyt_login_state.json")
        page = context.new_page()

        for username in usernames:
            print(f"🚀 수집 시작: {username}")
            try:
                page.goto(f"https://exolyt.com/user/tiktok/{username}")
                time.sleep(5)
                soup = BeautifulSoup(page.content(), "html.parser")

                stats = extract_stats(soup)
                result_df = pd.concat([result_df, pd.DataFrame([{
                    "username": username,
                    "Likes": stats["Likes"]
                }])], ignore_index=True)

                print(f"✅ {username} - 수집 성공")
            except Exception as e:
                print(f"❌ {username} - 오류 발생: {e}")

        browser.close()
        result_df.to_csv("크롤링_결과.csv", index=False)
        print(result_df)

if __name__ == "__main__":
    crawl()