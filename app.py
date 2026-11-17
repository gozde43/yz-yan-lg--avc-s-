from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ana dizindeki tüm dosyaları (CSS, JS, JSON) statik olarak dışarıya açıyoruz
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def read_root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"error": "index.html bulunamadı"}

@app.get("/api/sorular")
def get_sorular():
    if os.path.exists("sorular.json"):
        return FileResponse("sorular.json", media_type="application/json")
    raise HTTPException(status_code=404, detail="sorular.json dosyası bulunamadı")