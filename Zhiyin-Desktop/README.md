<h1 align="center">ZHIYIN_BUTLER桌面可视化组件</h1>

<p align="center">基于Electron + vite + vue3开发</p>

## 说明

本项目为Zhiyin-Butler桌面可视化组件，版本为beta0.2.0

当前版本包含四个窗口：

- 初始化窗口：startWindow，加载初始化内核，检查网络并验证激活
- 待激活窗口：activationWindow，加载激活内核，用于未激活的客户端
- 主应用窗口：mainWindow，加载主内核程序
- 设置窗口：settingWindow，用户通过设置窗口选择TTS服务模式，调节收音阈值

## 项目部署

### 安装内核

- 打包[智音Butler客户端内核源码](https://github.com/JKerbin/Zhiyin-Butler-Opensource/tree/main/Zhiyin-Client)
```bash
$ pyinstaller -F client_boot.py
$ pyinstaller -F client_activation.py
$ pyinstaller -F client_main.py
```
- 将dist中的的可执行文件复制到本项目的bin目录中
- 将config.env文件复制到本项目目录中

### 安装环境

```bash
$ npm install

# 国内开发者建议使用镜像
$ npm install -g cnpm --registry=https://registry.npmmirror.com
$ cnpm install
```

### 运行项目

```bash
$ npm run dev
```

### 构建项目

```bash
$ npm run build:win
```
中国大陆开发者在第一次构建的时候可能会遇到相关组件拉取失败的问题

建议先下载cashe（版本可能发生变化，以部署时要求的环境为准）：
- [electron-v28.3.2-win32-x64](https://github.com/electron/electron/releases/download/v28.3.2/electron-v28.3.2-win32-x64.zip)
- [winCodeSign-2.6.0.7z](https://github.com/electron-userland/electron-builder-binaries/releases/download/winCodeSign-2.6.0/winCodeSign-2.6.0.7z)
- [nsis-3.0.4.1](https://github.com/electron-userland/electron-builder-binaries/releases/download/nsis-3.0.4.1/nsis-3.0.4.1.7z)
- [nsis-resources-3.4.1](https://github.com/electron-userland/electron-builder-binaries/releases/download/nsis-resources-3.4.1/nsis-resources-3.4.1.7z)
