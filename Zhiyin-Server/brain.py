import requests

from utils import Config, Massage


class Brain:
    def __init__(self):
        self.__c = 'BRAIN'
        self.conf = Config()
        self.mas = Massage(self.__c)
        self.__openai_api_key = self.conf.config('OPENAI_API_KEY')
        self.base_url = 'https://api.openai.com/v1/chat/completions'

    def program_manager(self, user_input, plist, proxies):
        """
        古希腊掌管控制软件的神
        :param: user_input: 用户输入
        :param: proxies: openai代理
        :param: plist: 用户软件列表
        :return: 选中的程序名称
        """
        try:
            program_list = '/'.join(plist)
            system_message = {
                "role": "system",
                "content": "你是一个软件管家，下面我给你软件名称列表，名称之间用'/'分隔；\n" +
                           program_list +
                           "根据用户的话，返回你觉得对应的软件名称，不要说任何多余的内容，如果你觉得没有对应的软件，返回unknown\n"
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.__openai_api_key
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [system_message, {"role": "user", "content": user_input}],
                "temperature": 0.7
            }
            response = requests.post(self.base_url, headers=headers, json=payload, proxies=proxies)
            response_data = response.json()
            ai_output = response_data['choices'][0]['message']['content']
            return ai_output
        except Exception as e:
            self.mas.error(e)

    def cortex(self, user_input, proxies):
        """
        大脑皮层：负责简单对话和执行功能
        :param: user_input: 用户输入
        :param: proxies: openai代理
        :return:
        - 用户输入
        - ai输出
        """
        try:
            # 系统消息
            system_message = {
                "role": "system",
                "content": "你是一个AI管家，你的名字叫‘智音’；\n"
                           "如果你觉得用户是在和你聊天，你正常和他聊；\n"
                           "如果你觉得用户在让你执行电脑功能，返回‘activate_func_mode’，不要说多余的话。"
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.__openai_api_key
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [system_message, {"role": "user", "content": user_input}],
                "temperature": 0.7
            }
            response = requests.post(self.base_url, headers=headers, json=payload, proxies=proxies)
            response_data = response.json()
            ai_output = response_data['choices'][0]['message']['content']
            return user_input, ai_output
        except Exception as e:
            self.mas.error(e)
