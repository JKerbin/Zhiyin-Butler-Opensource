from audio import Audio
from network import Network
from program import ProgramManager
from utils import *

module = 'MAIN'
conf = Config()
sig = Sig(module)
net = Network(conf.config('SERVER_HOST'), conf.config('SERVER_PORT'))
prom = ProgramManager()
user = Audio()
mas = Massage(module)

# 服务模式：普通/增强/本地
server_mode = conf.config('SERVER_MOD')


# 播放提示音
def play_audio(file_name):
    user.play(user.decode(conf.config('AUDIO_DIR') + f'/sys/{file_name}')[0], 'tts_hd')


if __name__ == '__main__':
    """
    这个是主客户端进程，检查用户是否注册，音频设备是否完整
    持续执行录音并上传用户语音工作，接收服务端消息并处理
    """
    try:
        ver = net.verification_client()
        if ver != 'success':
            play_audio('erraudio.wav')
            raise Exception('主进程验证失败')

        play_audio('hello.wav')

        while True:
            voice, voice_len = user.record()
            if voice == 'bad':
                play_audio('nodevice.wav')
                raise Exception('设备不完整')

            response_type, response_content, tts_mode = net.ai_client(
                speech=voice,
                speech_len=voice_len,
                plist=prom.program_list,
                server_mode=server_mode
            )

            if response_type == 'chat':
                user.play(response_content, tts_mode)
            elif response_type == 'error':
                play_audio('erraudio.wav')
            elif response_type == 'func':
                if response_content == 'unknown':
                    play_audio('ukfaudio.wav')
                else:
                    play_audio('funcaudio.wav')
                    prom.start_process(response_content)
            else:
                pass

    except Exception as e:
        mas.info(str(e))
        sig.mainbad()
