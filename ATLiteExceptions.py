class JSONMissingError(Exception):
    pass

class InvalidSKOError(Exception):
    pass

class PermissionDeniedError(Exception):
    pass

class JSONPropertyMissingError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class UserNotLoggedInError(Exception):
    pass

class InvalidUserError(Exception):
    pass

class OtherError(Exception):
    pass