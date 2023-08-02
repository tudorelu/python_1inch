import json
import requests
from decimal import Decimal

class OneInchExchange:

    base_url = 'https://api.1inch.io'

    chains = dict(
        ethereum = '1',
        binance = '56',
        fantom = "250",
        avalanche = '43114',
        polygon = '137',
        arbitrum = '42161',
        optimism = '10'
    )

    versions = dict(
        # v2 = "v2.0",
        v2_1 = "v2.1"
    )

    endpoints = dict(
        swap = "swap",
        quote = "quote",
        tokens = "tokens",
        protocols = "protocols",
        protocols_images = "protocols/images",
        approve_spender = "approve/spender",
        approve_calldata = "approve/calldata"
    )

    tokens = dict()
    tokens_by_address = dict()
    protocols = []
    protocols_images = []

    def __init__(self, address, chain='ethereum', version="v5.2"):
        self.address = address
        self.version = version
        self.chain_id = self.chains[chain]
        self.chain = chain
        self.get_tokens()
        # self.get_protocols()
        # self.get_protocols_images()


    def _get(self, url, params=None, headers=None):
        """ Implements a get request """
        try:
            response = requests.get(url, params=params, headers=headers)
            payload = json.loads(response.text)
            data = payload
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError when doing a GET request from {}".format(url))
            data = None
        return data


    def health_check(self):
        url = '{}/56/{}/healthcheck'.format(
            self.base_url, self.chain_id)
        response = requests.get(url)
        result = json.loads(response.text)
        if not result.__contains__('status'):
            return result
        return result['status']

    def get_tokens(self):
        if not self.tokens:
            return self.tokens
        else:
            return self.fetch_tokens()
    
    def fetch_tokens(self):
        url = '{}/{}/{}/tokens'.format(
            self.base_url, self.version, self.chain_id)
        result = self._get(url)
        if not result.__contains__('tokens'):
            return result
        for key in result['tokens']:
            token = result['tokens'][key]
            self.tokens_by_address[key] = token
            self.tokens[token['symbol']] = token
        return self.tokens

    def get_protocols(self):
        url = '{}/{}/{}/protocols'.format(
            self.base_url, self.version, self.chain_id)
        result = self._get(url)
        if not result.__contains__('protocols'):
            return result
        self.protocols = result
        return self.protocols


    def get_protocols_images(self):
        url = '{}/{}/{}/protocols/images'.format(
            self.base_url, self.version, self.chain_id)
        result = self._get(url)
        if not result.__contains__('protocols'):
            return result
        self.protocols_images = result
        return self.protocols_images


    def get_quote(self, from_token_symbol:str, to_token_symbol:str, amount:int):
        url = '{}/{}/{}/quote'.format(
            self.base_url, self.version, self.chain_id)
        url = url + '?fromTokenAddress={}&toTokenAddress={}&amount={}'.format(
            self.tokens[from_token_symbol]['address'], 
            self.tokens[to_token_symbol]['address'], 
            format(Decimal(10**self.tokens[from_token_symbol]['decimals'] \
                * amount).quantize(Decimal('1.')), 'n'))
        result = self._get(url)
        return result


    def do_swap(self, from_token_symbol:str, to_token_symbol:str, 
        amount:int, from_address:str, slippage:int):
        url = '{}/{}/{}/quote'.format(
            self.base_url, self.version, self.chain_id)
        url = url + "?fromTokenAddress={}&toTokenAddress={}&amount={}".format(
            self.tokens[from_token_symbol]['address'], 
            self.tokens[to_token_symbol]['address'], 
            amount)
        url = url + '&fromAddress={}&slippage={}'.format(
            from_address, slippage)
        result = self._get(url)
        return result

    def convert_amount_to_decimal(self, token_symbol, amount):
        decimal = self.tokens[token_symbol]['decimals']
        return Decimal(amount) / Decimal(10**decimal)