from crawler import ExhibitionRuleCrawler
from init_db import setup_database


def demo_crawling():
    print("=== 전시회 규칙 크롤링 데모 ===")
    print()

    print("1. 데이터베이스 초기화 중...")
    setup_database()
    print()

    print("2. 크롤링 시작...")
    urls = [
        "https://gsma.my.site.com/mwcoem/s/New%20for%202026",
        "https://gsma.my.site.com/mwcoem/s/Event%20Rules%20and%20Regulations",
        "https://gsma.my.site.com/mwcoem/s/Stand%20Build%20Rules%20and%20Regulations",
    ]

    crawler = ExhibitionRuleCrawler()

    for i, url in enumerate(urls, 1):
        print(f"  {i}/3 크롤링 중: {url}")
        html = crawler.fetch_page(url)
        if html:
            parsed_data = crawler.parse_page(html, url)
            if parsed_data["categories"]:
                crawler.save_to_database(parsed_data)
                print(f"    ✅ 완료: {len(parsed_data['categories'])}개 카테고리 저장")
            else:
                print(f"    ⚠️  데이터 없음")
        else:
            print(f"    ❌ 실패")
        print()

    print("3. 크롤링 완료!")
    print("   웹 인터페이스에서 결과를 확인하세요: http://localhost:8000")


if __name__ == "__main__":
    demo_crawling()
