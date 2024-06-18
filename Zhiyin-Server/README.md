<h1 align="center">ZHIYIN_BUTLER服务端源代码</h1>

<p align="center">基于python3 + flask开发</p>

## 说明

本项目为Zhiyin-Butler服务端源代码，版本为beta0.1.3

包含功能：

- 处理 AI 交互请求
- 用户登录验证
- 邀请码注册

## 基础 URL

```
http://<服务器-ip>:<服务端口>/api/
```

## 端点

### 1. AI 服务

#### 端点
```
POST /api/ai
```

#### 描述
处理用户语音输入并提供 AI 生成的响应，支持普通语音模式和增强语音模式

#### 请求

- **Content-Type**: `application/json`

- **请求体参数**:
    - `speech` (string): Base64 编码的语音数据
    - `speech_len` (int): 语音数据的长度
    - `server_mode` (string): 服务器模式，取值为 `normal` 或 `hd` 或 `local`
    - `program_list` (list): 程序列表（用于功能模式时）

#### 响应

- **Content-Type**: `application/json`

- **响应体**:
    - `type` (string): 响应类型 (`chat`聊天模式或 `func`功能模式)
    - `content` (string): 响应的内容
    - `mode` (string): 响应使用的 TTS 模式

#### 示例

**请求:**
```json
{
    "speech": "base64_encoded_speech_data",
    "speech_len": 12345,
    "server_mode": "normal",
    "program_list": ["app1", "app2"]
}
```

**响应:**
```json
{
    "type": "chat",
    "content": "/A32dfa...（base64编码的音频数据）",
    "mode": "normal"
}
```

### 2. 用户验证

#### 端点
```
POST /api/verification
```

#### 描述
根据提供的 MAC 地址验证用户

#### 请求

- **Content-Type**: `application/json`

- **请求体参数**:
    - `mac` (list): 用户的 MAC 地址列表

#### 响应

- **Content-Type**: `application/json`

- **响应体**:
    - `state` (string): 验证结果 (`success` 或 `failure`)

#### 示例

**请求:**
```json
{
    "mac": ["00-1A-2B-3C-4D-5E","3E-3D-3A-3B-3C-00"]
}
```

**响应:**
```json
{
    "state": "success"
}
```

### 3. 邀请码注册服务

#### 端点
```
POST /api/activation
```

#### 描述
根据提供的 MAC 地址和邀请码激活用户

#### 请求

- **Content-Type**: `application/json`

- **请求体参数**:
    - `mac` (string): 用户的 MAC 地址
    - `invitation` (string): 用户的邀请码

#### 响应

- **Content-Type**: `application/json`

- **响应体**:
    - `state` (string): 激活结果 (`success` 或 `failure`)。

#### 示例

**请求:**
```json
{
    "mac": ["00-1A-2B-3C-4D-5E","3E-3D-3A-3B-3C-00"],
    "invitation": "e4bfc14e-7618-42e3-9241-ed3a55c49485"
}
```

**响应:**
```json
{
    "state": "success"
}
```



## 项目部署

### 安装环境
```bash
$ pip install -r requirements.txt
```

### 部署MySQL数据库（部署本地）

```bash
# 新建MySQL用户
$ CREATE USER 'zhiyin_db'@'127.0.0.1' IDENTIFIED BY 'password（自定的密码）';
# 新建数据库
$ CREATE DATABASE zhiyin;
# 权限管理
$ GRANT ALL PRIVILEGES ON zhiyin.* TO 'zhiyin_db'@'127.0.0.1';
# 新建邀请码表
$ CREATE TABLE invitation_codes (
        invitation VARCHAR(255)
    );
# 新建用户mac表 #
$ CREATE TABLE allowed_users (
        mac_address VARCHAR(17)
    );
# 邀请码表结构
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| invitation | varchar(255) | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
# 用户表结构
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| mac_address | varchar(17) | YES  | UNI | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
```

### 部署代理（仅中国大陆，以使用clash代理为例）

获取配置代理服务，运行服务

如使用Windows系统作为服务器，记得关闭手动代理设置，否则服务器会被全局代理
```bash
# 打开config.env
OPENAI_PROXIES="127.0.0.1:7890"
```

### 配置环境变量

```bash
# 打开config.env
OPENAI_API_KEY="填入你的openai_api_key（用于文本生成和tts_hd接口）"
BAIDU_API_KEY="填入你的百度api_key（用于asr和tts接口生成access_token）"
BAIDU_SECRET_KEY="填入你的百度secret_key（用于asr和tts接口生成access_token）"

DB_USER="zhiyin_db" # 你的MySQL数据库用户名称，建议使用默认zhiyin_db
DB_PASSWORD="填入你的MySQL数据库用户密码"
DB_NAME="zhiyin" # 你的MySQL数据库名称，建议使用默认zhiyin

OPENAI_PROXIES="如果你的服务器部署在中国大陆，此处填入代理服务地址（如clash的地址为：127.0.0.1:7890）"
LOG_PATH="log" # 日志文件目录，建议使用默认
SERVICE_PORT="1228" # 服务端口，默认为1228
```

### 添加邀请码

```bash
# 添加5个邀请码
python invitation.py
```

### 运行服务

```bash
python server.py
```
