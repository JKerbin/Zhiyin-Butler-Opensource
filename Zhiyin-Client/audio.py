import base64
import os

import numpy as np
import pyaudio
import comtypes.client

from utils import Massage


class Audio:
    def __init__(self):
        self.__c = 'VOICE'
        # 单通道，采样率16000，hd模式采用率24000，录制最长时间30s，0.5s未采集到声音停止
        self.config = {
            'CHUNK': 1024,
            'FORMAT': pyaudio.paInt16,
            'CHANNELS': 1,
            'RATE_TTS': 16000,
            'RATE_TTS_HD': 24000,
            'RECORD_SECONDS': 30,
            'SILENCE_TIMEOUT': 0.5,
        }
        self.mas = Massage(self.__c)

    def record(self, audio_threshold):
        """
        采集base64音频信息
        :return: base64编码的音频文件, 音频文件大小
        """
        try:
            self.mas.info('采集base64音频信息')
            audio = pyaudio.PyAudio()
            # 打开音频流
            stream = audio.open(format=self.config['FORMAT'],
                                channels=self.config['CHANNELS'],
                                rate=self.config['RATE_TTS'],
                                input=True,
                                frames_per_buffer=self.config['CHUNK'])
            # 录音时间片单位
            unit = self.config['RATE_TTS'] / self.config['CHUNK']
            # 循环直到录到有效内容
            while True:
                frames = []
                silent_frames = 0
                for i in range(0, int(unit * self.config['RECORD_SECONDS'])):
                    data = stream.read(self.config['CHUNK'])
                    frames.append(data)
                    # 检测静音时间
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    if np.max(np.abs(audio_data)) < int(audio_threshold):
                        silent_frames += 1
                    else:
                        silent_frames = 0
                    if silent_frames >= int(unit * self.config['SILENCE_TIMEOUT']):
                        break
                # 无内容录音
                if len(frames) / unit <= self.config['SILENCE_TIMEOUT']:
                    self.mas.warning('未采集到有效的base64信息')
                else:
                    break
            stream.stop_stream()
            stream.close()
            audio.terminate()
            # 返回录音内容和录音文件长度
            speech = base64.b64encode(b''.join(frames)).decode("utf-8")
            speech_len = len(b''.join(frames))
            self.mas.info('音频base64编码完成')
            return speech, speech_len
        except Exception as e:
            self.mas.error(e)
            return 'bad', 0

    def play(self, audio_content, mode):
        """
        播放base64编码的音频数据
        :param audio_content: 音频数据（服务模式为base64编码，本地模式为文本内容）
        :param mode: 通用模式/增强模式
        """
        try:
            if mode == 'tts_local':
                self.mas.info('使用WIN11-TTS-API模拟音频')
                # 初始化 SAPI.SpVoice 对象
                sapi = comtypes.client.CreateObject("SAPI.SpVoice")
                # 将文本转换为语音
                sapi.Speak(audio_content)
            else:
                self.mas.info('模拟base64音频')
                audio_data = base64.b64decode(audio_content)
                audio = pyaudio.PyAudio()
                # 打开音频流
                stream = audio.open(format=self.config['FORMAT'],  # 根据实际情况调整
                                    channels=self.config['CHANNELS'],  # 单声道
                                    rate=self.config['RATE_TTS'] if mode == 'tts' else self.config['RATE_TTS_HD'],
                                    # 采样率
                                    output=True)
                stream.write(audio_data)
                stream.stop_stream()
                stream.close()
                audio.terminate()
            self.mas.info('音频模拟结束')
        except Exception as e:
            self.mas.error(e)

    def decode(self, wav):
        """
        将wav文件解码为base64编码
        :param wav: 文件路径
        :return: base64编码信息, 音频文件大小
        """
        try:
            self.mas.info(f'从{wav}中解码音频为base64编码')
            with open(wav, "rb") as f:
                speech = base64.b64encode(f.read()).decode("utf8")
            speech_len = os.path.getsize(wav)
            return speech, speech_len
        except Exception as e:
            self.mas.error(e)
            return '', 0
