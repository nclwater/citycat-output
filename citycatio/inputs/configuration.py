class Configuration:
    def __init__(self, data: dict):
        assert isinstance(data, dict)
        self.data = data

    def write(self):
        pass
