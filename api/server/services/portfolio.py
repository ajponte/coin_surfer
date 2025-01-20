import abc
import enum
from typing import Any, Dict, Optional

from clients.coinbase import configure_coinbase, CoinbaseClient

DEFAULT_API_KEY_FILE = "etc/coinbase/api_key/cdp_api_key-ro.json"

class PortfolioName(str, enum.Enum):
    def __new__(cls, name: str):
        return cls(name)

    COINBASE = 'coinbase'
    META_MASK = 'metamask'

class Portfolio(abc.ABC):
    @abc.abstractmethod
    def portfolio_connect(self) -> 'Portfolio':
        ...

class Coinbase(Portfolio):
    def __init__(self):
        self._client: Optional[CoinbaseClient] = None

    def portfolio_connect(self) -> 'Coinbase':
        if self._client is not None:
            return self
        self._client = configure_coinbase(
            config={'COINBASE_KEY_FILE': DEFAULT_API_KEY_FILE}
        )
        return self

    def get_accounts(self):
        if not self._client:
            raise ValueError('Coinbase SDK Client not initialized.')
        return self._client.get_accounts()
