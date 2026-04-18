from pathlib import Path
from typing import Any, Dict, Optional

from asr_engine import OVQwen3ASRModel
from core.config import asr_device, resolve_asr_model_dir


class ASRService:
    def __init__(self, model_dir: Optional[str] = None, device: Optional[str] = None) -> None:
        self._model = None
        self._model_dir = Path(str(model_dir)) if model_dir else None
        self._device = device

    def initialize(self) -> None:
        if self._model is not None:
            return

        model_dir = self._model_dir or resolve_asr_model_dir()
        device = self._device or asr_device()

        self._model = OVQwen3ASRModel.from_pretrained(
            model_dir=str(model_dir),
            device=device,
        )

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        if self._model is None:
            raise RuntimeError("ASR 模型尚未初始化")

        results = self._model.transcribe(audio=audio_path)
        if not results:
            return {"language": "unknown", "text": ""}

        result = results[0]
        return {
            "language": getattr(result, "language", "unknown") or "unknown",
            "text": getattr(result, "text", "") or "",
        }
