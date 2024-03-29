class InvalidUsageError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"message": self.message}


class ValidationError(InvalidUsageError):
    def __init__(self):
        super().__init__("Invalid data", 400)


class QueryError(InvalidUsageError):
    def __init__(self):
        super().__init__("Invalid query", 400)


class NotLoggedInError(InvalidUsageError):
    def __init__(self):
        super().__init__("Unauthorized", 401)


class InvalidTokenError(InvalidUsageError):
    def __init__(self):
        super().__init__("Invalid token", 401)


class InvalidPageNumber(InvalidUsageError):
    def __init__(self):
        super().__init__("Invalid page number", 400)
