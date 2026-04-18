# SpeechRecognition API

基于 `lab2-speech-recognition/Qwen3-ASR` 权重，提供 FastAPI 音频识别接口。
Qwen3-ASR 是通义千问团队推出的自动语音识别模型，支持 52 种语言和方言的语音识别和语言识别。该模型基于 Qwen3-Omni 的强大音频理解能力和大规模语音训练数据，在开源 ASR 模型中达到了最先进的性能。

主要特点:

    🌍 支持 30 种语言和 22 种中文方言的语音识别
    ⚡ 0.6B 版本在保持高精度的同时实现极高吞吐量
    🎤 支持流式/离线统一推理
    📏 支持长音频转写

在本实验中，我们将：

    从 ModelScope 下载预转换的 OpenVINO 模型
    使用 OpenVINO 加载并运行语音识别
    体验交互式 Gradio 语音识别演示


## 📋 目录结构

```
speechRecognitionAPI/
├── main.py                 # FastAPI 入口
├── routers/                # API 路由
│   └── asr_router.py
├── services/               # 业务逻辑
│   └── asr_service.py
├── models/                 # 数据模型
│   └── asr_models.py
├── asr_engine/             # ASR 引擎
├── core/                   # 核心配置
├── static/models/          # AI 模型文件（需单独下载）
├── data/                   # 测试数据（可选）
├── docs/                   # 文档
├── requirements.txt        # 依赖列表
├── usage_guide.ipynb       # Jupyter 使用手册
└── .gitignore             # Git 忽略配置
```

## ⚠️ 重要：模型文件准备

由于模型文件较大（约 2GB+），未包含在 Git 仓库中。**首次使用前**需要下载模型文件。

### 📥 自动下载模型（推荐）

项目已集成自动下载功能，首次运行时会自动从 ModelScope 下载模型。您也可以手动执行以下代码：

```python
from pathlib import Path

model_dir = Path("Qwen3-ASR-0.6B-fp16-ov")

if not model_dir.exists():
    from modelscope import snapshot_download
    snapshot_download("snake7gun/Qwen3-ASR-0.6B-fp16-ov", local_dir=str(model_dir))
    print(f"模型已下载到: {model_dir}")
else:
    print(f"模型已存在: {model_dir}，跳过下载")
```

**注意**：首次下载需要安装 `modelscope`：
```bash
pip install modelscope
```

### 📂 模型文件说明

下载完成后，需要将模型文件移动到正确的位置：

```bash
# 创建目标目录
mkdir -p static/models/Qwen3-ASR

# 移动模型文件
cp -r Qwen3-ASR-0.6B-fp16-ov/* static/models/Qwen3-ASR/
```

或者修改代码中的模型路径配置。

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/your-username/speechRecognitionAPI.git
cd speechRecognitionAPI
```

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 3️⃣ 下载模型

```python
model_dir = Path("static/models/Qwen3-ASR")

# 确保目录存在
model_dir.mkdir(parents=True, exist_ok=True)

if not any(model_dir.iterdir()):  # 检查目录是否为空
    print("🔄 开始下载模型到 static/models/Qwen3-ASR...")
    print(f"📍 下载路径: {model_dir.absolute()}")
    
    from modelscope import snapshot_download
    snapshot_download(
        "snake7gun/Qwen3-ASR-0.6B-fp16-ov", 
        local_dir=str(model_dir)
    )
    print(f"✅ 模型已下载到: {model_dir}")
else:
    print(f"✅ 模型已存在: {model_dir}")
    print("⏭️  跳过下载步骤")
```

然后移动模型到正确位置（也可以不用移动）：

```bash
mkdir -p static/models/Qwen3-ASR
cp -r Qwen3-ASR-0.6B-fp16-ov/* static/models/Qwen3-ASR/
```

### 4️⃣ 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8060 --reload
```

## 📡 API 接口

- `GET /`：服务健康检查
- `POST /api/asr/transcribe`：上传音频识别
  - 表单字段：`file`

## 📝 示例请求

```bash
curl -X POST "http://127.0.0.1:8060/api/asr/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/audio.wav"
```

## Swagger UI（交互文档）
http://127.0.0.1:8060/docs

## ReDoc
http://127.0.0.1:8060/redoc

## OpenAPI JSON 规范
http://127.0.0.1:8060/openapi.json

## 📚 更多资源
- 📖 [Jupyter 使用手册](usage_guide.ipynb) - 详细的交互式使用指南

