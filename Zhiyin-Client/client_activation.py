from network import Network
from utils import *

module = 'ACTIVATION'
conf = Config()
sig = Sig(module)
net = Network(conf.config('SERVER_HOST'), conf.config('SERVER_PORT'))
mas = Massage(module)

if __name__ == '__main__':
    """
    用于注册激活客户端，运行参数有一个，为用户激活码
    例如：python client_activation.py e4bfc14e-7618-42e3-9241-ed3a55c49485
    """
    mas.info('客户端产品激活')
    if len(sys.argv) != 2:
        mas.error('调用错误')
    else:
        invitation = sys.argv[1]
        result = net.activation_client(invitation)
        if result == 'success':
            sig.actsucc()
        elif result == 'exist':
            sig.actsucc()
        elif result == 'fail':
            sig.actfail()
        else:
            sig.unknown()
