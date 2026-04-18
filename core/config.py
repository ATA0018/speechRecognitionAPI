import os
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_static_model_dir() -> Path:
    return project_root() / "static" / "models" / "Qwen3-ASR"


def legacy_lab2_model_dir() -> Path:
    return project_root() / "lab2-speech-recognition" / "Qwen3-ASR"


def is_qwen3_ov_model_dir(d: Path) -> bool:
    """目录内是否具备 OpenVINO Qwen3-ASR 导出（自包含或 optimum-intel thinker 布局）。"""
    if not d.is_dir() or not (d / "config.json").is_file():
        return False
    self_contained = (d / "openvino_language_model.xml").is_file() and (
        d / "openvino_audio_conv_model.xml"
    ).is_file()
    optimum = (d / "thinker" / "openvino_thinker_language_model.xml").is_file() and (
        d / "thinker" / "openvino_thinker_audio_model.xml"
    ).is_file()
    return self_contained or optimum


def resolve_asr_model_dir() -> Path:
    """
    解析 ASR 权重目录，优先级：
    1. 环境变量 ASR_MODEL_DIR
    2. static/models/Qwen3-ASR（随应用分发的静态资源）
    3. lab2-speech-recognition/Qwen3-ASR（兼容旧布局）
    """
    env = (os.environ.get("ASR_MODEL_DIR") or "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if not is_qwen3_ov_model_dir(p):
            raise FileNotFoundError(
                f"ASR_MODEL_DIR 中缺少有效的 Qwen3-ASR OpenVINO 文件: {p}"
            )
        return p

    for candidate in (default_static_model_dir(), legacy_lab2_model_dir()):
        if is_qwen3_ov_model_dir(candidate):
            return candidate

    raise FileNotFoundError(
        "未找到 Qwen3-ASR 模型目录。请将完整权重放入 static/models/Qwen3-ASR，"
        "或设置环境变量 ASR_MODEL_DIR 指向该目录。"
    )


def asr_device() -> str:
    return (os.environ.get("ASR_DEVICE") or "CPU").strip() or "CPU"
