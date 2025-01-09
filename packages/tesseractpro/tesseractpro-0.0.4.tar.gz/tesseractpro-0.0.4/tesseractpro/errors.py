class ApiTokenError(Exception):
    """Raises when the API token is invalid"""
    pass


class AuthenticationTimeoutError(Exception):
    pass
