from pydantic import BaseModel


class CoefficientEntry(BaseModel):
    feature: str
    coef: float


class PredictionEntry(BaseModel):
    row: int
    predicted_probability: float
    prediction: int


class ModelStats(BaseModel):
    model_type: str
    aic: float
    aicc: float
    bic: float
    num_parameters: int
    likelihood: float
    brier_score: float
    log_loss: float
    rmse: float
    acc_cv: float
    precision: float
    recall: float
    f1: float


class ModelResult(BaseModel):
    stats: ModelStats
    coefficients: list[CoefficientEntry]
    predictions: list[PredictionEntry]


class TrainResponse(BaseModel):
    models: dict[str, ModelResult]


class ValidateResponse(BaseModel):
    valid: bool
    errors: list[str]
