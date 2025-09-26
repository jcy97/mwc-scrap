from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import ExhibitionRule, RuleCategory, RuleItem, get_session
from crawler import ExhibitionRuleCrawler
from report_generator import PDFGenerator, PPTGenerator
import os
from datetime import datetime

app = FastAPI(title="Exhibition Rules Management System")

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    db = get_session()
    try:
        rules = db.query(ExhibitionRule).all()
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "rules": rules, "total_rules": len(rules)},
        )
    finally:
        db.close()


@app.get("/rule/{rule_id}", response_class=HTMLResponse)
async def get_rule_detail(request: Request, rule_id: int):
    db = get_session()
    try:
        rule = db.query(ExhibitionRule).filter(ExhibitionRule.id == rule_id).first()
        if rule:
            categories = (
                db.query(RuleCategory)
                .filter(RuleCategory.exhibition_rule_id == rule_id)
                .all()
            )
            for category in categories:
                category.items = (
                    db.query(RuleItem)
                    .filter(RuleItem.category_id == category.id)
                    .order_by(RuleItem.order_index)
                    .all()
                )

        return templates.TemplateResponse(
            "rule_detail.html",
            {
                "request": request,
                "rule": rule,
                "categories": categories if rule else [],
            },
        )
    finally:
        db.close()


@app.post("/crawl")
async def start_crawling(background_tasks: BackgroundTasks):
    background_tasks.add_task(crawl_data)
    return {"message": "크롤링이 시작되었습니다. 잠시 후 새로고침해주세요."}


def crawl_data():
    urls = [
        "https://gsma.my.site.com/mwcoem/s/New%20for%202026",
        "https://gsma.my.site.com/mwcoem/s/Event%20Rules%20and%20Regulations",
        "https://gsma.my.site.com/mwcoem/s/Stand%20Build%20Rules%20and%20Regulations",
    ]

    crawler = ExhibitionRuleCrawler()
    crawler.crawl_and_save(urls)


@app.get("/download/pdf")
async def download_pdf():
    db = get_session()
    try:
        rules = db.query(ExhibitionRule).all()
        all_data = []

        for rule in rules:
            categories = (
                db.query(RuleCategory)
                .filter(RuleCategory.exhibition_rule_id == rule.id)
                .all()
            )
            rule_data = {"title": rule.title, "url": rule.url, "categories": []}

            for category in categories:
                items = (
                    db.query(RuleItem)
                    .filter(RuleItem.category_id == category.id)
                    .order_by(RuleItem.order_index)
                    .all()
                )
                category_data = {
                    "name": category.name,
                    "items": [item.content_ko or item.content_en for item in items],
                }
                rule_data["categories"].append(category_data)

            all_data.append(rule_data)

        pdf_generator = PDFGenerator()
        filename = pdf_generator.generate_pdf(all_data)
        return FileResponse(
            path=filename,
            filename=f"exhibition_rules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            media_type="application/pdf",
        )
    finally:
        db.close()


@app.get("/download/ppt")
async def download_ppt():
    db = get_session()
    try:
        rules = db.query(ExhibitionRule).all()
        all_data = []

        for rule in rules:
            categories = (
                db.query(RuleCategory)
                .filter(RuleCategory.exhibition_rule_id == rule.id)
                .all()
            )
            rule_data = {"title": rule.title, "url": rule.url, "categories": []}

            for category in categories:
                items = (
                    db.query(RuleItem)
                    .filter(RuleItem.category_id == category.id)
                    .order_by(RuleItem.order_index)
                    .all()
                )
                category_data = {
                    "name": category.name,
                    "items": [item.content_ko or item.content_en for item in items],
                }
                rule_data["categories"].append(category_data)

            all_data.append(rule_data)

        ppt_generator = PPTGenerator()
        filename = ppt_generator.generate_ppt(all_data)
        return FileResponse(
            path=filename,
            filename=f"exhibition_rules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
