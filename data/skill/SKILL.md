---
name: local-asr-fastapi-runner
description: Runs and validates a local FastAPI speech recognition service based on Qwen3-ASR OpenVINO models. Use when the user asks to start local ASR API, test /api/asr/transcribe, validate FastAPI module before hardware integration, or prepare Skill run evidence for challenge submissions.
---

# Local ASR FastAPI Runner

## Purpose

Provide a stable workflow to run and verify the local speech recognition API before UNO + ESP8266 hardware integration.

## Scope

This skill only covers the FastAPI module:

- start service
- health check
- transcribe test
- evidence checklist for challenge write-up

## Required Paths

- API root: `/Users/yourpath/Desktop/speechRecognition/speechRecognitionAPI/speechRecognitionAPI`
- model path dependency: `../lab2-speech-recognition/Qwen3-ASR` (resolved by service code)

## Workflow

Copy and execute this checklist:

```text
FastAPI Skill Progress
- [ ] Step 1: install dependencies
- [ ] Step 2: start API service
- [ ] Step 3: run health check
- [ ] Step 4: run transcription test
- [ ] Step 5: collect screenshot evidence
```

### Step 1: install dependencies

```bash
cd /Users/yourpath/Desktop/speechRecognition/speechRecognitionAPI/speechRecognitionAPI
pip install -r requirements.txt
```

### Step 2: start API service

```bash
cd /Users/yourpath/Desktop/speechRecognition/speechRecognitionAPI/speechRecognitionAPI
uvicorn main:app --host 0.0.0.0 --port 8060 --reload
```

Expected: Uvicorn shows startup logs and no import/model-load errors.

### Step 3: run health check

```bash
curl -s http://127.0.0.1:8060/
```

Expected: JSON indicates service is running.

### Step 4: run transcription test

```bash
curl -X POST "http://127.0.0.1:8060/api/asr/transcribe" \
  -H "accept: application/json" \
  -F "file=@/Users/yourpath/Desktop/speechRecognition/data/records/sample_en.wav"
```

Expected:

- HTTP 200
- response contains `data.text`
- response contains `data.language`

### Step 5: collect screenshot evidence

Capture at least:

1. terminal startup success
2. health check response
3. transcribe response
4. optional Swagger test page

## Failure Handling

- If startup fails, check Python environment and `requirements.txt`.
- If transcription fails, verify model files exist under `lab2-speech-recognition/Qwen3-ASR`.
- If curl fails from device, use LAN IP instead of `127.0.0.1`.

## Output Format

When reporting results, use:

```markdown
## FastAPI Skill Run Result
- Status: success | failed
- Health check: pass | fail
- Transcribe: pass | fail
- Notes: <short reason or blocker>
```
