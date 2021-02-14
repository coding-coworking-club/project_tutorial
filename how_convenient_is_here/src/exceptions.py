class APIKeyError(Exception):
    """Raised when user does not fill in API Key"""

    def __str__(self):
        return self.__class__.__name__
    pass
