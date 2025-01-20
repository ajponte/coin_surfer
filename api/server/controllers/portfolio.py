from typing import Dict

from clients.coinbase import configure_coinbase


DEFAULT_API_KEY_FILE = "etc/coinbase/api_key/cdp_api_key-ro.json"

def get_portfolio(wallet_type: str, portfolio_id: str) -> Dict:
    if wallet_type not in ['coinbase']:
        return {'message': f'{wallet_type} not currently supported'}
    coinbase = configure_coinbase(config={'COINBASE_KEY_FILE': DEFAULT_API_KEY_FILE})
    portfolios = coinbase.get_portfolio_breakdown(portfolio_id=portfolio_id)
    import pdb; pdb.set_trace()
    return {}
