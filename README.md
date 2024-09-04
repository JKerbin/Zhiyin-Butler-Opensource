<h1 align="center">ZHIYIN_BUTLER语音助手</h1>

<p align="center">基于Electron + python开发的Windows桌面应用（客户端 + 服务端）</p>

<p align="center">
<img src="https://img.shields.io/badge/electron-28.2.0-blue" alt="electron-version">
<img src="https://img.shields.io/badge/electron vite-2.0.0-blue" alt="electron-vite-version" />
<img src="https://img.shields.io/badge/electron builder-24.9.1-blue" alt="electron-builder-version" />
<img src="https://img.shields.io/badge/vite-5.0.12-blue" alt="vite-version" />
<img src="https://img.shields.io/badge/vue-3.4.15-blue" alt="vue-version" />
<img src="https://img.shields.io/badge/typescript-5.3.3-blue" alt="typescript-version" />
<br/>
<img src="https://img.shields.io/badge/python-3.12.3-green" alt="python-version" />
<img src="https://img.shields.io/badge/mysql-8.3.0-green" alt="mysql-version" />
<img src="https://img.shields.io/badge/flask-3.0.2-green" alt="flask-version" />
</p>

<img src="logo.png">

## 说明

智音语音助手（Zhiyin_Butler）旨在开发一款通用型智能电脑管家。与市面上常见的集成化语音助手（如小米的“小爱同学”或微软的“Copilot”）相比，智音语音助手不依赖特定硬件，支持在所有Windows 10/11系统上安装和部署。

项目的所有内容遵循[Apache License 2.0开源协议](https://github.com/JKerbin/Zhiyin-Butler-Opensource/blob/main/LICENSE)，作为通用型电脑管家系统示例供开发者参考学习。

代码版本：客户端beta0.3.0，服务端beta0.3.0，主要功能包括：

- 随心聊天
- 启动程序
- 文本模式
- 自定设置
  - 语音模式选择
  - 收音阈值调整
 
[下载测试版beta 0.3.0安装包](https://github.com/JKerbin/Zhiyin-Butler-Opensource/releases/tag/Installer)

播放演示视频请解除静音：

[演示视频](https://github.com/JKerbin/Zhiyin-Butler-Opensource/assets/81380030/84931fa2-0194-4da9-b404-610caf5eac15)

0.3.0新功能————文本模式演示：

[演示视频](https://github.com/user-attachments/assets/7260faf7-2c92-42f1-b710-7d0ac05493de)

更多功能正在开发中……

## 开发相关

开源语音助手智音Butler桌面应用采用node.js(Electron+Vite+Vue3)开发实现

智音Butler客户端内核程序使用python实现，客户端内核与图形化界面分离，可独立运行

智音Butler服务器使用flask框架搭建，调用ChatGPT-3.5-turbo和Baidu-tts-asr服务实现功能

了解项目开源代码，请查看
- [智音Butler客户端桌面源代码](https://github.com/JKerbin/Zhiyin-Butler-Opensource/tree/main/Zhiyin-Desktop)
- [智音Butler客户端内核源代码](https://github.com/JKerbin/Zhiyin-Butler-Opensource/tree/main/Zhiyin-Client)
- [智音Butler远程服务端源代码](https://github.com/JKerbin/Zhiyin-Butler-Opensource/tree/main/Zhiyin-Server)

### 推荐的集成开发环境

- [VSCode](https://code.visualstudio.com/) + [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)

- [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows) + [Anaconda](https://www.anaconda.com/download/)

### 服务器和客户端的部署

- 服务器可以部署在Windows、Ubuntu、CentOS环境中，参考服务器文档部署MySQL数据库
- 需注意openai相关服务不支持部署在中国大陆的服务器，参考服务器文档部署代理
- 桌面版源码支持编译为Linux、macOS、Windows对应的安装程序，但是客户端内核目前仅支持Windows版本
- 部署客户端需要[node.js](https://nodejs.org/en) + [pyinstaller](https://pyinstaller.org/en/stable/)相关依赖

## 更新说明

- 客户端
  - version-beta-0.3.0（重要更新）: 添加了文本聊天模式，可以在设置栏中开启
  - version-beta-0.2.0（重要更新）: 添加了设置界面，可以在设置中自由调整语音模式和收音阈值
  - version-beta-0.1.3: 添加了使用Win11内置的文字转语音API功能，加快响应速度
  - version-beta-0.1.2: 客户端新增开发模式（从config.env中读取配置）和发行模式（从config.py中读取配置）

- 服务端
  - version-beta-0.3.0（重要更新）: 添加了针对文本聊天模式的服务
  - version-beta-0.1.3: 针对客户端使用本地TTS接口的针对性优化
  - version-beta-0.1.2（漏洞修复）: 修复了服务端mysql服务超时断开的bug

