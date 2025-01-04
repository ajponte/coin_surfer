from typing import Optional


class LoadDataFameException(Exception):
    def __init__(self, message: str, cause: Optional[Exception]):
        self._msg = message
        self._cause = cause

    @property
    def message(self) -> str:
        return self._msg

    @property
    def cause(self) -> Optional[Exception]:
        return self._cause
