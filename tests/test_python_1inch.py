from python_1inch import OneInchExchange

def test_eth_init():
    eth = OneInchExchange('address')
    assert eth.address == 'address'
    assert eth.chain_id == '1'
    assert eth.chain == 'ethereum'


def test_bsc_init():
    bsc = OneInchExchange('address', chain='binance')
    assert bsc.address == 'address'
    assert bsc.chain_id == '56'
    assert bsc.chain == 'binance'
