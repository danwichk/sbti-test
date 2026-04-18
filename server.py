"""SBTI Personality Test - FastAPI Server"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="SBTI 性格测试")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve standalone HTML file at root
@app.get("/")
async def index():
    html_path = os.path.join(BASE_DIR, "sbti-test.html")
    return FileResponse(html_path, media_type="text/html")

# Serve individual files (for the multi-file version too)
@app.get("/style.css")
async def style():
    return FileResponse(os.path.join(BASE_DIR, "style.css"), media_type="text/css")

@app.get("/script.js")
async def script():
    return FileResponse(os.path.join(BASE_DIR, "script.js"), media_type="application/javascript")

# Serve static files from directory
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
