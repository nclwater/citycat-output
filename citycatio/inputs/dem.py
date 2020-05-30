import rasterio as rio


class Dem:
    def __init__(self, data: rio.MemoryFile):
        assert type(data) == rio.MemoryFile
        self.data = data

    def write(self):
        pass
