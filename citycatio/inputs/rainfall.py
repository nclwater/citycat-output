import pandas as pd
import os


class Rainfall:
    def __init__(self, data: pd.DataFrame):
        assert type(data) == pd.DataFrame
        assert len(data) > 0, 'Rainfall DataFrame is empty'
        self.data = data

    def write(self, path):
        with open(os.path.join(path, 'Rainfall_Data_1.txt'), 'w') as f:
            f.write('* * *\n')
            f.write('* * * rainfall * * *\n')
            f.write('* * *\n')
            f.write('{}\n'.format(len(self.data)))
            f.write('* * *\n')
            self.data.to_csv(f, sep=' ', header=False)
