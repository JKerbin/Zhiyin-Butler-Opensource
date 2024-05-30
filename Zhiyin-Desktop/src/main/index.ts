import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { spawn } from 'child_process'
const { exec } = require('child_process');

// 内核进程
let clientCore;
// 内核进程信号
let sig;

// 新建窗口
function createBrowserWindow({ icon, width, height, skipTb }) {
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
    alwaysOnTop: true,
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
  const startWindow = createBrowserWindow({ icon: icon, width: 900, height: 670, skipTb: false });
  const activationWindow = createBrowserWindow({ icon: icon, width: 900, height: 670, skipTb: false });
  const mainWindow = createBrowserWindow({ icon: icon, width: 180, height: 100, skipTb: true });
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    startWindow.loadURL(process.env['ELECTRON_RENDERER_URL']);
  } else {
    const url = join(__dirname, '../renderer/index.html');
    startWindow.loadFile(url);
  }

  ipcMain.handle('ipc', (_, msg) => {
    if (msg.module === 'close') {
      app.quit();
      // 注意要停止ai子进程
      exec('taskkill /F /IM client_main.exe', () => {
        console.log('client_main closed');
      });
      exec();
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
      clientCore = spawn('bin/client_main.exe')
      clientCore.stdout.on('data', (data) => {
        sig = data.toString();
        console.log(sig);
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

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // IPC test
  ipcMain.on('ping', () => console.log('pong'))

  client()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) client()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
