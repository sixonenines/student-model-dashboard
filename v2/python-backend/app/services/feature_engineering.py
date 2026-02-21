import pandas as pd


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.loc[df["First Attempt"] == "incorrect", "First Attempt"] = 0
    df.loc[df["First Attempt"] == "hint", "First Attempt"] = 0
    df.loc[df["First Attempt"] == "correct", "First Attempt"] = 1
    df = df[(df["First Attempt"] == 0) | (df["First Attempt"] == 1)]

    df = df.dropna()
    df.insert(loc=len(df.columns), column="Outcome", value=df["First Attempt"])

    df.rename(
        columns={
            "KC (Default)": "KCModel",
            "Opportunity": "OpportunityModel",
            "Corrects": "CorrectModel",
            "Incorrects": "IncorrectModel",
            "Hints": "TellsModel",
        },
        inplace=True,
    )

    if "Row" not in df.columns:
        df["Row"] = df.index

    return df
