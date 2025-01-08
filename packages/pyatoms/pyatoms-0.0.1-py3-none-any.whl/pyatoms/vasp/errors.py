class XDATCARError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class OUTCARError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MaxTimeExceededError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class VASPError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
