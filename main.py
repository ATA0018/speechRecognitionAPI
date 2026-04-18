from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from core.Response import StandardResponse, fail, success
from routers import asr_router
from services.asr_service import ASRService

BASE_DIR = Path(__file__).resolve().parent

OPENAPI_TAGS_METADATA = [
    {
        "name": "Root",
        "description": "根路径与服务状态! ",
    },
    {
        "name": "ASR",
        "description": (
            "语音识别：上传音频返回文本。"
            "统一 JSON 结构为 **`code`** / **`message`** / **`data`**；"
            "出错时 HTTP 状态码与 **`code`** 一致，正文仍为上述结构!"
        ),
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    asr_service = ASRService()
    asr_service.initialize()
    app.state.asr_service = asr_service
    yield


app = FastAPI(
    title="Speech Recognition API",
    summary="Qwen3-ASR（OpenVINO）语音识别 HTTP API",
    description=(
        "基于 **Qwen3-ASR** 与 **OpenVINO** 的离线语音识别服务。"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=OPENAPI_TAGS_METADATA,
    servers=[
        {"url": "/", "description": "当前主机（默认 uvicorn 根路径）"},
    ],
    contact={
        "name": "SpeechRecognition API",
    },
    openapi_external_docs={
        "description": "Qwen3-ASR 模型与能力说明（Hugging Face）",
        "url": "https://huggingface.co/Qwen/Qwen3-ASR",
    },
    swagger_ui_parameters={
        "docExpansion": "list",
        "defaultModelsExpandDepth": 2,
        "displayRequestDuration": True,
        "filter": True,
        "tryItOutEnabled": True,
    },
)

# 部分代码生成/网关仅认 OpenAPI 3.0.x；未使用 3.1 专有特性时可固定为 3.0.2
app.openapi_version = "3.0.2"

_static_dir = BASE_DIR / "static"
if _static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(asr_router.router, prefix="/api/asr", tags=["ASR"])


@app.exception_handler(HTTPException)
async def http_exception_standard_response(_request: Request, exc: HTTPException) -> JSONResponse:
    """将 HTTPException 统一为 code / message / data 结构。"""
    detail = exc.detail
    msg = detail if isinstance(detail, str) else str(detail)
    body = fail(code=exc.status_code, msg=msg, data=None)
    return JSONResponse(status_code=exc.status_code, content=body)


@app.get("/", response_model=StandardResponse, tags=["Root"])
async def root() -> StandardResponse:
    return StandardResponse.model_validate(
        success(data={"service": "speech-recognition-api"}, msg="SpeechRecognition API is running")
    )


def custom_openapi() -> dict:
    """生成 OpenAPI 后打补丁，使 Swagger UI 对 multipart 文件显示「选择文件」。"""
    if app.openapi_schema is not None:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        summary=app.summary,
        description=app.description,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,
        webhooks=app.webhooks.routes,
        tags=app.openapi_tags,
        servers=app.servers,
        separate_input_output_schemas=app.separate_input_output_schemas,
        external_docs=app.openapi_external_docs,
    )
    from core.openapi_patch import patch_schemas_for_swagger_multipart_files

    patch_schemas_for_swagger_multipart_files(openapi_schema)
    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi
