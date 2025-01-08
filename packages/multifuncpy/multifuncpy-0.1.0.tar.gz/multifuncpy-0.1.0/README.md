# AsyncHttpClient

一个简单易用的异步HTTP客户端，基于aiohttp封装，支持链式调用。

## 特性

- 异步HTTP请求支持
- 链式调用API
- 自动会话管理
- 超时控制
- 统一的错误处理
- 支持自定义headers
- 支持JSON数据

## 安装
```bash
pip install AsyncHttpClient
```

## 快速开始

```python
import asyncio
from async_http_client import AsyncHttpClient

async def main():
    async with AsyncHttpClient() as client:
        # GET请求示例
        response = await client.get('https://api.example.com/users')
        data = await response.json()
        print(data)

        # POST请求示例
        response = await client.post(
            'https://api.example.com/users',
            json_data={"name": "test"}
        )
        result = await response.json()
        print(result)

asyncio.run(main())

```

## API参考

### AsyncHttpClient
#### 主要方法：
- get(url, **kwargs) - 发送GET请求
- post(url, data=None, json_data=None, **kwargs) - 发送POST请求
- put(url, data=None, json_data=None, **kwargs) - 发送PUT请求
- delete(url, data=None, json_data=None,**kwargs) - 发送DELETE请求

## 高级用法
```python
from datetime import timedelta
from async_http_client import AsyncHttpClient

# 自定义配置
client = AsyncHttpClient(
    base_url='https://api.example.com',
    timeout=timedelta(seconds=30),
    headers={'Authorization': 'Bearer token123'}
)

async def main():
    # 使用上下文管理器
    async with client:
        response = await client.get('/users')
        data = await response.json()

```

## 依赖
- Python >= 3.7
- aiohttp

## 许可证
MIT License

## 贡献
欢迎提交Issue和Pull Request！

