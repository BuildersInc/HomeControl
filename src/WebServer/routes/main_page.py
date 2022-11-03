

class MainPage:
    def __init__(self, route: str, name: str, methods: list,) -> None:
        self.route = route
        self.name = name
        self.methods = methods
        self.handler = self.action

    @staticmethod
    def action():
        return "Hello"
