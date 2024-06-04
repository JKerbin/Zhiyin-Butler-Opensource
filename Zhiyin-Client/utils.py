import os
import datetime
import sys
import threading
import time
from config import config
from functools import wraps
from dotenv import load_dotenv


class Config:
    def __init__(self):
        self.__c = 'UTILS'
        self.env_path = 'config.env'
        self.mas = Massage(self.__c)
        self.sig = Sig(self.__c)

    def config(self, env):
        """
        获取环境变量
        :param env: 环境变量名
        :return: 环境变量值
        """
        if not os.path.exists(self.env_path):
            self.sig.envmissing()
            return ''
        try:
            load_dotenv(dotenv_path=self.env_path, verbose=True)
            dev = os.getenv('DEV')
        except Exception as e:
            self.mas.error(e)
            return ''

        if dev == 'dev':
            # TODO: 从config.env中获取环境变量(开源版)
            try:
                load_dotenv(dotenv_path=self.env_path, verbose=True)
                return os.getenv(env)
            except Exception as e:
                self.mas.error(e)
                return ''
        elif dev == 'release':
            # TODO: 从config.py中获取环境变量(发行版)
            try:
                return config[env]
            except Exception as e:
                self.mas.error(e)
                return ''


class Sig:
    def __init__(self, module):
        self.module = module
        self.mas = Massage(self.module)

    def unknown(self):
        self.mas.info('信号量--未知信号')
        print('signal_unknown')

    def envmissing(self):
        self.mas.error('信号量--配置文件缺失')
        print('signal_envmissing')

    def main(self):
        self.mas.info('信号量--启动主进程')
        print('signal_main')

    def mainbad(self):
        self.mas.info('信号量--主进程意外退出')
        print('signal_mainbad')

    def activation(self):
        self.mas.info('信号量--需要激活')
        print('signal_activation')

    def actsucc(self):
        self.mas.info('信号量--激活成功')
        print('signal_actsucc')

    def actfail(self):
        self.mas.info('信号量--激活失败')
        print('signal_actfail')


class Massage:
    """
    打印信息
    """

    def __init__(self, module):
        self.module = module

    def write_log(self, log):
        try:
            conf = Config()
            log_path = conf.config('LOG_PATH')
            with open(log_path, 'a') as file:
                file.write(log + '\n')
        except Exception as e:
            self.error(e)

    def info(self, massage):
        print(f"\033[32mFROM_{self.module}_INFO: {massage}\033[0m")
        self.write_log(str(datetime.datetime.now()) + f": FROM_{self.module}_INFO: {massage}")

    def warning(self, massage):
        print(f"\033[33mFROM_{self.module}_WARNING: {massage}\033[0m")
        self.write_log(str(datetime.datetime.now()) + f": FROM_{self.module}_WARNING: {massage}")

    def error(self, massage):
        print(f"\033[31mFROM_{self.module}_ERROR: {massage}\033[0m")
        self.write_log(str(datetime.datetime.now()) + f": FROM_{self.module}_ERROR: {massage}")


class Loading:
    @staticmethod
    def __loading_bar(func):
        @wraps(func)
        def wrapper(*args, module='', desc='', colour='', **kwargs):
            mas = Massage('UTILS')
            mas.write_log(str(datetime.datetime.now()) + f": FROM_{module}_INFO: {desc}")
            # 进度条样式
            length = 20
            fill_char = '█'
            empty_char = '-'

            total = len(args[0])
            colour_code = {
                'green': '\033[32m',
                'yellow': '\033[33m',
                'red': '\033[31m'
            }.get(colour, '')  # 根据颜色选择对应的 ANSI 转义码

            for i, item in enumerate(func(*args, **kwargs)):
                percent = (i + 1) / total
                filled_length = int(length * percent)
                bar = fill_char * filled_length + empty_char * (length - filled_length)

                # 打印进度条
                sys.stdout.write('\r')
                sys.stdout.write(f'{colour_code}FROM_{module}_INFO: {desc} |{bar}| {percent: .1%}\033[0m')
                sys.stdout.flush()
                yield item

            sys.stdout.write('\n')
            sys.stdout.flush()

        return wrapper

    @staticmethod
    def __waiting_bar(func):
        @wraps(func)
        def wrapper(*args, module='', desc='', colour='', **kwargs):
            # 旋转光标
            def spinning_cursor():
                while True:
                    for cursor in '|/-\\':
                        yield cursor

            mas = Massage('UTILS')
            mas.write_log(str(datetime.datetime.now()) + f": FROM_{module}_INFO: {desc}")
            colour_code = {
                'green': '\033[32m',
                'yellow': '\033[33m',
                'red': '\033[31m'
            }.get(colour, '')  # 根据颜色选择对应的 ANSI 转义码

            spinner = spinning_cursor()
            t = threading.Thread(target=func, args=args, kwargs=kwargs)
            t.start()
            sys.stdout.write(f'{colour_code}FROM_{module}_INFO: {desc}\033[0m')
            while t.is_alive():
                sys.stdout.write(f'{colour_code}{next(spinner)}\033[0m')
                sys.stdout.flush()
                time.sleep(0.3)
                sys.stdout.write('\b')
            sys.stdout.write('\n')
            t.join()

        return wrapper

    # 进度条
    @staticmethod
    @__loading_bar
    def loba(data, module='', desc='', colour=''):
        """
        显示进度条（用法类似tqdm，colour可以自定义打印颜色）
        :param data: 待遍历的数据
        :param module: 消息来源
        :param desc: 进度条说明
        :param colour: 自定义颜色（green绿、yellow黄、red红，默认白色）
        :return:
        """
        for item in data:
            yield item

    # 等待条
    @staticmethod
    @__waiting_bar
    def waba(func, module='', desc='', colour='', *args, **kwargs):
        """
        显示等待条（在执行函数时显示）
        :param func: 待执行的函数
        :param module: 消息来源
        :param desc: 等待条说明
        :param colour: 自定义颜色（green绿、yellow黄、red红，默认白色）
        :param args: 待执行函数参数
        :param kwargs: 待执行函数可变关键字
        :return:
        """
        func(*args, **kwargs)
