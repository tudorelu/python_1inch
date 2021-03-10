# python_1inch
A python wrapper around the 1INCH exchange API. https://1inch.exchange

## API documentation:
https://docs.1inch.exchange/api/

## Installation

```sh
git clone https://github.com/tudorelu/python_1inch
```

## Usage Example
```py
from python_1inch import OneInchExchange

eth_exchange = OneInchExchange('Some_eth_address')
bsc_exchange = OneInchExchange('Some_eth_address', chain='binance')

eth_exchange.health_check()
# 'OK'

# fetches the tokens from the API
eth_exchange.get_tokens()

# are then stored in memory
eth_exchange.tokens
# {
#  '1INCH': {'address': '0x111111111117dc0aa78b770fa6a738034120c302',
#            'decimals': 18,
#            'logoURI': 'https://tokens.1inch.exchange/0x111111111117dc0aa78b770fa6a738034120c302.png',
#            'name': '1INCH Token',
#            'symbol': '1INCH'},
#   'ETH': {'address': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
#          'decimals': 18,
#          'logoURI': 'https://tokens.1inch.exchange/0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.png',
#          'name': 'Ethereum',
#          'symbol': 'ETH'},
#   ......
# }

eth_exchange.tokens_by_address
# {
#  '0x111111111117dc0aa78b770fa6a738034120c302': 
#           {'address': '0x111111111117dc0aa78b770fa6a738034120c302',
#            'decimals': 18,
#            'logoURI': 'https://tokens.1inch.exchange/0x111111111117dc0aa78b770fa6a738034120c302.png',
#            'name': '1INCH Token',
#            'symbol': '1INCH'},
#   ......
# }


# fetches the protocols (dexes)
eth_exchange.get_protocols()

# stored in memory
eth_exchange.protocols
# {'protocols': ['WETH',
#                'UNISWAP_V2',
#                 ......
#               ]}


# fetches the protocols images
eth_exchange.get_protocols_images()

# stored in memory
eth_exchange.protocols_images
# {'protocols': [{'id': 'WETH',
#                 'img': 'https://api.1inch.exchange/WETH.png',
#                 'title': 'WETH'},
#                {'id': 'MOONISWAP',
#                 'img': 'https://api.1inch.exchange/mooniswap.png',
#                 'title': 'Mooniswap'},
#               ......
#               ]
# }

# gets the exchange rate of two tokens 
eth_exchange.get_quote(from_token_symbol='ETH', to_token_symbol='USDT', amount=1)
# {'estimatedGas': 313182,
#  'fromToken': {'address': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
#                'decimals': 18,
#                'logoURI': 'https://tokens.1inch.exchange/0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.png',
#                'name': 'Ethereum',
#                'symbol': 'ETH'},
#  'fromTokenAmount': '1000000000000000000',
#  'protocols': [[[{'fromTokenAddress': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
#                   'name': 'WETH',
#                   'part': 100,
#                   'toTokenAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'}],
#                 [{'fromTokenAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
#                   'name': 'SUSHI',
#                   'part': 100,
#                   'toTokenAddress': '0xdac17f958d2ee523a2206206994597c13d831ec7'}]]],
#  'toToken': {'address': '0xdac17f958d2ee523a2206206994597c13d831ec7',
#              'decimals': 6,
#              'logoURI': 'https://tokens.1inch.exchange/0xdac17f958d2ee523a2206206994597c13d831ec7.png',
#              'name': 'Tether USD',
#              'symbol': 'USDT'},
#  'toTokenAmount': '1799077012'}


# converts wei to eth for the specified token
eth_exchange.convert_amount_to_decimal('ETH', 1000000000000000000)
# Decimal('1')

eth_exchange.convert_amount_to_decimal('USDT', 80000000)
# Decimal('80')

# UNSUPPORTED YET
# eth_exchange.do_swap()

```