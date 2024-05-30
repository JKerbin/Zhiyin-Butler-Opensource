import base64
import json
import urllib
import urllib.parse

import requests

from utils import *


class TextAndSound:
    def __init__(self):
        self.__c = 'TS'
        self.conf = Config()
        self.mas = Massage(self.__c)
        self.__baidu_api_key = self.conf.config('BAIDU_API_KEY')
        self.__baidu_secret_key = self.conf.config('BAIDU_SECRET_KEY')
        self.__baidu_access_token = self.__get_access_token()
        self.__openai_api_key = self.conf.config('OPENAI_API_KEY')
        self.mas.info('语音助手初始化')

    def __get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.__baidu_api_key,
                  "client_secret": self.__baidu_secret_key}
        return str(requests.post(url, params=params).json().get("access_token"))

    @staticmethod
    def __double_url_encode(text):
        first_encoded = urllib.parse.quote(text, safe='')
        second_encoded = urllib.parse.quote(first_encoded, safe='')
        return second_encoded

    def tts(self, text):
        """
        使用百度tts接口生成语音
        :param text: 文本内容
        :return: base64编码的音频，采样率16000
        """
        try:
            url = "https://tsn.baidu.com/text2audio"
            payload = 'tex=' + self.__double_url_encode(text) + \
                      '&tok=' + self.__baidu_access_token + \
                      '&cuid=vb6Dpmim1aAxgA1MmFwM67BL0t4YM99u&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=0&aue=6'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            self.mas.info('base64编码音频生成')
            return base64.b64encode(response.content).decode('utf-8'), 'tts'
        except Exception as e:
            self.mas.error(e)

    def tts_hd(self, text, proxies):
        """
        使用openai的tts接口生成语音
        :param text: 文本内容
        :param proxies: 服务代理
        :return: base64编码的音频，采样率24000
        """
        try:
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.__openai_api_key}"
            }
            payload = {
                "model": "tts-1",
                "voice": "alloy",
                "input": text,
                "response_format": "wav"
            }
            response = requests.request("POST", url, headers=headers, json=payload, proxies=proxies)
            self.mas.info('base64编码音频生成')
            return base64.b64encode(response.content).decode('utf-8'), 'tts_hd'
        except Exception as e:
            self.mas.error(e)

    def asr(self, speech, speech_len):
        """
        使用百度asr语音转文字
        :param speech: base64编码的音频信息
        :param speech_len: 音频文件大小
        """
        try:
            url = "https://vop.baidu.com/server_api"
            payload = json.dumps({
                "format": "wav",
                "rate": 16000,
                "channel": 1,
                "cuid": "cwiDXQXyp4gTDBizmTHi9UWsdmkuFK3H",
                "token": self.__baidu_access_token,
                "speech": speech,
                "len": speech_len
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)['result'][0]
            self.mas.info("音频内容提取完成")
            return result
        except Exception as e:
            self.mas.error(e)
