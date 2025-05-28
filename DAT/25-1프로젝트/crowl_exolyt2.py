import pandas as pd
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 📌 엑셀에서 Username 리스트 읽기
def get_usernames():
    excel_path = r'D:/김동영/11_Github/mygit-1/DAT/25-1프로젝트/소셜핸들.xlsx'
    df = pd.read_excel(excel_path)
    return df['Username'].dropna().apply(lambda x: x.lstrip('@')).tolist()

# 📌 통계 정보 추출 함수 (Avg. Views, Avg. Comments, Total Video Shares)
def extract_stats(soup):
    stat_labels = {
        "Avg. Views": "Average views",
        "Avg. Comments": "Average comments",
        "Total Video Shares": "Video shares"
    }

    stats = {k: None for k in stat_labels.keys()}

    for key, label_text in stat_labels.items():
        label_elem = soup.find(lambda tag: tag.name in ["div", "span"] and label_text.lower() in tag.get_text(strip=True).lower())
        if label_elem:
            parent = label_elem.find_parent()
            if parent:
                sibling_texts = [el.get_text(strip=True) for el in parent.find_all(["div", "span"]) if el != label_elem]
                for text in sibling_texts:
                    if any(c.isdigit() for c in text):
                        stats[key] = text
                        break

    return stats

# 📌 메인 크롤링 함수
def crawl():
    usernames = get_usernames()
    usernames = usernames[:1]  # ✅ 테스트용: 첫 번째 사용자만 크롤링
    print("사용할 usernames:", usernames)

    result_df = pd.DataFrame(columns=["username", "avg_views", "avg_comments", "video_promotions"])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="exolyt_login_state.json")  # 로그인 세션 필요
        page = context.new_page()

        for username in usernames:
            print(f"\n🚀 수집 시작: {username}")
            try:
                page.goto(f"https://exolyt.com/user/tiktok/{username}")
                time.sleep(5)  # 페이지 로딩 대기

                soup = BeautifulSoup(page.content(), "html.parser")
                stats = extract_stats(soup)

                result_df = pd.concat([result_df, pd.DataFrame([{
                    "username": username,
                    "avg_views": stats["Avg. Views"],
                    "avg_comments": stats["Avg. Comments"],
                    "video_promotions": stats["Total Video Shares"]
                }])], ignore_index=True)

                print(f"✅ {username} - 수집 성공")
            except Exception as e:
                print(f"❌ {username} - 오류 발생: {e}")

        browser.close()
        result_df.to_csv("크롤링_결과.csv", index=False, encoding='utf-8-sig')
        print("\n📄 최종 결과:")
        print(result_df)

# 📌 실행부
if __name__ == "__main__":
    crawl()
