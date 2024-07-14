from network import Network
from utils import *

module = 'TEXT'
conf = Config()
sig = Sig(module)
net = Network(conf.config('SERVER_HOST'), conf.config('SERVER_PORT'))
mas = Massage(module)

if __name__ == '__main__':
    """
    这个是文本模式客户端进程，检查用户是否注册，调用并上传用户输入，返回服务器ai输出
    """
    try:
        if len(sys.argv) != 2:
            raise Exception('调用错误')
        ver = net.verification_client()
        if ver != 'success':
            raise Exception('主进程验证失败')
        # 打印ai输出内容
        print("ai输出：" + net.text_client(sys.argv[1]))

    except Exception as e:
        mas.error(str(e))
        sig.mainbad()
