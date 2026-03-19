import json
import io

import pandas as pd
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request
from slowapi import Limiter
from app.deps import get_real_ip

from app.services.data_validator import validate_dataframe
from app.services.feature_engineering import feature_engineering
from app.services.model_trainer import train_model
from app.schemas.responses import TrainResponse, ValidateResponse, ModelResult

router = APIRouter()
limiter = Limiter(key_func=get_real_ip)

VALID_MODEL_TYPES = {"AFM", "PFM", "IFM"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


async def _read_and_check_size(file: UploadFile) -> bytes:
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)} MB",
        )
    return contents


@router.post("/api/validate", response_model=ValidateResponse)
@limiter.limit("30/minute")
async def validate(request: Request, file: UploadFile = File(...)):
    contents = await _read_and_check_size(file)
    try:
        df = pd.read_excel(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read XLSX file")

    errors = validate_dataframe(df)
    return ValidateResponse(valid=len(errors) == 0, errors=errors)


@router.post("/api/train", response_model=TrainResponse)
@limiter.limit("10/minute")
async def train(
    request: Request,
    file: UploadFile = File(...),
    model_types: str = Form(...),
):
    contents = await _read_and_check_size(file)
    try:
        df = pd.read_excel(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read XLSX file")

    errors = validate_dataframe(df)
    if errors:
        raise HTTPException(status_code=422, detail=errors)

    try:
        requested_types = json.loads(model_types)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="model_types must be a JSON array")

    invalid = set(requested_types) - VALID_MODEL_TYPES
    if invalid:
        raise HTTPException(
            status_code=400, detail=f"Invalid model types: {', '.join(invalid)}"
        )

    cleaned_df = feature_engineering(df)

    results: dict[str, ModelResult] = {}
    for mt in requested_types:
        results[mt] = train_model(cleaned_df, mt)

    return TrainResponse(models=results)
