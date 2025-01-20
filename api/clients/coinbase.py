from typing import Dict, Any, Optional, List

from coinbase.rest import RESTClient

DEFAULT_CONNECTION_TIMEOUT = 10


def configure_coinbase(config: Dict[str, Any]) -> 'CoinbaseClient':
    return CoinbaseClient(
        key_file=config['COINBASE_KEY_FILE'],
        connection_timeout=config.get('COINBASE_CONNECTION_TIMEOUT')
    )

class CoinbaseClient:
    def __init__(
        self, key_file: str,
        connection_timeout: Optional[int] = DEFAULT_CONNECTION_TIMEOUT
    ):
        self._client = RESTClient(key_file=key_file, timeout=connection_timeout)

    def get_portfolio_breakdown(self, portfolio_id: str):
        portfolios = self._get_portfolios()['portfolios']
        portfolio = self._find_portfolio(portfolio_id=portfolio_id, portfolios_response=portfolios)
        if not portfolio:
            raise ValueError(f'No portfolio found for {portfolio_id}')
        return self._client.get_portfolio_breakdown(portfolio_uuid=portfolio_id)

    def _get_portfolios(self):
        return self._client.get_portfolios()

    @staticmethod
    def _find_portfolio(portfolio_id: str, portfolios_response: List) -> Optional[Dict]:
        for portfolio in portfolios_response:
            if portfolio['uuid'] == portfolio_id:
                return portfolio
        return None
