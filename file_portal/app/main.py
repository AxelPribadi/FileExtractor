from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.upload import router
# import logfire

app = FastAPI()
app.include_router(router)
templates = Jinja2Templates(directory="app/templates")
app.mount("/app/static",StaticFiles(directory="app/static"), name="static")
# logfire.configure()
# logfire.instrument_fastapi(app)


@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    # return {"axel":"pribadi"}


if __name__ == "__main__":
    print(1)
