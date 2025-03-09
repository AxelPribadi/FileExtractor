
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routes import router

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.include_router(router)

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# if __name__ == "__main__":
    # print(1)
    # file_extension = Path("app/main.py").suffix.lower()
    # print(file_extension)

