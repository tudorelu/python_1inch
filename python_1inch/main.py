import json
import requests
from decimal import Decimal
import aiohttp

class OneInchExchange:

    base_url = 'https://api.1inch.exchange'

    chains = dict(
        ethereum = '1',
        binance = '56',
        polygon = '137'
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

    def __init__(self, address, version = 'v4.0', chain='ethereum'):
        self.address = address
        self.version = version
        self.chain_id = self.chains[chain]
        self.chain = chain
        # self.get_tokens()
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

    def _get_asynch(self, session, url, params=None, headers=None):
        """ Implements a get request """
        try:
            response = await session.get(url, params=params, headers=headers)
            payload = await response.json()
            data = payload
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError when doing a GET request from {}".format(url))
            data = None
        return data


    def health_check(self):
        url = '{}/{}/{}/healthcheck'.format(
            self.base_url, self.version, self.chain_id)
        response = requests.get(url)
        result = json.loads(response.text)
        if not result.__contains__('status'):
            return result
        return result['status']


    def get_tokens(self):
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


    def get_quote(self, from_token_symbol:str, to_token_symbol:str, amount:float):
        url = '{}/{}/{}/quote'.format(
            self.base_url, self.version, self.chain_id)
        url = url + '?fromTokenAddress={}&toTokenAddress={}&amount={}'.format(
            self.tokens[from_token_symbol]['address'], 
            self.tokens[to_token_symbol]['address'], 
            format(Decimal(10**self.tokens[from_token_symbol]['decimals'] \
                * amount).quantize(Decimal('1.')), 'n'))
        result = self._get(url)
        return result

    def get_quote_asynch(self, session, from_token_symbol:str, to_token_symbol:str, amount:float):
        url = '{}/{}/{}/quote'.format(
            self.base_url, self.version, self.chain_id)
        url = url + '?fromTokenAddress={}&toTokenAddress={}&amount={}'.format(
            self.tokens[from_token_symbol]['address'],
            self.tokens[to_token_symbol]['address'],
            format(Decimal(10**self.tokens[from_token_symbol]['decimals'] \
                * amount).quantize(Decimal('1.')), 'n'))
        result = self._get_asynch(session, url)
        return result


    def do_swap(self, from_token_symbol:str, to_token_symbol:str, 
        amount:float, slippage:int):
        url = '{}/{}/{}/swap'.format(
            self.base_url, self.version, self.chain_id)
        url = url + "?fromTokenAddress={}&toTokenAddress={}&amount={}".format(
            self.tokens[from_token_symbol]['address'],
            self.tokens[to_token_symbol]['address'],
            format(Decimal(10 ** self.tokens[from_token_symbol]['decimals'] \
                           * amount).quantize(Decimal('1.')), 'n'))
        url = url + '&fromAddress={}&slippage={}'.format(
            self.address, slippage)
        result = self._get(url)
        return result

    def do_swap_asynch(self, session, from_token_symbol:str, to_token_symbol:str,
        amount:float, slippage:int):
        url = '{}/{}/{}/swap'.format(
            self.base_url, self.version, self.chain_id)
        url = url + "?fromTokenAddress={}&toTokenAddress={}&amount={}".format(
            self.tokens[from_token_symbol]['address'],
            self.tokens[to_token_symbol]['address'],
            format(Decimal(10 ** self.tokens[from_token_symbol]['decimals'] \
                           * amount).quantize(Decimal('1.')), 'n'))
        url = url + '&fromAddress={}&slippage={}'.format(
            self.address, slippage)
        result = self._get_asynch(session, url)
        return result

    def convert_amount_to_decimal(self, token_symbol, amount):
        decimal = self.tokens[token_symbol]['decimals']
        return Decimal(amount) / Decimal(10**decimal)