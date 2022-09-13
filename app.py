from random import randint
from re import A
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
# @limiter.limit("10/minute")
async def root(request: fastapi.Request):

    return templates.TemplateResponse("index.html", {"request": request, "homepage": extras.homepage_content})

@app.get("/recent", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def root(request: fastapi.Request):

    return templates.TemplateResponse("index.html", {"request": request, "homepage": extras.recent_content})

@app.get("/oldest", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def root(request: fastapi.Request):

    return templates.TemplateResponse("index.html", {"request": request, "homepage": extras.homepage_content})


@app.get("/about", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def root(request: fastapi.Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/login", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def login_page(request: fastapi.Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/profile/{username}", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def login_page(request: fastapi.Request, username:str):
    data = extras.get_userinfo(username)
    return templates.TemplateResponse("Profile.html", {"request": request, "username": data[0], "description": data[1]})


@app.get("/signin", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def login_page(request: fastapi.Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/submit", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("5/minute")
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

@app.get("/auth", response_class=fastapi.responses.JSONResponse)
# @limiter.limit("5/minute")
async def login_authentication(request: fastapi.Request, username:str, password:str):
    return {"status": extras.usercheck(username, password)}

@app.get("/sign-in", response_class=fastapi.responses.JSONResponse)
# @limiter.limit("5/minute")
async def login_authentication(request: fastapi.Request, username:str, password:str):
    return {"status": extras.adduser(username, password)}

@app.get("/submit-idea", response_class=fastapi.responses.HTMLResponse)
# @limiter.limit("10/minute")
async def login_authentication(request: fastapi.Request):
    pass

# endregion