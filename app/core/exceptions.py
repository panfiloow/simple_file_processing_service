from fastapi import HTTPException, status

class FileProcessingException(HTTPException):
    def __init__(self, detail: str = "File processing error"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class FileTooLargeException(FileProcessingException):
    def __init__(self, max_size: int):
        super().__init__(
            detail=f"File size exceeds maximum allowed size of {max_size} bytes"
        )

class UnsupportedFileTypeException(FileProcessingException):
    def __init__(self, file_type: str):
        super().__init__(
            detail=f"Unsupported file type: {file_type}"
        )

class FileNotFoundException(HTTPException):
    def __init__(self, file_id: str = None):
        detail = "File not found"
        if file_id:
            detail = f"File with id {file_id} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: str = None):
        detail = "Task not found"
        if task_id:
            detail = f"Task with id {task_id} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

class InsufficientStorageException(HTTPException):
    def __init__(self, available: int, required: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient storage. Available: {available} bytes, required: {required} bytes"
        )

class DuplicateFileException(HTTPException):
    def __init__(self, filename: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File with name '{filename}' already exists"
        )

