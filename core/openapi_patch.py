# -*- coding: utf-8 -*-
"""修正 OpenAPI 中与 Swagger UI 的兼容性（multipart 文件控件等）。"""
from typing import Any


def patch_schemas_for_swagger_multipart_files(schema: dict[str, Any]) -> None:
    """
    Pydantic v2 / OpenAPI 3.1 对上传文件常输出 contentMediaType，而 Swagger UI
    对 multipart 需要 type:string + format:binary（OpenAPI 3.0 约定）才会显示「选择文件」。
    """
    components = schema.get("components")
    if not isinstance(components, dict):
        return
    schemas = components.get("schemas")
    if not isinstance(schemas, dict):
        return
    for definition in schemas.values():
        if not isinstance(definition, dict) or definition.get("type") != "object":
            continue
        props = definition.get("properties")
        if not isinstance(props, dict):
            continue
        for sub in props.values():
            if not isinstance(sub, dict):
                continue
            if sub.get("type") == "string" and "contentMediaType" in sub:
                sub["format"] = "binary"
                sub.pop("contentMediaType", None)
