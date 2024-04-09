"""
    General Database Exception to hide internal database errors
"""
from fastapi import HTTPException, status


class CustomDatabaseException(Exception):
    """Custom database exception to handle sentry error logging"""

    def __init__(self, ex: Exception):
        super().__init__("Database Error")
        self.ex = ex
        # log detailed exception to sentry at this position
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error"
        )
