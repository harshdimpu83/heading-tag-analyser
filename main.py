"""
Heading Tag Analyser - FastAPI App
Enter a website URL to see all H1-H6 heading tags with counts.
"""

import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from heading_analyzer_core import fetch_headings, get_total_headings, HEADING_TAGS

load_dotenv()

app = FastAPI(title="Heading Tag Analyser")
templates = Jinja2Templates(directory="templates")

APP_PASSWORD = os.getenv("APP_PASSWORD", "heading2026")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": None,
        "error": None,
        "url_input": "",
        "auth_error": False,
    })


@app.post("/analyse", response_class=HTMLResponse)
async def analyse(
    request: Request,
    password: str = Form(...),
    url: str = Form(...),
):
    # Password check
    if password != APP_PASSWORD:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": None,
            "error": None,
            "url_input": url,
            "auth_error": True,
        })

    result = fetch_headings(url.strip())

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result if result["success"] else None,
        "error": result["error"] if not result["success"] else None,
        "url_input": url,
        "auth_error": False,
        "heading_tags": HEADING_TAGS,
        "total": get_total_headings(result["headings"]) if result["success"] else 0,
    })
