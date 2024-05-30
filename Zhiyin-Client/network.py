import json

import psutil
import requests

from audio import Audio
from utils import *


class Network:
    def __init__(self, host, port):
        def get_all_mac_addresses():
            """
            获取本机mac地址列表
            """
            mac_addresses = []
            macs = psutil.net_if_addrs()
            for _, addr_list in macs.items():
                for addr in addr_list:
                    if addr.family == psutil.AF_LINK:
                        mac_addresses.append(addr.address)
            return mac_addresses

        self.__c = 'NETWORK'
        self.mas = Massage(self.__c)
        try:
            conf = Config()
            self.__audio = Audio()
            self.err_audio = self.__audio.decode(conf.config('AUDIO_DIR') + '/sys/erraudio.wav')[0]
        except Exception as e:
            self.mas.error(e)
        try:
            self.host = host
            self.port = str(port)
            self.__server = f'{self.host}' + ':' + f'{self.port}/api/'
            self.__physical_address = get_all_mac_addresses()
        except Exception as e:
            self.mas.error(e)

    def verification_client(self, api='verification'):
        """
        使用本机mac地址验证服务
        :return: 验证结果，success验证成功，fail验证失败
        """
        try:
            url = self.__server + api
            self.mas.info(f'尝试与{url}建立连接')
            data = {
                "mac": self.__physical_address
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
            if response.status_code == 200:
                self.mas.info(f'来自{url}的有效报文')
                if response.json()['state'] == 'success':
                    self.mas.info('验证成功成功')
                else:
                    self.mas.warning('验证失败，请使用邀请码激活服务')
                return response.json()['state']
            else:
                self.mas.error(f'{url}连接错误，错误码-{response.status_code}')
                return 'fail'
        except requests.Timeout:
            self.mas.error(f'连接超时')
            return 'fail'
        except Exception as e:
            self.mas.error(e)
            return 'fail'

    def activation_client(self, invitation, api='activation'):
        """
        使用邀请码注册zhiyin服务，每个邀请码对应本机MAC地址
        :param invitation: 邀请码
        :param api: 服务器api接口
        :return: 注册状态，success注册成功，exist用户已经注册过，fail注册失败
        """
        try:
            url = self.__server + api
            self.mas.info(f'尝试与{url}建立连接')
            data = {
                "invitation": invitation,
                "mac": self.__physical_address
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
            if response.status_code == 200:
                self.mas.info(f'来自{url}的有效报文')
                if response.json()['state'] == 'success':
                    self.mas.info('邀请码注册成功')
                elif response.json()['state'] == 'exist':
                    self.mas.warning('用户已注册过')
                else:
                    self.mas.warning('注册失败，请检查邀请码是否正确')
                return response.json()['state']
            else:
                self.mas.error(f'{url}连接错误，错误码-{response.status_code}')
                return 'fail'
        except requests.Timeout:
            self.mas.error(f'连接超时')
            return 'fail'
        except Exception as e:
            self.mas.error(e)
            return 'fail'

    def ai_client(self, speech, speech_len, plist, server_mode, api='ai'):
        """
        发送用户语音到服务器，接受服务器返回结果
        :param speech: base64编码的音频信息
        :param speech_len: 音频文件大小
        :param api: 服务器api接口
        :param server_mode: 服务模式（正常模式/增强模式）
        :return:
        -type 返回类型（目前包括'chat', 'func'）
        -content 返回内容
        -mode 返回的音频模式，正常模式16000采样率，增强模式24000采样率
        """
        try:
            url = self.__server + api
            self.mas.info(f'尝试与{url}建立连接')
            data = {
                "speech": speech,
                "speech_len": speech_len,
                "server_mode": server_mode,
                "program_list": plist
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
            if response.status_code == 200:
                self.mas.info(f'来自{url}的有效报文')
                return response.json()['type'], response.json()['content'], response.json()['mode']
            else:
                self.mas.error(f'{url}连接错误，错误码-{response.status_code}')
                return 'error', self.err_audio, 'tts'
        except requests.Timeout:
            self.mas.error(f'连接超时')
            return 'error', self.err_audio, 'tts'
        except Exception as e:
            self.mas.error(e)
            return 'error', self.err_audio, 'tts'
