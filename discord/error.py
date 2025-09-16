METHOD_SUCCESS_CODES = {
    "GET": (200),
    "POST": (200, 201),
    "PATCH": (200, 201),
    "DELETE": (200, 204)
}

class DiscordError(Exception):
    """Represents a Discord API error."""
    def __init__(self, status: int, data: dict):
        """Initialize the error with Discord's response.
            Extracts reason, code, and walks the nested errors.

        Args:
            data (dict): Discord's error JSON
        """
        self.data = data
        """Raw error data."""

        self.reason = data.get('message', 'Unknown Error')
        """Discord-generated reason for error."""

        self.code = data.get('code', '???')
        """Discord-generated code of error."""

        self.error_data = data.get('errors', {})
        """Error-specific data."""

        self.details = self.walk(self.error_data)
        """Error details."""

        self.fatal = status in (401, 403)
        """If this error is considered fatal."""

        errors = [f"→ {path}: {reason}" for path, reason in self.details]
        full_message = f"{self.reason} ({self.code})"
        if errors:
            full_message += '\n' + '\n'.join(errors)

        super().__init__(full_message)

    def walk(self, node: dict, path=None):
        """Recursively traverses errors field to flatten nested validation errors into (path, message).

        Args:
            node (dict): current error level
            path (tuple[str, str], optional): path to this error level

        Returns:
            (list): list of errors
        """
        if path is None:
            path = []
        result = []

        if isinstance(node, dict):
            for key, value in node.items():
                if key == '_errors' and isinstance(value, list):
                    msg = value[0].get('message', 'Unknown error')
                    result.append(('.'.join(path), msg))
                elif isinstance(value, dict):
                    result.extend(self.walk(value, path + [key]))
        return result
