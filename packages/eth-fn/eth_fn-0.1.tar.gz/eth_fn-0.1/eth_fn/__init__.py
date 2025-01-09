
import eth_utils
import eth_abi

def eth_fn(fn, params):
    h = eth_utils.keccak(fn.encode()).hex()
    types = fn[fn.index('(')+1:fn.index(')')].split(',')
    param_hex = eth_abi.encode([i for i in types if i], params).hex()
    return '0x' + h[:8] + param_hex
