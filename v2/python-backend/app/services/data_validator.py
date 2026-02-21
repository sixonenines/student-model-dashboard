import pandas as pd

REQUIRED_COLUMNS = [
    "AnonStudentId",
    "First Attempt",
    "Corrects",
    "Incorrects",
    "Opportunity",
    "Hints",
    "KC (Default)",
]

EXPECTED_DTYPES = {
    "AnonStudentId": ["object"],
    "First Attempt": ["object"],
    "Corrects": ["int64"],
    "Incorrects": ["int64"],
    "Opportunity": ["float64", "int64"],
    "Hints": ["int64"],
    "KC (Default)": ["object"],
}


def validate_dataframe(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
        return errors

    for col, allowed_types in EXPECTED_DTYPES.items():
        if col in df.columns and str(df[col].dtype) not in allowed_types:
            errors.append(
                f"Column '{col}' has dtype '{df[col].dtype}', expected one of {allowed_types}"
            )

    return errors
