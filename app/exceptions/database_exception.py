
class DatabaseException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'Failed to write to the database: {self.message}'