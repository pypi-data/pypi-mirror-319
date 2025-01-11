# dmtopython

大漠插件Python封装，提供了简单易用的Python接口。
同时提供 TypeScript 类型定义，方便在 PyWebView 等环境中使用。
并且闲得蛋疼提供了中文函数名.
大漠插件需要32位python环境.
需要注册码和注册密钥.并且大漠插件已注册.

## 安装

```bash
pip install dmtopython
```

## 使用方法

有两种使用方式：

### 1. 使用完整功能（推荐）

```python
from dmtopython import DmSoft

# 创建DM对象并注册
dm = DmSoft(code="注册码", key="注册密钥")


# 使用鼠标功能
dm.mouse.MoveTo(100, 100)
dm.mouse.LeftClick()

# 使用键盘功能
dm.keyboard.KeyPress(65)

# 查找和绑定窗口
hwnd = dm.window.FindWindow("记事本", "无标题")
if hwnd > 0:
    dm.window.BindWindow(hwnd, "normal", "normal", "normal", 0)

# 截图功能
dm.ai.Capture(0, 0, 100, 100, "screen.png")

# 文字识别
text = dm.ocr.Ocr(0, 0, 100, 100, "000000-000000", 0.9)
```

### 2. 单独使用某个功能

如果只需要某个特定功能，可以直接使用对应的类：

```python
# 只使用鼠标功能
from dmtopython import DmMouse

mouse = DmMouse(code="注册码", key="注册密钥")
mouse.MoveTo(100, 100)
mouse.LeftClick()

# 只使用键盘功能
from dmtopython import DmKeyboard

keyboard = DmKeyboard(code="注册码", key="注册密钥")
keyboard.KeyPress(65)

# 只使用窗口操作
from dmtopython import DmWindow

window = DmWindow(code="注册码", key="注册密钥")
hwnd = window.FindWindow("记事本", "无标题")
```
## TypeScript 支持

项目提供了完整的 TypeScript 类型定义文件，可以在 PyWebView 等环境中获得完整的类型提示：

```typescript
// 复制 types/dmsoft.d.ts 到你的项目中

// 在 TypeScript 文件中使用
declare const dm: DmSoftType.DmSoft;

// 现在你可以获得完整的类型提示
dm.mouse.MoveTo(100, 100);
dm.keyboard.KeyPress(65);

// 在 PyWebView 中的使用示例
window.pywebview.api.dm.mouse.MoveTo(100, 100).then(() => {
    console.log('移动鼠标成功');
});

// 所有方法都有完整的参数和返回值类型定义
const hwnd = await window.pywebview.api.dm.window.FindWindow("记事本", "无标题");
if (hwnd > 0) {
    await window.pywebview.api.dm.window.BindWindow(hwnd, "normal", "normal", "normal", 0);
}
```

### 在 PyWebView 中使用

```python
import webview
from dmtopython import DmSoft

class Api:
    def __init__(self):
        self.dm = DmSoft(code="注册码", key="注册密钥")
        if self.dm.create_dm() != 1:
            raise Exception("创建对象失败")

api = Api()
window = webview.create_window('DM示例', html='index.html', js_api=api)
webview.start()
```

```html
<!-- index.html -->
<script>
// 确保 types/dmsoft.d.ts 在项目中
async function clickButton() {
    try {
        // 获得完整的类型提示
        await window.pywebview.api.dm.mouse.MoveTo(100, 100);
        await window.pywebview.api.dm.mouse.LeftClick();
    } catch (e) {
        console.error(e);
    }
}
</script>
```

## 功能模块

- `DmAi`: 截图等AI相关功能
- `DmMouse`: 鼠标操作
- `DmKeyboard`: 键盘操作
- `DmWindow`: 窗口操作
- `DmFoobar`: Foobar控件操作
- `DmMemory`: 内存操作
- `DmSystem`: 系统操作
- `DmOcr`: 文字识别
- `DmFile`: 文件操作
- `DmFind`: 图色查找
- `DmBg`: 后台设置
- `DmAsm`: 汇编操作
- `DmDmg`: 图色设置
- `DmFaq`: 常见问题

## 注意事项

1. 使用前需要安装大漠插件
2. 需要有效的注册码和注册密钥
3. 仅支持Windows系统
4. Python版本要求 >= 3.7 32位

## 贡献

欢迎提交问题和拉取请求到 [GitHub仓库](https://github.com/patrickwu123/dmtopython)。

## 作者

- patrickwu123

## 许可证

MIT License 