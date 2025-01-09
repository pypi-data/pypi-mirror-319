from .basetool import BaseTool


class TurningPoint(BaseTool):
    def __init__(self, data):
        super().__init__(data)

    def get_number(self) -> int:
        return self.get_option('number')
