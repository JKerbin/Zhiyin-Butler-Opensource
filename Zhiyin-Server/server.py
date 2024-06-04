from flask import Flask, request, jsonify
from gevent import pywsgi

from brain import Brain
from database import Database
from ts import TextAndSound
from utils import *

version = '0.1.2'  # 当前版本

ai = Brain()  # 主语音ai助手
aai = TextAndSound()  # auxiliary_ai语音识别助手
conf = Config()
db = Database(db_name=conf.config('DB_NAME'), user=conf.config('DB_USER'), pw=conf.config('DB_PASSWORD'))
app = Flask(__name__)


@app.route('/api/ai', methods=['POST'])
def ai_api():
    """
    ai服务
    """
    # 设置opan_ai代理地址
    proxies = {
        'http': conf.config('OPENAI_PROXIES'),
        'https': conf.config('OPENAI_PROXIES'),
    }
    data = request.get_json()
    # user_input：用户输入，ai_output：ai输出
    text = aai.asr(data['speech'], data['speech_len'])
    user_input, ai_output = ai.cortex(text, proxies)
    output_type = 'chat'
    if data['server_mode'] == 'normal':
        # 普通语音模式
        output_content, tts_mode = aai.tts(ai_output)
    elif data['server_mode'] == 'hd':
        # 增强语音模式
        output_content, tts_mode = aai.tts_hd(ai_output, proxies)
    else:
        return {"type": "error"}
    if ai_output == 'activate_func_mode':
        # 目前唯一功能，打开应用23333
        output_content = ai.program_manager(user_input, data['program_list'], proxies)
        output_type = 'func'
    response_data = {
        "type": output_type,
        "content": output_content,
        "mode": tts_mode
    }
    return jsonify(response_data)


@app.route('/api/verification', methods=['POST'])
def verification_api():
    """
    用户登录验证服务
    """
    data = request.get_json()
    result = db.user_verification(data['mac'])
    response_data = {
        "state": result
    }
    return jsonify(response_data)


@app.route('/api/activation', methods=['POST'])
def activation_api():
    """
    邀请码注册服务
    """
    data = request.get_json()
    result = db.user_activation(data['mac'], data['invitation'])
    response_data = {
        "state": result
    }
    return jsonify(response_data)


if __name__ == '__main__':
    service_port = int(conf.config('SERVICE_PORT'))
    mas = Massage('SERVER')
    mas.info(f'服务器版本{version}，在{service_port}端口上运行服务')
    server = pywsgi.WSGIServer(('0.0.0.0', service_port), app)
    server.serve_forever()
