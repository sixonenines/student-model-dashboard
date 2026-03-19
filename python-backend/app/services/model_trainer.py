import numpy as np
import pandas as pd
from patsy import dmatrices
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import (
    log_loss,
    f1_score,
    precision_score,
    recall_score,
    brier_score_loss,
)

from app.schemas.responses import (
    ModelStats,
    CoefficientEntry,
    PredictionEntry,
    ModelResult,
)

FORMULAS = {
    "AFM": "Outcome ~ AnonStudentId + KCModel + KCModel:OpportunityModel",
    "PFM": "Outcome ~ AnonStudentId + KCModel + KCModel:(CorrectModel+IncorrectModel)",
    "IFM": "Outcome ~ AnonStudentId + KCModel + KCModel:(CorrectModel+IncorrectModel+TellsModel)",
}


def _deviance(X, y, model):
    return 2 * log_loss(y, model.predict_proba(X), normalize=False)


def _get_x(df: pd.DataFrame, model_type: str):
    formula = FORMULAS[model_type]
    _, X = dmatrices(formula, df, return_type="dataframe")
    return X


def train_model(df: pd.DataFrame, model_type: str) -> ModelResult:
    X = _get_x(df, model_type)
    y = df["Outcome"].astype(int)

    # Train on full data
    model = LogisticRegression(max_iter=1000, penalty=None)
    model.fit(X, y)

    # 10-fold cross-validation
    kf = KFold(n_splits=10, random_state=None)
    acc_cv = cross_val_score(model, X, y, cv=kf).mean()

    # Predictions on full data
    predicted_prob = model.predict_proba(X)
    predicted_class = model.predict(X)
    predicted_prob_max = np.max(predicted_prob, axis=1)

    predictions = []
    for i, row_val in enumerate(df["Row"].values):
        predictions.append(
            PredictionEntry(
                row=int(row_val),
                predicted_probability=round(float(predicted_prob_max[i]), 2),
                prediction=int(predicted_class[i]),
            )
        )

    # 80/20 train-test split metrics
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    split_model = LogisticRegression(max_iter=1000, penalty=None)
    split_model.fit(X_train, y_train)

    y_pred = split_model.predict(X_test)
    rmse = float(np.sqrt(np.mean((y_test - y_pred) ** 2)))
    f1 = float(f1_score(y_test, y_pred, average="macro"))
    precision = float(precision_score(y_test, y_pred, average="macro"))
    recall = float(recall_score(y_test, y_pred, average="macro"))

    # Information criteria (computed on full model)
    y_pred_proba = model.predict_proba(X)[:, 1]
    logloss = log_loss(y, y_pred_proba)
    loglikelihood = -logloss * len(y)
    K = len(model.coef_[0])
    n = len(df)
    likelihood = float(-_deviance(X, y, model) / 2)
    aic = -2 * loglikelihood + 2 * K
    aicc = -2 * loglikelihood + 2 * K + (2 * K * (K + 1) / (n - K - 1))
    bic = aic + K * (np.log(n) - 2)
    brier = float(brier_score_loss(y, y_pred_proba))

    stats = ModelStats(
        model_type=f"Py_{model_type}",
        aic=round(aic, 2),
        aicc=round(aicc, 2),
        bic=round(bic, 2),
        num_parameters=K,
        likelihood=round(likelihood, 2),
        brier_score=round(brier, 2),
        log_loss=round(logloss, 2),
        rmse=round(rmse, 2),
        acc_cv=round(float(acc_cv), 2),
        precision=round(precision, 2),
        recall=round(recall, 2),
        f1=round(f1, 2),
    )

    coefs = np.transpose(model.coef_).round(2)
    coefficients = [
        CoefficientEntry(feature=str(col), coef=float(coefs[i][0]))
        for i, col in enumerate(X.columns)
    ]

    return ModelResult(stats=stats, coefficients=coefficients, predictions=predictions)
