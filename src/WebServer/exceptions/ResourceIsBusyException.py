class ResourceIsBusyException(Exception):

    def __init__(self, path, msg):
        """
        Exception is raised when a path is busy in the API

        """
        self.path = path
        self.msg = f"\"{path}\" {msg}"
        super().__init__(self.msg)
