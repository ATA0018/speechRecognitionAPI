# -*- coding: utf-8 -*-
from typing import Any, List, Optional, Sequence

from pydantic import BaseModel, Field


def res_antd(
    data: Optional[Sequence[Any]] = None,
    total: int = 0,
    code: bool = True,
) -> dict:
    """
    支持 ant-design-table 的返回格式。
    """
    rows: List[Any] = list(data) if data is not None else []
    return {
        "success": code,
        "data": rows,
        "total": total,
    }


def base_response(code: int, msg: str, data: Any = None) -> dict:
    """基础返回：HTTP 业务码 + 文案 + 载荷。"""
    return {
        "code": code,
        "message": msg,
        "data": data,
    }


def success(data: Any = None, msg: str = "") -> dict:
    """成功：code=200。"""
    return base_response(200, msg, data)


def fail(code: int = -1, msg: str = "", data: Any = None) -> dict:
    """失败：自定义业务 code（可与 HTTP 状态码对齐）。"""
    return base_response(code, msg, data)


class StandardResponse(BaseModel):
    """与 success / fail 一致的统一 JSON 结构，供 OpenAPI 与校验使用。"""

    code: int = Field(..., description="业务状态码，成功一般为 200")
    message: str = Field(default="", description="说明信息")
    data: Any = Field(default=None, description="业务数据，结构随接口而定")
