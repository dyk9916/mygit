import pandas as pd
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# ✅ 엑셀에서 Username 리스트 불러오기
def get_usernames():
    excel_path = r'D:/김동영/11_Github/mygit-1/DAT/25-1프로젝트/소셜핸들.xlsx'
    df = pd.read_excel(excel_path)
    return df['Username'].dropna().apply(lambda x: x.lstrip('@')).tolist()

# ✅ 통계 정보 추출 함수 (Likes, Total Video Shares를 라벨 기준으로 정확하게 탐색)
def extract_stats(soup):
    stats = {"Likes": None, "Total Video Shares": None}  # 수집하려는 라벨들

    for label in stats.keys():
        # 🎯 'Likes' 또는 'Total Video Shares' 텍스트가 포함된 div/span 찾기
        label_elem = soup.find(
            lambda tag: tag.name in ["div", "span"] and label.lower() in tag.get_text(strip=True).lower()
        )
        if label_elem:
            # 📌 해당 라벨이 있는 태그의 부모 요소 탐색
            parent = label_elem.find_parent()
            if parent:
                # 👀 부모 내부에서 형제 요소들 중 숫자를 포함한 요소만 추출
                siblings = parent.find_all(["div", "span"])
                for sib in siblings:
                    text = sib.get_text(strip=True)
                    if sib != label_elem and any(c.isdigit() for c in text):
                        stats[label] = text  # 🎯 실제 수치를 여기에 저장
                        break

    return stats  # {'Likes': '1.2M', 'Total Video Shares': '5.3K'} 형태로 반환

# ✅ 메인 크롤링 함수
def crawl():
    usernames = get_usernames()
    print("사용할 usernames:", usernames)

    # 📄 결과 저장용 빈 데이터프레임 생성
    result_df = pd.DataFrame(columns=["username", "likes", "total_video_shares"])

    with sync_playwright() as p:
        # 🔐 크롬 브라우저 열기 + 로그인 세션 불러오기
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="exolyt_login_state.json")
        page = context.new_page()

        for username in usernames:
            print(f"\n🚀 수집 시작: {username}")
            try:
                # 🌐 TikTok 계정 분석 페이지 이동
                page.goto(f"https://exolyt.com/user/tiktok/{username}")
                time.sleep(5)  # ⏳ 페이지 로딩 대기

                soup = BeautifulSoup(page.content(), "html.parser")  # 🧪 HTML 분석 준비
                stats = extract_stats(soup)  # 📥 통계 정보 수집

                # 📊 결과를 데이터프레임에 추가
                result_df = pd.concat([result_df, pd.DataFrame([{
                    "username": username,
                    "likes": stats["Likes"],
                    "total_video_shares": stats["Total Video Shares"]
                }])], ignore_index=True)

                print(f"✅ {username} - 수집 성공")
            except Exception as e:
                print(f"❌ {username} - 오류 발생: {e}")

        browser.close()  # 💻 브라우저 종료

    # 💾 CSV로 저장
    result_df.to_csv("크롤링_결과.csv", index=False, encoding="utf-8-sig")
    print("\n📄 최종 결과:")
    print(result_df)

# ✅ 프로그램 시작 지점
if __name__ == "__main__":
    crawl()
