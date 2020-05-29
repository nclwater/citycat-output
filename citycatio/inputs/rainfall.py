import pandas as pd


def validate(rainfall: pd.DataFrame):
    assert type(rainfall) == pd.DataFrame
    assert len(rainfall) > 0, 'Rainfall DataFrame is empty'
    return rainfall


def write(rainfall: pd.DataFrame):
    pass
