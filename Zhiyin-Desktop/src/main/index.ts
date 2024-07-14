import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { spawn } from 'child_process'
const iconv = require('iconv-lite');
const { exec } = require('child_process');

// 内核进程
let clientCore;
// 内核进程信号
let sig;

// 配置信息
export const config = {
  audioThreshold: '698',
  serverMod: 'local',
};

// 新建窗口
function createBrowserWindow({ icon, width, height, skipTb, onTop }) {
  const window = new BrowserWindow({
    icon: icon,
    width: width,
    height: height,
    transparent: true,
    frame: false,
    resizable: false,
    show: false,
    autoHideMenuBar: true,
    skipTaskbar: skipTb,
    alwaysOnTop: onTop,
    ...(process.platform === 'linux' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  });

  window.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url);
    return { action: 'deny' };
  });

  window.on('ready-to-show', () => {
    window.setTitle('Zhiyin Desktop');
    window.show();
  });

  return window;
}

// 客户端函数
function client() {
  // 初始化窗口
  // 设置窗口
  const settingWindow = createBrowserWindow({ icon: icon, width: 400, height: 500, skipTb: true, onTop: false });
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    settingWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/setting');
  } else {
    const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/setting';
    settingWindow.loadURL(url);
  }
  settingWindow.hide()
  // 文本聊天窗口
  const textWindow = createBrowserWindow({ icon: icon, width: 430, height: 550, skipTb: true, onTop: false });
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    textWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/text');
  } else {
    const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/text';
    textWindow.loadURL(url);
  }
  textWindow.hide()
  // 开始窗口
  const startWindow = createBrowserWindow({ icon: icon, width: 900, height: 670, skipTb: false, onTop: false });
  // 产品激活窗口
  const activationWindow = createBrowserWindow({ icon: icon, width: 900, height: 670, skipTb: false, onTop: false });
  // 主页面浮窗
  const mainWindow = createBrowserWindow({ icon: icon, width: 200, height: 130, skipTb: true, onTop: true });

  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    startWindow.loadURL(process.env['ELECTRON_RENDERER_URL']);
  } else {
    const url = join(__dirname, '../renderer/index.html');
    startWindow.loadFile(url);
  }

  // 文本模式通讯
  ipcMain.handle('text-input', async (_, userInput) => {
    return new Promise((resolve, reject) => {
      const clientCore = spawn('bin/client_text.exe', [userInput]);
      clientCore.stdout.on('data', (data) => {
        const output = iconv.decode(data, 'gbk');
        // const output = data.toString()
        console.log(output)
        const aiOutputIndex = output.indexOf('ai输出：');

        let res;
        if (aiOutputIndex !== -1) {
          res = output.substring(aiOutputIndex + 5); // 截取 "ai输出：" 后的内容
        } else {
          res = '出错了，请检查网络或者程序完整性';
        }

        resolve(res);
      });

      clientCore.stderr.on('data', (data) => {
        reject(data.toString());
      });

      clientCore.on('error', (err) => {
        reject(err.message);
      });
    });
  });

  // 进程管理通讯
  ipcMain.handle('ipc', (_, msg) => {
    if (msg.module === 'close') {
      if (msg.window === 'mainWindow') {
        // 退出主程序
        app.quit();
        // 注意要停止ai子进程
        exec('taskkill /F /IM client_main.exe', () => {
          console.log('client_main closed');
        });
        exec();
      } else if (msg.window === 'startWindow') {
        // 退出主程序
        app.quit();
      } else if (msg.window === 'activationWindow') {
        // 退出主程序
        app.quit();
      } else if (msg.window === 'textWindow') {
        // 关闭聊天窗口
        textWindow.hide()
      }
    }

    if (msg.module === 'setting') {
      // 重启主窗口
      if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
        mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/main');
      } else {
        const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/main';
        mainWindow.loadURL(url);
      }
      // 显示设置窗口
      settingWindow.show()
      // 注意要停止ai子进程
      exec('taskkill /F /IM client_main.exe', () => {
        console.log('client_main closed');
      });
      exec();
    }

    if (msg.module === 'text') {
      // 显示文本聊天窗口
      textWindow.show()
    }

    if (msg.module === 'setconfig') {
      config.audioThreshold = msg.audioThreshold;
      config.serverMod = msg.serverMod;
      console.log(config.audioThreshold)
      console.log(config.serverMod)
      settingWindow.hide()
    }

    else if (msg.module === 'submit_invitation') {
      // 此处
      // 调用验证activation内核模块
      // 参数为msg.invitation，即用户输入的验证码
      clientCore = spawn('bin/client_activation.exe', [msg.invitation])
      clientCore.stdout.on('data', (data) => {
        sig = data.toString();
        console.log(sig)
        if (sig.includes('signal_actfail')) {
          // 启动验证窗口
          if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
            activationWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/activation');
          } else {
            const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/activation';
            activationWindow.loadURL(url);
          }
        } else if (sig.includes('signal_actsucc')) {
          // 启动主窗口
          activationWindow.close();
          if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
            mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/main');
          } else {
            const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/main';
            mainWindow.loadURL(url);
          }
        }
      });
    }

    else if (msg.module === 'begin') {
      startWindow.close();
      // 
      // 此处
      // 调用初始化boot内核模块
      clientCore = spawn('bin/client_boot.exe');
      clientCore.stdout.on('data', (data) => {
        sig = data.toString();
        // 接受内核发送的sig决定开启验证窗口或是主窗口
        if (sig.includes('signal_activation')) {
          // 启动验证窗口
          if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
            activationWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/activation');
          } else {
            const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/activation';
            activationWindow.loadURL(url);
          }
        } else if (sig.includes('signal_main')) {
          // 启动主窗口
          if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
            mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/main');
          } else {
            const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/main';
            mainWindow.loadURL(url);
          }
        } else {
          console.log('unknown');
        }
      });
    }

    // 启动ai子进程
    else if (msg.module === 'mainON') {
      clientCore = spawn('bin/client_main.exe', [config.serverMod, config.audioThreshold])
      clientCore.stdout.on('data', (data) => {
        sig = data.toString();
        console.log(sig);
        if (sig.includes('signal_mainbad')) {
          // 刷新主窗口
          if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
            mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'] + '/#/main');
          } else {
            const url = 'file://' + join(__dirname, '../renderer/index.html') + '#/main';
            mainWindow.loadURL(url);
          }
        }
      });
    }

    // 关闭ai子进程
    else if (msg.module === 'mainOFF') {
      exec('taskkill /F /IM client_main.exe', () => {
        console.log('client_main closed');
      });
      exec();
    }
  });
}

app.whenReady().then(() => {
  // 为windows设置应用程序用户模型id
  electronApp.setAppUserModelId('com.electron')

  // 默认使用F12开启开发者模式
  // 开发模式中忽略Command(Control) + R
  // 更多细节：https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // IPC测试
  ipcMain.on('ping', () => console.log('pong'))

  client()

  app.on('activate', function () {
    // 在macOS上，当单击dock图标并且没有其他打开的窗口时，通常会在应用程序中重新创建一个窗口
    if (BrowserWindow.getAllWindows().length === 0) client()
  })
})

// 关闭所有窗口后退出（macOS除外，应用程序及其菜单栏通常会保持活动状态，直到用户使用Command + Q退出）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
