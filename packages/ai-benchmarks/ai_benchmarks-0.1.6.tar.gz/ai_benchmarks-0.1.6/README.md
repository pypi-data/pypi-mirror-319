# LLM 推理服务基准测试

本仓库包含了测试常见推理服务吞吐的代码以及相关的测试结果。

## 安装说明

### 基础环境

- Python 3.9 或以上版本
- Poetry (非必须)

请使用以下命令安装 Poetry：
```bash
pip install poetry
```

## 运行方式

### [通过 pip 线上安装运行]

    pip install ai_benchmarks
    run-benchmark -h
    run-app

### [通过 pip手动构建安装运行]

1. **构建包或以其他方式获取：**
    ```bash
    cd ai-benchmarks && poetry build
    ```

2. **安装包：**
    ```bash
    pip install ai_benchmarks-x.x.x.tar.gz
    ```

3. **接口运行方式：**
   - 启动后可访问 [127.0.0.1:8012/docs](http://127.0.0.1:8012/docs) 查看接口文档。
    ```bash
    run-app
    ```

4. **直接运行方式,-h查看帮助，默认执行配置文件默认测试端点：**
    ```bash
    run-benchmark -h
    ```

### [通过代码运行]

1. **安装依赖：**
    ```bash
    cd ai-benchmarks
    poetry安装
    poetry lock && poetry install
    requirements安装
    pip install -i https://mirrors.aliyun.com/pypi/simple/   -r .\requirements.txt
    ```

2. **`benchmark.py`** 是主要的压测脚本，采用 asyncio、AsyncOpenAI 和 ProcessPoolExecutor等 实现多端压测框架。

3. **直接运行压测：**
    ```bash
    poetry run python -m inference.benchmark
    ```

4. **启动接口压测：**
   - 启动后可访问 [127.0.0.1:8012/docs](http://127.0.0.1:8012/docs) 查看接口文档。
    ```bash
    poetry run python -m inference.main
    ```

5. **测试报告和结果：**
   - 测试报告输出到 `inference/report` 文件夹。
   - 原始测试结果数据输出到 `inference/results` 文件夹，可使用 `draw.ipynb` 进行绘图。

## 配置文件说明

```yaml
[section]                  # 支持多section
endpoint:                  # *必须提供一个有效的 endpoint
api_key:                   # 认证KEY
concurrent_requests:       # 同时并发的请求数
batch:                     # 执行批次
duration_enabled:          # 启用持续请求的时间限制（开启后不执行 concurrent_requests）[True/False]
duration_time:             # 请求持续时间，默认为 1 秒
duratio_interval:          # 持续/请求间隔，默认0.2秒
duration_batch:            # 请求持续时间内每次并发数量，默认为 10
ip:                        # 用户查询机器资源占用
username:                  # 用户名
password:                  # 密码
timeout:                   # 超时时间，默认 60 秒
max_retries:               # 最大重试次数，默认 1
max_connections:           # 最大连接数
max_keepalive_connections: # 最大保持活动连接数
model:                     # 自动获取，可手动添加
owned_by:                  # 自动获取，可手动添加
stream:                    # 流式回复默认关闭[True/False]
prompts:                   # 问题, 为空自动匹配默认问题, 格式 [{"id": 1, "prompt": "Output from 1 to 100"}, {"id": 2, "prompt": "List the top 10 most important people in history."},]

