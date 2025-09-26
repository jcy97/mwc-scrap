import requests
from bs4 import BeautifulSoup
import re
from models import ExhibitionRule, RuleCategory, RuleItem, get_session
from sqlalchemy.orm import Session


class ExhibitionRuleCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def fetch_page(self, url):
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def parse_page(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

        title_element = soup.find("h1") or soup.find("h2") or soup.find("title")
        title = title_element.get_text(strip=True) if title_element else "Unknown Title"

        categories = {}

        if "New for 2026" in url:
            categories = self.parse_new_for_2026(soup)
        elif "Event Rules" in url:
            categories = self.parse_event_rules(soup)
        elif "Stand Build Rules" in url:
            categories = self.parse_stand_build_rules(soup)
        else:
            categories = self.parse_generic_rules(soup)

        return {"title": title, "url": url, "categories": categories}

    def parse_new_for_2026(self, soup):
        categories = {}

        h3_elements = soup.find_all("h3")
        for h3 in h3_elements:
            if h3.get_text(strip=True) and not h3.get_text(strip=True).startswith("<>"):
                category_name = h3.get_text(strip=True)

                items = []
                next_element = h3.find_next_sibling()
                while next_element and next_element.name != "h3":
                    if next_element.name == "p" and next_element.get_text(strip=True):
                        text = next_element.get_text(strip=True)
                        if len(text) > 20:
                            items.append(text)
                    next_element = next_element.find_next_sibling()

                if items:
                    categories[category_name] = items

        return categories

    def parse_event_rules(self, soup):
        categories = {}

        h3_elements = soup.find_all("h3")
        for h3 in h3_elements:
            category_name = h3.get_text(strip=True)
            if (
                not category_name
                or category_name.startswith("###")
                or len(category_name) < 3
            ):
                continue

            items = []
            next_element = h3.find_next_sibling()
            while next_element and next_element.name not in ["h1", "h2", "h3"]:
                if next_element.name == "p":
                    text = next_element.get_text(strip=True)
                    if len(text) > 20:
                        items.append(text)
                elif next_element.name == "ul":
                    for li in next_element.find_all("li"):
                        text = li.get_text(strip=True)
                        if text:
                            items.append(text)
                next_element = next_element.find_next_sibling()

            if items:
                categories[category_name] = items

        return categories

    def parse_stand_build_rules(self, soup):
        categories = {}

        section_headers = soup.find_all(["h2", "h3", "h4"])
        for header in section_headers:
            category_name = header.get_text(strip=True)
            if not category_name or len(category_name) < 5:
                continue

            items = []
            next_element = header.find_next_sibling()
            while next_element and next_element.name not in ["h1", "h2", "h3", "h4"]:
                if next_element.name == "p":
                    text = next_element.get_text(strip=True)
                    if len(text) > 30:
                        items.append(text)
                elif next_element.name == "ul":
                    for li in next_element.find_all("li"):
                        text = li.get_text(strip=True)
                        if text and len(text) > 10:
                            items.append(text)
                next_element = next_element.find_next_sibling()

            if items:
                categories[category_name] = items[:5]

        return categories

    def parse_generic_rules(self, soup):
        categories = {}

        all_headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        for header in all_headers:
            category_name = header.get_text(strip=True)
            if len(category_name) < 5:
                continue

            items = []
            next_element = header.find_next_sibling()
            count = 0
            while next_element and count < 10:
                if next_element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                    break

                if next_element.name == "p":
                    text = next_element.get_text(strip=True)
                    if len(text) > 20:
                        items.append(text)
                        count += 1
                elif next_element.name in ["ul", "ol"]:
                    for li in next_element.find_all("li"):
                        text = li.get_text(strip=True)
                        if text and len(text) > 10:
                            items.append(text)
                            count += 1
                            if count >= 10:
                                break

                next_element = next_element.find_next_sibling()

            if items:
                categories[category_name] = items

        return categories

    def save_to_database(self, parsed_data):
        db = get_session()
        try:
            existing_rule = (
                db.query(ExhibitionRule).filter_by(url=parsed_data["url"]).first()
            )
            if existing_rule:
                db.delete(existing_rule)
                db.commit()

            exhibition_rule = ExhibitionRule(
                url=parsed_data["url"], title=parsed_data["title"]
            )
            db.add(exhibition_rule)
            db.commit()
            db.refresh(exhibition_rule)

            for category_name, items in parsed_data["categories"].items():
                category = RuleCategory(
                    exhibition_rule_id=exhibition_rule.id,
                    name=category_name,
                    name_en=category_name,
                )
                db.add(category)
                db.commit()
                db.refresh(category)

                for idx, item in enumerate(items):
                    rule_item = RuleItem(
                        category_id=category.id,
                        content_ko=item,
                        content_en=item,
                        order_index=idx,
                    )
                    db.add(rule_item)

            db.commit()
            print(f"Successfully saved rules from {parsed_data['url']}")

        except Exception as e:
            db.rollback()
            print(f"Database error: {str(e)}")
        finally:
            db.close()

    def crawl_and_save(self, urls):
        for url in urls:
            print(f"Crawling {url}...")
            html = self.fetch_page(url)
            if html:
                parsed_data = self.parse_page(html, url)
                if parsed_data["categories"]:
                    self.save_to_database(parsed_data)
                    print(f"Found {len(parsed_data['categories'])} categories")
                else:
                    print(f"No categories found for {url}")
            else:
                print(f"Failed to fetch {url}")


def main():
    urls = [
        "https://gsma.my.site.com/mwcoem/s/New%20for%202026",
        "https://gsma.my.site.com/mwcoem/s/Event%20Rules%20and%20Regulations",
        "https://gsma.my.site.com/mwcoem/s/Stand%20Build%20Rules%20and%20Regulations",
    ]

    crawler = ExhibitionRuleCrawler()
    crawler.crawl_and_save(urls)


if __name__ == "__main__":
    main()
