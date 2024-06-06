<h1 align="center">ZHIYIN_BUTLER客户端内核组件</h1>

<p align="center">基于python3 + pyinstaller开发</p>

## 说明

本项目为Zhiyin-Butler客户端内核源代码，版本为beta0.1.0

项目目录：
<pre>
项目根目录/
├── README.md
├── requirements.txt
├── config.env                      # 配置文件（用于开发模式）
├── config.py                       # 配置文件（用于发行模式）
├── log                             # 日志文件
├── audio/                          # 音频文件
│   ├── sys/                        # 内置语音
│   │   ├── erraudio.wav
│   │   ├── funcaudio.wav
│   │   ├── hello.wav
│   │   ├── nodevice.wav
│   │   └── ukfaudio.wav
├── programs/
│   ├── lnk/
│   │   └── ...                     # 程序快捷方式
│   └── plist                       # 程序表
├── build/
│   └── reports/
│       └── tests/
│           └── testReport.html
├── client_boot.py                  # 客户端初始化内核
├── client_activation.py            # 客户端激活内核
├── client_main.py                  # 客户端主内核
├── audio.py                        # 音频处理相关组件
├── network.py                      # 网络连接相关组件
├── program.py                      # 程序管理相关组件
└── utils.py                        # 通用组件
</pre>

## 项目部署

### 安装环境
```bash
$ pip install -r requirements.txt
```

### 配置环境变量

```bash
# 打开config.env
SYS_LNK_DIR="C:/ProgramData/Microsoft/Windows/Start Menu/Programs" # Windows开始菜单目录，默认不用更改
PROGRAM_DIR="programs" # 程序控制相关信息保存目录，不需要更改
AUDIO_DIR="audio" # 程序音频信息保存目录，不需要更改
LOG_PATH="log" # 日志信息保存目录，不需要更改
SERVER_HOST="http://127.0.0.1" # 服务地址，使用远程服务器是配置成服务器的公网ip
SERVER_PORT="1228" # 服务端口，默认1228
SERVER_MOD="normal" # 服务模式（tts模式），mormal使用百度tts接口，hd模式使用openai的tts接口

```

### 运行项目

```bash
$ python client_boot.py
$ python client_activation.py [激活码]
$ python client_main.py
```

### 打包内核

```bash
$ pyinstaller -F client_boot.py
$ pyinstaller -F client_activation.py
$ pyinstaller -F client_main.py
```
