# dmtopython

大漠插件Python API封装,支持窗口操作、系统操作、内存操作等功能。

## 安装

```bash
pip install dmtopython
```

## 快速开始

```python
from dmtopython import DmSoft

# 创建大漠实例
dm = DmSoft(code="your_code", key="your_key")
dm.create_dm()

# 使用窗口模块
hwnd = dm.window.查找窗口("记事本", "")

# 使用系统模块
dm.system.防护盾(1, "memory")

# 使用内存模块
value = dm.memory.读取整数(hwnd, "4A3B2C1D")
```

## 主要功能

### 窗口操作
- 查找窗口
- 绑定窗口
- 获取窗口标题
- 获取窗口状态
- 等等...

### 系统操作
- 防护盾
- 防护盾参数
- 防护盾解除
- 等等...

### 内存操作
- 读写内存
- 读写数据
- 读写字符串
- 等等...

## 注意事项

1. 本模块仅支持Windows系统
2. 需要安装大漠插件并正确注册后才能使用
3. 使用前需要有有效的大漠注册码
4. python需要32位

## 许可证

MIT License

## 作者

nan1989

## 更多信息

- 项目主页: https://github.com/nan1989/dmtopython
- 问题反馈: https://github.com/nan1989/dmtopython/issues 