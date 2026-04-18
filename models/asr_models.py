from pydantic import BaseModel, Field


class TranscriptionData(BaseModel):
    language: str = Field(default="unknown", description="识别语言")
    text: str = Field(default="", description="识别文本")


class TranscriptionSuccessResponse(BaseModel):
    """识别成功时的标准包体（与 core.Response.StandardResponse 字段一致）。"""

    code: int = Field(default=200, description="业务状态码")
    message: str = Field(default="", description="说明信息")
    data: TranscriptionData
