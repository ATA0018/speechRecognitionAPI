import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status

from core.Response import success
from models.asr_models import TranscriptionData, TranscriptionSuccessResponse
from services.asr_service import ASRService

router = APIRouter()


def get_asr_service(request: Request) -> ASRService:
    service = getattr(request.app.state, "asr_service", None)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ASR 服务未初始化",
        )
    return service


@router.post(
    "/transcribe",
    response_model=TranscriptionSuccessResponse,
    summary="音频识别",
    description=(
        "**在 Swagger（/docs）里调试：** 请点击 **Choose File** 选择本地音频后再点 **Execute**。"
        "不要在输入框里填写 ` /path/to.wav` 或 `@/path`——那是终端 curl 的写法，填进 Swagger 会变成普通字符串，导致报错 "
        "`Expected UploadFile, received: str`。\n\n"
        "**关于「复制 curl」：** Swagger UI 生成的 multipart 请求往往带 `Content-Type: multipart/form-data`且**没有 boundary**，"
        "复制到终端执行会失败；请在页面内 Execute，或自行使用 `curl -F 'file=@/真实路径' URL`（不要手写该 Content-Type 头）。"
    ),
)
async def transcribe_audio(
    file: UploadFile = File(
        ...,
        description="本地音频文件。Swagger 中必须用文件选择器上传，勿粘贴路径。",
    ),
    asr_service: ASRService = Depends(get_asr_service),
) -> TranscriptionSuccessResponse:
    suffix = Path(file.filename or "audio.wav").suffix or ".wav"
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_path = Path(temp_file.name)
    temp_file.close()

    try:
        with temp_path.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)

        result = asr_service.transcribe(str(temp_path))
        payload = success(
            data=TranscriptionData(**result).model_dump(),
            msg="识别成功",
        )
        return TranscriptionSuccessResponse.model_validate(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"识别失败: {exc}",
        ) from exc
    finally:
        if temp_path.exists():
            temp_path.unlink()
