# 加载 .env 文件
from dotenv import load_dotenv
load_dotenv()

from services.log_service import get_logger
logger=get_logger(server_name="bee")
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import chat, embeddings, rerank
from services import env_service
from services.http_service import http_clients
from jinja2 import Environment, FileSystemLoader

bee_version = "1.1.0"
bee_description = "欢迎使用 Bee, 一个轻量级 LLM API 代理"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await http_clients.startup()
    yield
    await http_clients.shutdown()

app = FastAPI(title="Bee",
              version=bee_version,
              description=bee_description,
              docs_url=None,
              redoc_url=None,
              openapi_url="/openapi.json",
              lifespan=lifespan)

# 挂载静态文件（确保静态资源能被访问）
app.mount("/static", StaticFiles(directory="static"), name="static")

# 自定义 Jinja2 环境，改用 [{[ ]}] 作为变量定界符
env = Environment(
    loader=FileSystemLoader("static"),
    variable_start_string="[[",   # 改成 [[ 和 ]]
    variable_end_string="]]",
    autoescape=True,
)

# 模板
jinja_templates = Jinja2Templates(env=env)

if env_service.get_show_swagger()=="true":
    # 自定义 /docs 页面
    @app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
    def custom_swagger_ui(request: Request):
        template_response=jinja_templates.TemplateResponse(
            "swagger/index.html",
            {
                "request": request,
                "title": "swagger - bee",
                "openapi_url": app.openapi_url,
            }
        )
        return template_response

if env_service.get_show_redoc()=="true":
    # 自定义 /redoc 页面
    @app.get("/redoc", include_in_schema=False, response_class=HTMLResponse)
    def custom_redoc_ui(request: Request):
        template_response=jinja_templates.TemplateResponse(
            "redoc/index.html",
            {
                "request": request,
                "title": "redoc - bee",
                "openapi_url": app.openapi_url,
            }
        )
        return template_response

app.include_router(chat.router)
app.include_router(embeddings.router)
app.include_router(rerank.router)

@app.get(path="/",include_in_schema=False)
def home(request: Request):
    template_response=jinja_templates.TemplateResponse(
            "home/index.html",
            {
                "request": request,
                "title": "home - bee",
                "bee_version":bee_version,
            }
        )
    return template_response
    
@app.get(path="/version",
         tags=["Default"])
@app.get(path="/v",
         tags=["Default"],include_in_schema=False)
def version():
    return {
        "description": bee_description,
        "name":"Bee",
        "version":bee_version,
        }