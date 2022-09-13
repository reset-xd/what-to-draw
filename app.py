from random import randint
import fastapi
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.templating import Jinja2Templates
import extras

limiter = Limiter(key_func=get_remote_address)
app = fastapi.FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="Static"), name="static")
templates = Jinja2Templates(directory="Templates")

# region [html]

@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def root(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request, "homepage": extras.homepage_content})

@app.get("/recent", response_class=fastapi.responses.HTMLResponse)
async def root(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request, "homepage": extras.recent_content})

@app.get("/oldest", response_class=fastapi.responses.HTMLResponse)
async def root(request: fastapi.Request):

    return templates.TemplateResponse("index.html", {"request": request, "homepage": extras.homepage_content})


@app.get("/about", response_class=fastapi.responses.HTMLResponse)
async def root(request: fastapi.Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/submit", response_class=fastapi.responses.HTMLResponse)
async def login_authentication(request: fastapi.Request):
    pass

# endregion

# region [internal]

@app.get("/random", response_class=fastapi.responses.RedirectResponse)
# @limiter.limit("20/minute")
async def random_idea(request: fastapi.Request):
    return "http://localhost:8000/idea/{0}".format(randint(1, extras.gen_id()-1))

@app.get("/idea/{idea_id}", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("5/minute")
async def login_authentication(request: fastapi.Request, idea_id:int):
    data = extras.get_idea_by_id(idea_id)
    return templates.TemplateResponse("PerPage.html", {"request": request, "title": data[1], "description": data[2], "tag": data[3]})

@app.get("/submit-idea", response_class=fastapi.responses.HTMLResponse)
@limiter.limit("1/minute")
async def sub_idea(request: fastapi.Request):
    pass

# endregion