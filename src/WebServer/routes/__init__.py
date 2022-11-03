class Page:
    def __init__(self, route: str, name: str, handler, methods: list,) -> None:
        self.route = route
        self.name = name
        self.methods = methods
        self.handler = handler
