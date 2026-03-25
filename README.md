# 🔍 Mini Web Vulnerability Scanner

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![Security](https://img.shields.io/badge/Security-WebScanner-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

轻量级 Web 漏洞扫描与可视化分析工具

---

## 一、项目简介

Mini Web Vulnerability Scanner 是一个基于 Python 实现的轻量级 Web 安全扫描工具，用于对目标网站进行自动化漏洞检测与安全分析。

系统通过爬虫技术获取目标页面，并结合插件化检测机制，对常见 Web 漏洞进行扫描与分析，同时生成结构化报告并提供 Web 可视化展示。

扫描过程采用异步架构，前端通过 SSE（Server-Sent Events）实时接收扫描进度，无需等待扫描完成即可看到逐步更新的结果。

本项目适用于：

- Web 安全教学实验  
- 漏洞扫描原理学习  
- 安全工具开发实践  
- 网络安全课程设计  

---

## 二、项目演示

### Web 扫描界面
![Web扫描界面](images/scan_ui.png)

### 实时扫描进度
![实时扫描进度](images/scan_progress.png)

### 扫描结果展示
![扫描结果展示](images/scan_result.png)

---

## 三、CLI 使用示例

执行扫描：

```bash
python main.py --url http://example.com
````

输出示例：

```text
[+] Found URLs
[+] Expanding parameters
[PluginManager] Running SQL Injection Scan
[PluginManager] Running XSS Scan
[PluginManager] Running Directory Scan
[PluginManager] Running Header Scan
```

生成报告：

```text
scan_report.txt
scan_report.json
```

---

## 四、快速开始

启动 Web 界面：

```bash
python webapp.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

---

## 五、项目架构

```mermaid
flowchart TD

A[用户] --> B[Web界面 / CLI]

B --> C[扫描核心 scanner.py]

C --> D1[爬虫模块 crawler.py]
C --> D2[插件管理 plugin_manager.py]

D2 --> E1[SQL注入检测]
D2 --> E2[XSS检测]
D2 --> E3[目录扫描]
D2 --> E4[安全头检测]

C --> F[报告生成 report_generator.py]

F --> G1[TXT报告]
F --> G2[JSON报告]
F --> G3[Web页面展示]
```

---

## 六、工作流程

```mermaid
flowchart TD
A[输入目标URL] --> B[AJAX 提交扫描请求]
B --> C[后台线程异步扫描]
C --> D1[爬取页面]
D1 --> D2[提取URL参数]
D2 --> D3[执行插件扫描]
D3 --> D4[收集漏洞结果]
D4 --> E[生成扫描报告]
C -->|SSE 实时推送进度| F[前端进度条 & 日志流]
E --> G[Web展示 / 下载报告]
```

---

## 七、主要功能

### 1 网站爬取

自动抓取目标站点 URL，并提取参数用于后续漏洞测试。

---

### 2 SQL 注入检测

对 URL 参数进行注入测试，检测潜在 SQL 注入漏洞。

---

### 3 XSS 漏洞检测

检测页面是否存在跨站脚本攻击（XSS）风险。

---

### 4 敏感目录扫描

扫描常见敏感路径：

* /admin
* /login
* /backup

---

### 5 HTTP 安全头检测

检测关键安全头：

* Content-Security-Policy
* X-Frame-Options
* X-XSS-Protection

---

### 6 报告生成

生成两种格式：

```text
scan_report.txt
scan_report.json
```

---

### 7 Web 可视化界面

提供 Web 页面：

* 输入目标 URL
* 一键启动扫描（AJAX 异步提交，无页面刷新）
* **实时进度条与日志流**（SSE 推送，逐插件更新）
* 扫描完成后动态渲染结果，HIGH 风险项自动展开
* 下载 JSON 报告

---

## 八、项目结构

```text
miniwebscanner
│
├── core
│   ├── scanner.py          # 支持 progress_callback 注入
│   ├── crawler.py
│   └── plugin_manager.py   # 插件执行时逐步回调进度
│
├── plugins
│   ├── base_plugin.py
│   ├── sql_injection.py
│   ├── xss_scanner.py
│   ├── dir_scanner.py
│   └── header_scanner.py
│
├── report
│   └── report_generator.py
│
├── templates
│   └── index.html          # AJAX 提交 + SSE 实时进度渲染
│
├── webapp.py               # /scan 启动接口 + /progress SSE 流
├── main.py
├── requirements.txt
└── README.md
```

---

## 九、实时进度机制

扫描采用 **异步 + SSE（Server-Sent Events）** 架构，解决了原有同步阻塞导致用户长时间等待的问题。

```
前端                        后端
 │                            │
 │── POST /scan ─────────────>│ 立即返回 scan_id
 │<─ { scan_id } ─────────────│ 后台线程开始扫描
 │                            │
 │── GET /progress/{id} ─────>│ 建立 SSE 连接
 │<─ event: progress ─────────│ 爬虫阶段完成
 │<─ event: progress ─────────│ 参数扩展完成
 │<─ event: progress ─────────│ 插件1 完成
 │<─ event: progress ─────────│ 插件2 完成
 │        ...                 │        ...
 │<─ event: done ─────────────│ 扫描结束，附带完整报告
```

进度百分比分配：

| 阶段 | 进度区间 |
|------|----------|
| 爬虫 | 5% → 20% |
| 参数扩展 | 25% → 35% |
| 插件扫描（按插件数均分） | 35% → 90% |
| 报告生成 | 95% → 100% |

---

## 十、安装方法

### 1 安装 Python

```bash
Python 3.10+
```

---

### 2 创建虚拟环境

```bash
python -m venv venv
```

激活环境：

```bash
venv\Scripts\activate
```

---

### 3 安装依赖

```bash
pip install -r requirements.txt
```

---

## 十一、使用方法

### CLI 扫描

```bash
python main.py --url http://example.com
```

---

### Web 扫描

```bash
python webapp.py
```

访问：

```text
http://127.0.0.1:5000
```

---

## 十二、技术实现

本项目涉及以下关键技术：

* 爬虫技术（Requests + BeautifulSoup）
* 插件化架构（Plugin Pattern）
* Web 框架（Flask）
* 异步扫描（Threading + Queue）
* 实时推送（SSE / Server-Sent Events）
* 漏洞检测逻辑（SQL Injection / XSS）
* 报告生成（TXT / JSON）

---

## 十三、扩展方向

* 进一步异步化（asyncio / aiohttp 提高爬取效率）
* 增加更多漏洞检测插件（CSRF、SSRF 等）
* 扫描任务队列（Celery / Redis）
* 用户系统与权限管理
* 可视化图表分析（漏洞趋势、风险分布）

---

## 十四、贡献方式

欢迎参与本项目开发：

1. Fork 本仓库
2. 创建新分支
3. 提交 Pull Request

---

## 十五、许可证

本项目采用 MIT License 开源协议
