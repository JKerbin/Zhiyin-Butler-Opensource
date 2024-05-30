from network import Network
from utils import *

module = 'BOOT'
conf = Config()
sig = Sig(module)
net = Network(conf.config('SERVER_HOST'), conf.config('SERVER_PORT'))
mas = Massage(module)

if __name__ == '__main__':
    """
    用于客户端初始化，检查本机是否注册
    """
    mas.info('客户端初始化验证')
    result = net.verification_client()
    if result == 'success':
        sig.main()
    elif result == 'fail':
        sig.activation()
    else:
        sig.unknown()
