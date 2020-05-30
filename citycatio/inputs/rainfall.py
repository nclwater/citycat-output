import pandas as pd


class Rainfall:
    def __init__(self, data: pd.DataFrame):
        assert type(data) == pd.DataFrame
        assert len(data) > 0, 'Rainfall DataFrame is empty'
        self.data = data

    def write(rainfall: pd.DataFrame):
        pass
