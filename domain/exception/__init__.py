class EntityNotFoundError(Exception):
    def __init__(self, entity: any, reason: str):
        if hasattr(entity, '__name__'):
            entity = entity.__name__

        super().__init__(f'{entity} not found: {reason}')


class InvalidStateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class WrongFileTypeError(Exception):
    def __init__(self, filename: str, mimetype: str) -> None:
        super().__init__(f'Wrong type {mimetype} for file {filename}')


class MissingFileError(Exception):
    def __init__(self, filename) -> None:
        super().__init__(f'Missing {filename} file')
