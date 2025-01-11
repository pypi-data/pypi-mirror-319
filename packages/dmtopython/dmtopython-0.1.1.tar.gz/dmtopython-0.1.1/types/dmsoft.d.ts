declare namespace DmSoftType {
    export interface DmSoft {
        /** 鼠标操作模块 */
        mouse: DmMouse;
        /** 键盘操作模块 */
        keyboard: DmKeyboard;
        /** 窗口操作模块 */
        window: DmWindow;
        /** 图色查找模块 */
        find: DmFind;
        /** 后台设置模块 */
        bg: DmBg;
        /** 文件操作模块 */
        file: DmFile;
        /** 系统操作模块 */
        system: DmSystem;
        /** 内存操作模块 */
        memory: DmMemory;
        /** 文字识别模块 */
        ocr: DmOcr;
        /** 图形控件模块 */
        foobar: DmFoobar;
        /** AI功能模块 */
        ai: DmAi;
        /** FAQ接口 */
        faq: DmFaq;
        /** 驱动防护模块 */
        dmg: DmDmg;

        /**
         * 设置是否开启或者关闭插件内部的图片缓存机制. (默认是打开)
         * @param enable 0: 关闭 1: 打开
         * @returns 0: 失败 1: 成功
         */
        EnablePicCache(enable: number): number;

        /**
         * 获取注册在系统中的dm.dll的路径
         * @returns dm.dll所在路径
         */
        GetBasePath(): string;

        /**
         * 返回当前进程已经创建的dm对象个数
         * @returns 对象个数
         */
        GetDmCount(): number;

        /**
         * 返回当前大漠对象的ID值，这个值对于每个对象是唯一存在的
         * @returns 当前对象的ID值
         */
        GetID(): number;

        /**
         * 获取插件命令的最后错误
         * @returns 错误码
         */
        GetLastError(): number;

        /**
         * 获取全局路径
         * @returns 当前设置的全局路径
         */
        GetPath(): string;

        /**
         * 设定图色的获取方式
         * @param mode 图色输入模式
         * @returns 0: 失败 1: 成功
         */
        SetDisplayInput(mode: string): number;

        /**
         * 设置枚举窗口相关函数的最长延时
         * @param delay 延时值(毫秒)
         * @returns 0: 失败 1: 成功
         */
        SetEnumWindowDelay(delay: number): number;

        /**
         * 设置全局路径
         * @param path 路径
         * @returns 0: 失败 1: 成功
         */
        SetPath(path: string): number;

        /**
         * 设置是否对前台图色进行加速
         * @param enable 0: 关闭 1: 打开
         * @returns 0: 失败 1: 成功
         */
        SpeedNormalGraphic(enable: number): number;

        /**
         * 返回当前插件版本号
         * @returns 版本号字符串
         */
        Ver(): string;

        /**
         * 调用此函数来注册，从而使用插件的高级功能
         * @param reg_code 注册码
         * @param ver_info 版本附加信息（附加码）
         * @returns 
         * - -1: 无法连接网络
         * - -2: 进程没有以管理员方式运行
         * - 0: 失败
         * - 1: 成功
         * - 2: 余额不足
         * - 3: 绑定了本机器，但是账户余额不足50元
         * - 4: 注册码错误
         * - 5: 你的机器或者IP在黑名单列表中或者不在白名单列表中
         * - 6: 非法使用插件
         * - 7: 你的帐号因为非法使用被封禁
         * - 8: ver_info不在你设置的附加白名单中
         * - 77: 机器码或者IP因为非法使用被封禁
         * - 777: 同一个机器码注册次数超过了服务器限制
         */
        Reg(reg_code: string, ver_info: string): number;
    }

    export interface DmMouse {
        /**
         * 设置当前系统鼠标的精确度开关
         * @param enable 0:关闭指针精确度开关 1:打开指针精确度开关
         * @returns 设置之前的精确度开关
         */
        EnableMouseAccuracy(enable: number): number;
        
        /**
         * 获取鼠标位置
         * @returns [x, y] 坐标数组
         */
        GetCursorPos(): [number, number];
        
        /**
         * 获取鼠标特征码
         * @returns 鼠标特征码字符串，失败返回空串
         */
        GetCursorShape(): string;
        
        /**
         * 获取鼠标特征码(扩展)
         * @param type 获取方式 0:方式1 1:方式2
         * @returns 鼠标特征码字符串，失败返回空串
         */
        GetCursorShapeEx(type: number): string;
        
        /**
         * 获取鼠标热点位置
         * @returns 热点坐标字符串，格式"x,y"，失败返回空串
         */
        GetCursorSpot(): string;
        
        /**
         * 获取系统鼠标的移动速度
         * @returns 当前速度(1-11)，失败返回0
         */
        GetMouseSpeed(): number;
        
        /**
         * 按下鼠标左键
         * @returns 是否成功
         */
        LeftClick(): number;
        
        /**
         * 双击鼠标左键
         * @returns 是否成功
         */
        LeftDoubleClick(): number;
        
        /**
         * 按住鼠标左键
         * @returns 是否成功
         */
        LeftDown(): number;
        
        /**
         * 弹起鼠标左键
         * @returns 是否成功
         */
        LeftUp(): number;
        
        /**
         * 按下鼠标中键
         * @returns 是否成功
         */
        MiddleClick(): number;
        
        /**
         * 按住鼠标中键
         * @returns 是否成功
         */
        MiddleDown(): number;
        
        /**
         * 弹起鼠标中键
         * @returns 是否成功
         */
        MiddleUp(): number;
        
        /**
         * 鼠标相对移动
         * @param rx X方向的偏移量
         * @param ry Y方向的偏移量
         * @returns 是否成功
         */
        MoveR(rx: number, ry: number): number;
        
        /**
         * 移动鼠标到指定位置
         * @param x X坐标
         * @param y Y坐标
         * @returns 是否成功
         */
        MoveTo(x: number, y: number): number;
        
        /**
         * 移动鼠标到指定范围内的随机位置
         * @param x 起始X坐标
         * @param y 起始Y坐标
         * @param w 宽度范围
         * @param h 高度范围
         * @returns 实际移动到的坐标，格式"x,y"
         */
        MoveToEx(x: number, y: number, w: number, h: number): string;
        
        /**
         * 按下鼠标右键
         * @returns 是否成功
         */
        RightClick(): number;
        
        /**
         * 按住鼠标右键
         * @returns 是否成功
         */
        RightDown(): number;
        
        /**
         * 弹起鼠标右键
         * @returns 是否成功
         */
        RightUp(): number;
        
        /**
         * 设置鼠标单击或双击的时间间隔
         * @param type 鼠标类型 "normal"|"windows"|"dx"
         * @param delay 延时时间(毫秒)
         * @returns 是否成功
         */
        SetMouseDelay(type: "normal" | "windows" | "dx", delay: number): number;
        
        /**
         * 设置鼠标移动速度
         * @param speed 速度等级(1-11)，推荐6
         * @returns 是否成功
         */
        SetMouseSpeed(speed: number): number;
        
        /**
         * 滚轮向下滚动
         * @returns 是否成功
         */
        WheelDown(): number;
        
        /**
         * 滚轮向上滚动
         * @returns 是否成功
         */
        WheelUp(): number;
        
        /**
         * 等待按键按下
         * @param vk_code 虚拟键码 0:任意键 1:左键 2:右键 4:中键
         * @param time_out 超时时间(毫秒) 0:一直等待
         * @returns 0:超时 1:指定按键按下 其他:按下的按键码
         */
        WaitKey(vk_code: number, time_out: number): number;

        // 中文别名
        启用鼠标精确度(enable: number): number;
        获取鼠标位置(): [number, number];
        获取鼠标特征码(): string;
        获取鼠标特征码EX(type: number): string;
        获取鼠标热点位置(): string;
        获取鼠标速度(): number;
        左键单击(): number;
        左键双击(): number;
        左键按下(): number;
        左键弹起(): number;
        中键单击(): number;
        中键按下(): number;
        中键弹起(): number;
        相对移动(rx: number, ry: number): number;
        移动到(x: number, y: number): number;
        移动到范围(x: number, y: number, w: number, h: number): string;
        右键单击(): number;
        右键按下(): number;
        右键弹起(): number;
        设置鼠标延时(type: "normal" | "windows" | "dx", delay: number): number;
        设置鼠标速度(speed: number): number;
        滚轮向下(): number;
        滚轮向上(): number;
        等待按键(vk_code: number, time_out: number): number;
    }

    export interface DmKeyboard {
        /** 获取指定的按键状态 */
        GetKeyState(vk_code: number): number;
        /** 按住指定的虚拟键码 */
        KeyDown(vk_code: number): number;
        /** 按住指定的按键名 */
        KeyDownChar(key_str: string): number;
        /** 点击指定的虚拟键码 */
        KeyPress(vk_code: number): number;
        /** 点击指定的按键名 */
        KeyPressChar(key_str: string): number;
        /** 按顺序输入文本 */
        KeyPressStr(key_str: string, delay: number): number;
        /** 弹起指定的虚拟键码 */
        KeyUp(vk_code: number): number;
        /** 弹起指定的按键名 */
        KeyUpChar(key_str: string): number;
        /** 设置按键延时 */
        SetKeypadDelay(type: "normal" | "windows" | "dx", delay: number): number;
        /** 设置键鼠模拟方式 */
        SetSimMode(mode: 0 | 1 | 2 | 3): number;
        /** 等待按键按下 */
        WaitKey(vk_code: number, time_out: number): number;

        // 中文别名
        /** 获取指定的按键状态 */
        获取按键状态(vk_code: number): number;
        /** 按住指定的虚拟键码 */
        按下键码(vk_code: number): number;
        /** 按住指定的按键名 */
        按下键名(key_str: string): number;
        /** 点击指定的虚拟键码 */
        点击键码(vk_code: number): number;
        /** 点击指定的按键名 */
        点击键名(key_str: string): number;
        /** 按顺序输入文本 */
        输入文本(key_str: string, delay: number): number;
        /** 弹起指定的虚拟键码 */
        弹起键码(vk_code: number): number;
        /** 弹起指定的按键名 */
        弹起键名(key_str: string): number;
        /** 设置按键延时 */
        设置按键延时(type: "normal" | "windows" | "dx", delay: number): number;
        /** 设置键鼠模拟方式 */
        设置模拟方式(mode: 0 | 1 | 2 | 3): number;
        /** 等待按键按下 */
        等待按键(vk_code: number, time_out: number): number;
    }

    export interface DmWindow {
        /**
         * 把窗口坐标转换为屏幕坐标
         * @param hwnd 指定的窗口句柄
         * @param x 窗口X坐标
         * @param y 窗口Y坐标
         * @returns 0:失败 1:成功
         */
        ClientToScreen(hwnd: number, x: number, y: number): number;

        /**
         * 根据指定进程名,枚举系统中符合条件的进程PID,并且按照进程打开顺序排序
         * @param name 进程名,比如qq.exe
         * @returns 返回所有匹配的进程PID,并按打开顺序排序,格式"pid1,pid2,pid3"
         */
        EnumProcess(name: string): string;

        /**
         * 根据指定条件,枚举系统中符合条件的窗口
         * @param parent 获得的窗口句柄是该窗口的子窗口的窗口句柄,取0时为获得桌面句柄
         * @param title 窗口标题. 此参数是模糊匹配
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param filter 取值定义如下:
         * 1: 匹配窗口标题,参数title有效
         * 2: 匹配窗口类名,参数class_name有效
         * 4: 只匹配指定父窗口的第一层孩子窗口
         * 8: 匹配父窗口为0的窗口,即顶级窗口
         * 16: 匹配可见的窗口
         * 32: 匹配出的窗口按照窗口打开顺序依次排列
         * 这些值可以相加,比如4+8+16就是类似于任务管理器中的窗口列表
         * @returns 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
         */
        EnumWindow(parent: number, title: string, class_name: string, filter: number): string;

        /**
         * 根据指定进程以及其它条件,枚举系统中符合条件的窗口
         * @param process_name 进程映像名.比如(svchost.exe). 此参数是精确匹配,但不区分大小写
         * @param title 窗口标题. 此参数是模糊匹配
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param filter 取值定义如下:
         * 1: 匹配窗口标题,参数title有效
         * 2: 匹配窗口类名,参数class_name有效
         * 4: 只匹配指定映像的所对应的第一个进程
         * 8: 匹配父窗口为0的窗口,即顶级窗口
         * 16: 匹配可见的窗口
         * 32: 匹配出的窗口按照窗口打开顺序依次排列
         * 这些值可以相加,比如4+8+16
         * @returns 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
         */
        EnumWindowByProcess(process_name: string, title: string, class_name: string, filter: number): string;

        /**
         * 根据指定进程pid以及其它条件,枚举系统中符合条件的窗口
         * @param pid 进程pid
         * @param title 窗口标题. 此参数是模糊匹配
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param filter 取值定义如下:
         * 1: 匹配窗口标题,参数title有效
         * 2: 匹配窗口类名,参数class_name有效
         * 8: 匹配父窗口为0的窗口,即顶级窗口
         * 16: 匹配可见的窗口
         * 这些值可以相加,比如2+8+16
         * @returns 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
         */
        EnumWindowByProcessId(pid: number, title: string, class_name: string, filter: number): string;

        /**
         * 根据两组设定条件来枚举指定窗口
         * @param spec1 查找串1. (内容取决于flag1的值)
         * @param flag1 取值如下:
         * 0表示spec1的内容是标题
         * 1表示spec1的内容是程序名字. (比如notepad)
         * 2表示spec1的内容是类名
         * 3表示spec1的内容是程序路径.(不包含盘符,比如\\windows\\system32)
         * 4表示spec1的内容是父句柄.(十进制表达的串)
         * 5表示spec1的内容是父窗口标题
         * 6表示spec1的内容是父窗口类名
         * 7表示spec1的内容是顶级窗口句柄.(十进制表达的串)
         * 8表示spec1的内容是顶级窗口标题
         * 9表示spec1的内容是顶级窗口类名
         * @param type1 取值如下:
         * 0精确判断
         * 1模糊判断
         * @param spec2 查找串2. (内容取决于flag2的值)
         * @param flag2 取值同flag1
         * @param type2 取值同type1
         * @param sort 取值如下:
         * 0不排序
         * 1对枚举出的窗口进行排序,按照窗口打开顺序
         * @returns 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
         */
        EnumWindowSuper(spec1: string, flag1: number, type1: number, spec2: string, flag2: number, type2: number, sort: number): string;

        /**
         * 查找符合条件的窗口
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param title 窗口标题. 此参数是模糊匹配
         * @returns 整形表示的窗口句柄,没找到返回0
         */
        FindWindow(class_name: string, title: string): number;

        /**
         * 根据指定进程以及其它条件,查找符合条件的窗口
         * @param process_name 进程映像名. 此参数是精确匹配,但不区分大小写
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param title 窗口标题. 此参数是模糊匹配
         * @returns 整形表示的窗口句柄,没找到返回0
         */
        FindWindowByProcess(process_name: string, class_name: string, title: string): number;

        /**
         * 根据指定进程pid以及其它条件,查找符合条件的窗口
         * @param process_id 进程pid
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param title 窗口标题. 此参数是模糊匹配
         * @returns 整形表示的窗口句柄,没找到返回0
         */
        FindWindowByProcessId(process_id: number, class_name: string, title: string): number;

        /**
         * 在父窗口的第一层子窗口中查找符合类名或者标题名的窗口
         * @param parent 父窗口句柄
         * @param class_name 窗口类名. 此参数是模糊匹配
         * @param title 窗口标题. 此参数是模糊匹配
         * @returns 整形表示的窗口句柄,没找到返回0
         */
        FindWindowEx(parent: number, class_name: string, title: string): number;

        /**
         * 向指定窗口发送粘贴命令
         * @param hwnd 指定的窗口句柄
         * @returns 0:失败 1:成功
         */
        SendPaste(hwnd: number): number;

        /**
         * 向指定窗口发送文本数据
         * @param hwnd 指定的窗口句柄
         * @param text 发送的文本数据
         * @returns 0:失败 1:成功
         */
        SendString(hwnd: number, text: string): number;

        /**
         * 向指定窗口发送文本数据(另一种模式)
         * @param hwnd 指定的窗口句柄
         * @param text 发送的文本数据
         * @returns 0:失败 1:成功
         */
        SendString2(hwnd: number, text: string): number;

        /**
         * 向绑定的窗口发送文本数据(使用输入法)
         * @param text 发送的文本数据
         * @returns 0:失败 1:成功
         */
        SendStringIme(text: string): number;

        /**
         * 向指定窗口发送文本数据(使用输入法)
         * @param hwnd 指定的窗口句柄
         * @param text 发送的文本数据
         * @param mode 取值意义如下:
         * 0: 向hwnd的窗口输入文字(前提是必须先用模式200安装了输入法)
         * 1: 同模式0,如果由于保护无效，可以尝试此模式.(前提是必须先用模式200安装了输入法)
         * 2: 同模式0,如果由于保护无效，可以尝试此模式. (前提是必须先用模式200安装了输入法)
         * 200: 向系统中安装输入法,多次调用没问题. 全局只用安装一次.
         * 300: 卸载系统中的输入法. 全局只用卸载一次. 多次调用没关系.
         * @returns 0:失败 1:成功
         */
        SendStringIme2(hwnd: number, text: string, mode: number): number;

        /**
         * 设置窗口客户区域的宽度和高度
         * @param hwnd 指定的窗口句柄
         * @param width 宽度
         * @param height 高度
         * @returns 0:失败 1:成功
         */
        SetClientSize(hwnd: number, width: number, height: number): number;

        /**
         * 设置窗口的大小
         * @param hwnd 指定的窗口句柄
         * @param width 宽度
         * @param height 高度
         * @returns 0:失败 1:成功
         */
        SetWindowSize(hwnd: number, width: number, height: number): number;

        /**
         * 设置窗口的状态
         * @param hwnd 指定的窗口句柄
         * @param flag 取值定义如下:
         * 0: 关闭指定窗口
         * 1: 激活指定窗口
         * 2: 最小化指定窗口,但不激活
         * 3: 最小化指定窗口,并释放内存,但同时也会激活窗口
         * 4: 最大化指定窗口,同时激活窗口
         * 5: 恢复指定窗口,但不激活
         * 6: 隐藏指定窗口
         * 7: 显示指定窗口
         * 8: 置顶指定窗口
         * 9: 取消置顶指定窗口
         * 10: 禁止指定窗口
         * 11: 取消禁止指定窗口
         * 12: 恢复并激活指定窗口
         * 13: 强制结束窗口所在进程
         * 14: 闪烁指定的窗口
         * 15: 使指定的窗口获取输入焦点
         * @returns 0:失败 1:成功
         */
        SetWindowState(hwnd: number, flag: number): number;

        /**
         * 设置窗口的标题
         * @param hwnd 指定的窗口句柄
         * @param title 标题
         * @returns 0:失败 1:成功
         */
        SetWindowText(hwnd: number, title: string): number;

        /**
         * 设置窗口的透明度
         * @param hwnd 指定的窗口句柄
         * @param trans 透明度取值(0-255) 越小透明度越大 0为完全透明(不可见) 255为完全显示(不透明)
         * @returns 0:失败 1:成功
         */
        SetWindowTransparent(hwnd: number, trans: number): number;

        /**
         * 设置SendString和SendString2的每个字符之间的发送间隔
         * @param delay 大于等于0的延迟数值. 单位是毫秒. 默认是0
         * @returns 0:失败 1:成功
         */
        SetSendStringDelay(delay: number): number;

        // 中文别名
        窗口坐标转屏幕坐标: (hwnd: number, x: number, y: number) => number;
        枚举进程: (name: string) => string;
        枚举窗口: (parent: number, title: string, class_name: string, filter: number) => string;
        按进程名枚举窗口: (process_name: string, title: string, class_name: string, filter: number) => string;
        按进程ID枚举窗口: (pid: number, title: string, class_name: string, filter: number) => string;
        超级枚举窗口: (spec1: string, flag1: number, type1: number, spec2: string, flag2: number, type2: number, sort: number) => string;
        查找窗口: (class_name: string, title: string) => number;
        按进程名查找窗口: (process_name: string, class_name: string, title: string) => number;
        按进程ID查找窗口: (process_id: number, class_name: string, title: string) => number;
        查找子窗口: (parent: number, class_name: string, title: string) => number;
        发送粘贴: (hwnd: number) => number;
        发送文本: (hwnd: number, text: string) => number;
        发送文本2: (hwnd: number, text: string) => number;
        发送文本到输入法: (text: string) => number;
        发送文本到输入法2: (hwnd: number, text: string, mode: number) => number;
        设置客户区大小: (hwnd: number, width: number, height: number) => number;
        设置窗口大小: (hwnd: number, width: number, height: number) => number;
        设置窗口状态: (hwnd: number, flag: number) => number;
        设置窗口标题: (hwnd: number, title: string) => number;
        设置窗口透明度: (hwnd: number, trans: number) => number;
        设置发送文本延迟: (delay: number) => number;

        /**
         * 获取窗口客户区域的位置
         * @param hwnd 指定的窗口句柄
         * @returns 窗口客户区域在屏幕上的位置,格式为"left,top,right,bottom"
         */
        GetClientRect(hwnd: number): string;

        /**
         * 获取窗口客户区域的宽度和高度
         * @param hwnd 指定的窗口句柄
         * @returns 窗口客户区域的宽度和高度,格式为"width,height"
         */
        GetClientSize(hwnd: number): string;

        /**
         * 获取顶层活动窗口中具有输入焦点的窗口句柄
         * @returns 返回窗口句柄
         */
        GetForegroundFocus(): number;

        /**
         * 获取顶层活动窗口,可以获取到按键自带插件无法获取到的句柄
         * @returns 返回窗口句柄
         */
        GetForegroundWindow(): number;

        /**
         * 获取鼠标指向的窗口句柄,可以获取到按键自带的插件无法获取到的句柄
         * @returns 返回窗口句柄
         */
        GetMousePointWindow(): number;

        /**
         * 根据指定的进程名,获取进程详细信息
         * @param process_name 进程名,比如"qq.exe"
         * @returns 返回格式"pid,进程名,进程全路径"
         */
        GetProcessInfo(process_name: string): string;

        /**
         * 获取特殊窗口
         * @param flag 取值定义如下:
         * 0 : 获取桌面窗口
         * 1 : 获取任务栏窗口
         * @returns 返回窗口句柄
         */
        GetSpecialWindow(flag: number): number;

        /**
         * 获取给定窗口相关的窗口句柄
         * @param hwnd 窗口句柄
         * @param flag 取值定义如下:
         * 0 : 获取父窗口
         * 1 : 获取第一个子窗口
         * 2 : 获取First窗口
         * 3 : 获取Last窗口
         * 4 : 获取下一个窗口
         * 5 : 获取上一个窗口
         * 6 : 获取拥有者窗口
         * 7 : 获取顶层窗口
         * @returns 返回窗口句柄
         */
        GetWindow(hwnd: number, flag: number): number;

        /**
         * 获取窗口的类名
         * @param hwnd 窗口句柄
         * @returns 窗口的类名
         */
        GetWindowClass(hwnd: number): string;

        /**
         * 获取窗口所在进程的进程ID
         * @param hwnd 窗口句柄
         * @returns 返回进程ID
         */
        GetWindowProcessId(hwnd: number): number;

        /**
         * 获取窗口所在进程的exe文件全路径
         * @param hwnd 窗口句柄
         * @returns 返回进程所在的文件路径
         */
        GetWindowProcessPath(hwnd: number): string;

        /**
         * 把屏幕坐标转换为窗口坐标
         * @param hwnd 指定的窗口句柄
         * @param x 屏幕X坐标
         * @param y 屏幕Y坐标
         * @returns 0:失败 1:成功
         */
        ScreenToClient(hwnd: number, x: number, y: number): number;

        // 补充中文别名
        获取窗口客户区域位置: (hwnd: number) => string;
        获取窗口客户区域大小: (hwnd: number) => string;
        获取焦点窗口句柄: () => number;
        获取顶层活动窗口: () => number;
        获取鼠标指向窗口: () => number;
        获取进程信息: (process_name: string) => string;
        获取特殊窗口: (flag: number) => number;
        获取相关窗口句柄: (hwnd: number, flag: number) => number;
        获取窗口类名: (hwnd: number) => string;
        获取窗口进程ID: (hwnd: number) => number;
        获取窗口进程路径: (hwnd: number) => string;
        屏幕坐标转窗口坐标: (hwnd: number, x: number, y: number) => number;

        /**
         * 获取窗口在屏幕上的位置
         * @param hwnd 指定的窗口句柄
         * @returns 窗口在屏幕上的位置,格式为"left,top,right,bottom"
         */
        GetWindowRect(hwnd: number): string;

        /**
         * 获取指定窗口的一些属性
         * @param hwnd 窗口句柄
         * @param flag 取值定义如下:
         * 0: 判断窗口是否存在
         * 1: 判断窗口是否处于激活
         * 2: 判断窗口是否可见
         * 3: 判断窗口是否最小化
         * 4: 判断窗口是否最大化
         * 5: 判断窗口是否置顶
         * 6: 判断窗口是否无响应
         * 7: 判断窗口是否可用(灰色为不可用)
         * 8: 判断窗口是否可鼠标穿透
         * 9: 判断窗口是否置顶
         * @returns 0:不满足条件 1:满足条件
         */
        GetWindowState(hwnd: number, flag: number): number;

        /**
         * 获取窗口的标题
         * @param hwnd 指定的窗口句柄
         * @returns 窗口的标题
         */
        GetWindowTitle(hwnd: number): string;

        // 补充对应的中文别名
        获取窗口位置: (hwnd: number) => string;
        获取窗口状态: (hwnd: number, flag: number) => number;
        获取窗口标题: (hwnd: number) => string;
    }

    export interface DmFind {
        /**
         * 设置多线程查找图片的线程数量
         * @param limit 线程数量
         * @returns 0:失败 1:成功
         */
        SetFindPicMultithreadLimit(limit: number): number;

        /**
         * 设置图片密码
         * @param pwd 图片密码
         * @returns 0:失败 1:成功
         */
        SetPicPwd(pwd: string): number;

        /**
         * 查找指定区域内的图片
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 找到的图片序号(从0开始索引),没找到返回-1
         */
        FindPic(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): number;

        /**
         * 查找指定区域内的所有图片
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        FindPicEx(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的颜色
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式"RRGGBB-DRDGDB",比如"123456-000000"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 找到的点的X坐标,没找到返回-1
         */
        FindColor(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, dir: number): number;

        /**
         * 查找指定区域内的所有颜色
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式"RRGGBB-DRDGDB",比如"123456-000000"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 所有颜色信息的坐标值,格式为"x1,y1|x2,y2|..."
         */
        FindColorEx(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的图片(返回坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回找到的图片序号(从0开始索引)以及X Y坐标,格式为"id,x,y"
         */
        FindPicS(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的所有图片(返回坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        FindPicE(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的图片(内存)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,可以是多个图片,比如"data1|data2|data3"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 找到的图片序号(从0开始索引),没找到返回-1
         */
        FindPicMem(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): number;

        /**
         * 查找指定区域内的所有图片(内存)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,可以是多个图片,比如"data1|data2|data3"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        FindPicMemEx(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的图片(内存,返回坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,可以是多个图片,比如"data1|data2|data3"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回找到的图片序号(从0开始索引)以及X Y坐标,格式为"id,x,y"
         */
        FindPicMemS(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的所有图片(内存,返回坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,可以是多个图片,比如"data1|data2|data3"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        FindPicMemE(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 获取指定图片的尺寸
         * @param pic_name 文件名比如"1.bmp"
         * @returns 形式如"w,h"比如"30,20"
         */
        GetPicSize(pic_name: string): string;

        /**
         * 预先加载指定的图片
         * @param pic_name 文件名比如"1.bmp|2.bmp|3.bmp"等,可以使用通配符,比如"*.bmp"
         * @returns 0:失败 1:成功
         */
        LoadPic(pic_name: string): number;

        /**
         * 释放指定的图片
         * @param pic_name 文件名比如"1.bmp|2.bmp|3.bmp"等,可以使用通配符,比如"*.bmp"
         * @returns 0:失败 1:成功
         */
        FreePic(pic_name: string): number;

        /**
         * 抓取指定区域的动画
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file_name 保存的文件名,保存的地方必须有写入权限
         * @param delay 每帧间隔，单位毫秒。建议60
         * @param time 总共时长，单位毫秒。
         * @returns 0:失败 1:成功
         */
        CaptureGif(x1: number, y1: number, x2: number, y2: number, file_name: string, delay: number, time: number): number;

        /**
         * 判断指定区域的图像是否有变化
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param t 判断时间,单位毫秒
         * @returns 0:没有变化 1:有变化
         */
        IsDisplayDead(x1: number, y1: number, x2: number, y2: number, t: number): number;

        /**
         * 抓取上次操作的图色区域
         * @param file_name 保存的文件名,保存的地方必须有写入权限
         * @returns 0:失败 1:成功
         */
        CapturePre(file_name: string): number;

        /**
         * 抓取指定区域的图像,保存为png格式
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file_name 保存的文件名,保存的地方必须有写入权限
         * @returns 0:失败 1:成功
         */
        CapturePng(x1: number, y1: number, x2: number, y2: number, file_name: string): number;

        /**
         * 抓取指定区域的图像,保存为jpg格式
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file_name 保存的文件名,保存的地方必须有写入权限
         * @returns 0:失败 1:成功
         */
        CaptureJpg(x1: number, y1: number, x2: number, y2: number, file_name: string): number;

        /**
         * 抓取指定区域的图像,保存为bmp格式
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file_name 保存的文件名,保存的地方必须有写入权限
         * @returns 0:失败 1:成功
         */
        CaptureBmp(x1: number, y1: number, x2: number, y2: number, file_name: string): number;

        /**
         * 查找相似图片
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 找到的图片序号(从0开始索引),没找到返回-1
         */
        FindPicSim(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): number;

        /**
         * 查找相似图片(返回所有坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        FindPicSimEx(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找相似图片(返回坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回找到的图片序号和坐标,格式如"index|x|y",比如"3|100|200"
         */
        FindPicSimE(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找形状
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param offset_color 偏移颜色,可以支持任意多个点,格式为"x1|y1|xxxxxx-xxxxxx,x2|y2|xxxxxx-xxxxxx"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 0:没找到 1:找到
         */
        FindShape(x1: number, y1: number, x2: number, y2: number, offset_color: string, sim: number, dir: number): number;

        /**
         * 查找形状(返回坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param offset_color 偏移颜色,可以支持任意多个点,格式为"x1|y1|xxxxxx-xxxxxx,x2|y2|xxxxxx-xxxxxx"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回找到的坐标,格式为"x|y",没找到返回空字符串
         */
        FindShapeE(x1: number, y1: number, x2: number, y2: number, offset_color: string, sim: number, dir: number): string;

        /**
         * 查找形状(返回所有坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param offset_color 偏移颜色,可以支持任意多个点,格式为"x1|y1|xxxxxx-xxxxxx,x2|y2|xxxxxx-xxxxxx"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有找到的坐标,格式为"x1,y1|x2,y2|...",没找到返回空字符串
         */
        FindShapeEx(x1: number, y1: number, x2: number, y2: number, offset_color: string, sim: number, dir: number): string;

        /**
         * 获取指定区域的HSV平均值
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns HSV平均值,格式为"H,S,V"
         */
        GetAveHSV(x1: number, y1: number, x2: number, y2: number): string;

        /**
         * 获取指定区域的RGB平均值
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns RGB平均值,格式为"R,G,B"
         */
        GetAveRGB(x1: number, y1: number, x2: number, y2: number): string;

        /**
         * 获取指定坐标的颜色
         * @param x X坐标
         * @param y Y坐标
         * @returns 颜色字符串,格式"RRGGBB",如"123456"
         */
        GetColor(x: number, y: number): string;

        /**
         * 获取指定坐标的BGR颜色
         * @param x X坐标
         * @param y Y坐标
         * @returns BGR颜色字符串,格式"BBGGRR",如"563412"
         */
        GetColorBGR(x: number, y: number): string;

        /**
         * 获取指定坐标的HSV颜色
         * @param x X坐标
         * @param y Y坐标
         * @returns HSV颜色字符串,格式"H.S.V",如"0.0.0"
         */
        GetColorHSV(x: number, y: number): string;

        /**
         * 获取指定区域的颜色数量
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
         * @param sim 相似度,取值范围0.1-1.0
         * @returns 颜色数量
         */
        GetColorNum(x1: number, y1: number, x2: number, y2: number, color: string, sim: number): number;

        /**
         * 获取指定区域的二进制颜色数据
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns 二进制颜色数据的地址
         */
        GetScreenData(x1: number, y1: number, x2: number, y2: number): number;

        /**
         * 获取指定区域的图像,用24位位图的数据格式返回
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns 0表示失败,1表示成功
         */
        GetScreenDataBmp(x1: number, y1: number, x2: number, y2: number): number;

        /**
         * 转换图片格式为24位BMP格式
         * @param pic_name 要转换的图片名
         * @param bmp_name 要保存的BMP图片名
         * @returns 0表示失败,1表示成功
         */
        ImageToBmp(pic_name: string, bmp_name: string): number;

        /**
         * 把RGB的颜色格式转换为BGR(按键格式)
         * @param rgb_color RGB格式的颜色字符串
         * @returns BGR格式的字符串
         */
        RGB2BGR(rgb_color: string): string;

        /**
         * 设置图色排除区域
         * @param mode 模式,0表示添加,1表示设置颜色,2表示清空
         * @param info 根据mode的取值来决定
         * @returns 0表示失败,1表示成功
         */
        SetExcludeRegion(mode: number, info: string): number;

        /**
         * 设置多线程找图的线程数量
         * @param count 线程数量,最小不能小于2
         * @returns 0表示失败,1表示成功
         */
        SetFindPicMultithreadCount(count: number): number;

        /**
         * 抓取指定区域的图像,保存为24位位图
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file_name 保存的文件名
         * @returns 0表示失败,1表示成功
         */
        Capture(x1: number, y1: number, x2: number, y2: number, file_name: string): number;

        /**
         * 比较指定坐标点的颜色
         * @param x X坐标
         * @param y Y坐标
         * @param color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
         * @param sim 相似度,取值范围0.1-1.0
         * @returns 0表示颜色匹配,1表示颜色不匹配
         */
        CmpColor(x: number, y: number, color: string, sim: number): number;

        /**
         * 开启图色调试模式,此模式会稍许降低图色和文字识别的速度
         * @param enable_debug 0表示关闭,1表示开启
         * @returns 0表示失败,1表示成功
         */
        EnableDisplayDebug(enable_debug: number): number;

        /**
         * 开启多线程找图
         * @param enable 0表示关闭,1表示开启
         * @returns 0表示失败,1表示成功
         */
        EnableFindPicMultithread(enable: number): number;

        /**
         * 允许以截图方式获取颜色
         * @param enable 0表示关闭,1表示开启
         * @returns 0表示失败,1表示成功
         */
        EnableGetColorByCapture(enable: number): number;

        /**
         * 查找指定区域内的所有颜色块
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
         * @param sim 相似度,取值范围0.1-1.0
         * @param count 在宽度为width,高度为height的颜色块中,符合color颜色的最小数量
         * @param width 颜色块的宽度
         * @param height 颜色块的高度
         * @returns 返回所有颜色块信息的坐标值,格式为"x1,y1|x2,y2|..."
         */
        FindColorBlockEx(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, count: number, width: number, height: number): string;

        /**
         * 查找指定区域内的颜色,返回坐标
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回坐标,格式为"x|y",比如"100|200"
         */
        FindColorE(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, dir: number): string;

        /**
         * 根据指定的多点查找颜色坐标,返回坐标
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param first_color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
         * @param offset_color 偏移颜色,格式为"x1|y1|RRGGBB-DRDGDB,x2|y2|RRGGBB-DRDGDB"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回坐标,格式为"x|y",比如"100|200"
         */
        FindMultiColorE(x1: number, y1: number, x2: number, y2: number, first_color: string, offset_color: string, sim: number, dir: number): string;

        /**
         * 从内存加载图片
         * @param addr BMP图像首地址
         * @param size BMP图像大小
         * @param pic_name 文件名,指定这个地址对应的图片名
         * @returns 0表示失败,1表示成功
         */
        LoadPicByte(addr: number, size: number, pic_name: string): number;

        /**
         * 根据通配符获取文件集合
         * @param pic_name 文件名,可以使用通配符,比如"*.bmp"
         * @returns 返回的是通配符对应的文件集合,每个图片以|分割
         */
        MatchPicName(pic_name: string): string;

        // 中文别名
        找图相似(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): number;
        找图相似Ex(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;
        找图相似E(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;
        找形状(x1: number, y1: number, x2: number, y2: number, offset_color: string, sim: number, dir: number): number;
        获取HSV平均值(x1: number, y1: number, x2: number, y2: number): string;
        获取RGB平均值(x1: number, y1: number, x2: number, y2: number): string;
        获取颜色(x: number, y: number): string;
        获取颜色BGR(x: number, y: number): string;
        获取颜色HSV(x: number, y: number): string;
        获取颜色数量(x1: number, y1: number, x2: number, y2: number, color: string, sim: number): number;
        获取屏幕数据(x1: number, y1: number, x2: number, y2: number): number;
        获取屏幕数据位图(x1: number, y1: number, x2: number, y2: number): number;
        图片转BMP(pic_name: string, bmp_name: string): number;
        RGB转BGR(rgb_color: string): string;
        设置排除区域(mode: number, info: string): number;
        设置多线程找图数量(count: number): number;
        抓图(x1: number, y1: number, x2: number, y2: number, file_name: string): number;
        比较颜色(x: number, y: number, color: string, sim: number): number;
        开启调试模式(enable_debug: number): number;
        开启多线程找图(enable: number): number;
        开启截图获取颜色(enable: number): number;
        找色块Ex(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, count: number, width: number, height: number): string;
        找色E(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, dir: number): string;
        找多点色E(x1: number, y1: number, x2: number, y2: number, first_color: string, offset_color: string, sim: number, dir: number): string;
        从内存加载图片(addr: number, size: number, pic_name: string): number;
        匹配图片名(pic_name: string): string;
        找图(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): number;
        找图Ex(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;
        找图E(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;
        找图S(x1: number, y1: number, x2: number, y2: number, pic_name: string, delta_color: string, sim: number, dir: number): string;
        找图内存(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): number;
        找图内存Ex(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;
        找图内存E(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;
        找图内存S(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;
        获取图片大小(pic_name: string): string;
        加载图片(pic_name: string): number;
        释放图片(pic_name: string): number;
        捕获动画(x1: number, y1: number, x2: number, y2: number, file_name: string, delay: number, time: number): number;
        判断图像是否有变化(x1: number, y1: number, x2: number, y2: number, t: number): number;
        捕获上次操作区域(file_name: string): number;
        捕获PNG图片(x1: number, y1: number, x2: number, y2: number, file_name: string): number;
        捕获JPG图片(x1: number, y1: number, x2: number, y2: number, file_name: string): number;
        捕获BMP图片(x1: number, y1: number, x2: number, y2: number, file_name: string): number;
        设置多线程找图线程数(limit: number): number;
        设置图片密码(pwd: string): number;
        找图相似内存(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): number;
        找图相似内存Ex(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 查找相似图片(内存)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,可以是多个图片,比如"data1|data2|data3"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 找到的图片序号(从0开始索引),没找到返回-1
         */
        FindPicSimMem(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): number;

        /**
         * 查找相似图片(内存,返回所有坐标)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,可以是多个图片,比如"data1|data2|data3"
         * @param delta_color 颜色色偏比如"203040"表示RGB的色偏分别是20 30 40
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        FindPicSimMemEx(x1: number, y1: number, x2: number, y2: number, pic_info: string, delta_color: string, sim: number, dir: number): string;

        /**
         * 对指定的数据地址和长度，组合成新的参数. FindPicMem FindPicMemE 以及FindPicMemEx专用
         * @param pic_info 老的地址描述串
         * @param addr 数据地址
         * @param size 数据长度
         * @returns 新的地址描述串
         */
        AppendPicAddr(pic_info: string, addr: number, size: number): string;

        /**
         * 把BGR(按键格式)的颜色格式转换为RGB
         * @param bgr_color bgr格式的颜色字符串
         * @returns RGB格式的字符串
         */
        BGR2RGB(bgr_color: string): string;

        /**
         * 抓取指定区域的动画，保存为gif格式
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file 保存的文件名
         * @param delay 动画间隔，单位毫秒。如果为0，表示只截取静态图片
         * @param time 总共截取多久的动画，单位毫秒
         * @returns 0:失败 1:成功
         */
        CaptureGif(x1: number, y1: number, x2: number, y2: number, file: string, delay: number, time: number): number;

        /**
         * 抓取指定区域的图像,保存为file(JPG压缩格式)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file 保存的文件名
         * @param quality jpg压缩比率(1-100) 越大图片质量越好
         * @returns 0:失败 1:成功
         */
        CaptureJpg(x1: number, y1: number, x2: number, y2: number, file: string, quality: number): number;

        /**
         * 抓取指定区域的图像,保存为PNG格式
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param file 保存的文件名
         * @returns 0:失败 1:成功
         */
        CapturePng(x1: number, y1: number, x2: number, y2: number, file: string): number;

        /**
         * 抓取上次操作的图色区域，保存为file(24位位图)
         * @param file 保存的文件名
         * @returns 0:失败 1:成功
         */
        CapturePre(file: string): number;

        /**
         * 判断指定的区域，在指定的时间内(秒),图像数据是否一直不变.(卡屏)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param t 需要等待的时间,单位是秒
         * @returns 0:没有卡屏 1:卡屏或窗口不见了
         */
        IsDisplayDead(x1: number, y1: number, x2: number, y2: number, t: number): number;

        // 中文别名
        /** 添加图片地址 */
        添加图片地址(pic_info: string, addr: number, size: number): string;
        /** BGR转RGB */
        BGR转RGB(bgr_color: string): string;
        /** 捕获动画 */
        捕获动画(x1: number, y1: number, x2: number, y2: number, file: string, delay: number, time: number): number;
        /** 捕获JPG图片 */
        捕获JPG图片(x1: number, y1: number, x2: number, y2: number, file: string, quality: number): number;
        /** 捕获PNG图片 */
        捕获PNG图片(x1: number, y1: number, x2: number, y2: number, file: string): number;
        /** 捕获上次操作区域 */
        捕获上次操作区域(file: string): number;
        /** 判断图像是否有变化 */
        判断图像是否有变化(x1: number, y1: number, x2: number, y2: number, t: number): number;

        /**
         * 查找指定区域内的颜色块
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
         * @param sim 相似度,取值范围0.1-1.0
         * @param count 在宽度为width,高度为height的颜色块中,符合color颜色的最小数量
         * @param width 颜色块的宽度
         * @param height 颜色块的高度
         * @returns 0:没找到 1:找到
         */
        FindColorBlock(x1: number, y1: number, x2: number, y2: number, color: string, sim: number, count: number, width: number, height: number): number;

        /**
         * 根据指定的多点查找颜色坐标
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param first_color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
         * @param offset_color 偏移颜色,格式为"x1|y1|RRGGBB-DRDGDB,x2|y2|RRGGBB-DRDGDB"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 0:没找到 1:找到
         */
        FindMultiColor(x1: number, y1: number, x2: number, y2: number, first_color: string, offset_color: string, sim: number, dir: number): number;

        /**
         * 根据指定的多点查找所有颜色坐标
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param first_color 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
         * @param offset_color 偏移颜色,格式为"x1|y1|RRGGBB-DRDGDB,x2|y2|RRGGBB-DRDGDB"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回所有颜色信息的坐标值,格式为"x1,y1|x2,y2|..."
         */
        FindMultiColorEx(x1: number, y1: number, x2: number, y2: number, first_color: string, offset_color: string, sim: number, dir: number): string;

        /**
         * 获取指定图片的尺寸
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @returns 形式如 "w,h" 的字符串
         */
        GetPicSize(pic_name: string): string;

        /**
         * 预先加载指定的图片
         * @param pic_name 文件名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @returns 0:失败 1:成功
         */
        LoadPic(pic_name: string): number;

        /**
         * 释放图片
         * @param pic_name 文件名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @returns 0:失败 1:成功
         */
        FreePic(pic_name: string): number;

        /**
         * 获取指定区域的屏幕数据
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns 0:失败 1:成功
         */
        GetScreenData(x1: number, y1: number, x2: number, y2: number): number;

        /**
         * 获取指定区域的屏幕数据,用于二次开发
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param data 返回图片的数据指针
         * @param size 返回图片的数据长度
         * @returns 0:失败 1:成功
         */
        GetScreenDataBmp(x1: number, y1: number, x2: number, y2: number, data: number, size: number): number;

        /**
         * 获取指定区域的HSV平均值
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns HSV平均值字符串,格式为"H.S.V"
         */
        GetAveHSV(x1: number, y1: number, x2: number, y2: number): string;

        /**
         * 获取指定区域的RGB平均值
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @returns RGB平均值字符串,格式为"R.G.B"
         */
        GetAveRGB(x1: number, y1: number, x2: number, y2: number): string;

        /**
         * 获取指定坐标的颜色
         * @param x X坐标
         * @param y Y坐标
         * @returns 颜色字符串,格式为"RRGGBB"
         */
        GetColor(x: number, y: number): string;

        /**
         * 获取指定坐标的颜色,以BGR格式返回
         * @param x X坐标
         * @param y Y坐标
         * @returns 颜色字符串,格式为"BBGGRR"
         */
        GetColorBGR(x: number, y: number): string;

        /**
         * 获取指定坐标的HSV颜色
         * @param x X坐标
         * @param y Y坐标
         * @returns HSV颜色字符串,格式为"H.S.V"
         */
        GetColorHSV(x: number, y: number): string;

        /**
         * 获取指定区域的颜色数量
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color 颜色格式为"RRGGBB-DRDGDB"
         * @param sim 相似度,取值范围0.1-1.0
         * @returns 颜色数量
         */
        GetColorNum(x1: number, y1: number, x2: number, y2: number, color: string, sim: number): number;

        /**
         * 开启图色调试模式,此模式会稍许降低图色和文字识别的速度
         * @param enable 0:关闭 1:开启
         * @returns 0:失败 1:成功
         */
        EnableDisplayDebug(enable: number): number;

        /**
         * 开启多线程找图
         * @param enable 0:关闭 1:开启
         * @returns 0:失败 1:成功
         */
        EnableFindPicMultithread(enable: number): number;

        /**
         * 允许以截图方式获取颜色
         * @param enable 0:关闭 1:开启
         * @returns 0:失败 1:成功
         */
        EnableGetColorByCapture(enable: number): number;

        /**
         * 设置多线程找图的线程数量
         * @param count 线程数量,最小不能小于2
         * @returns 0:失败 1:成功
         */
        SetFindPicMultithreadCount(count: number): number;

        /**
         * 在不解绑的情况下,切换绑定窗口(必须是同进程窗口)
         * @param hwnd 需要切换过去的窗口句柄
         * @returns 0:失败 1:成功
         */
        SwitchBindWindow(hwnd: number): number;

        /**
         * 设置当前对象用于输入的对象,结合图色对象和键鼠对象,用一个对象完成操作
         * @param dm_id 接口GetId的返回值
         * @param rx 两个对象绑定的窗口的左上角坐标的x偏移,一般是0
         * @param ry 两个对象绑定的窗口的左上角坐标的y偏移,一般是0
         * @returns 0:失败 1:成功
         */
        SetInputDm(dm_id: number, rx: number, ry: number): number;

        /**
         * 设置图色检测的延时,默认是0,当图色检测太频繁时(或者在虚拟机下),如果CPU占用过高,可以设置此参数,把图色检测的频率降低
         * @param delay 延时值,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetDisplayDelay(delay: number): number;

        /**
         * 设置opengl图色检测的最长等待时间,在每次检测图色之前,会等待窗口刷新,如果超过此时间,那么就不等待,直接进行图色检测
         * @param delay 等待刷新的时间,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetDisplayRefreshDelay(delay: number): number;

        // 中文别名
        /** 设置图色延时 */
        设置图色延时: (delay: number) => number;
        /** 设置刷新延时 */
        设置刷新延时: (delay: number) => number;

        /**
         * 获取当前绑定的窗口句柄
         * @returns 返回绑定的窗口句柄,如果没有绑定,则返回0
         */
        GetBindWindow(): number;

        /**
         * 判断当前对象是否已经绑定窗口
         * @returns 0: 未绑定 1: 已绑定
         */
        IsBind(): number;

        /**
         * 获取当前绑定窗口的FPS(刷新频率)
         * @returns 返回FPS值
         */
        GetFps(): number;

        // 中文别名
        /** 获取绑定窗口 */
        获取绑定窗口: () => number;
        /** 是否绑定 */
        是否绑定: () => number;
        /** 获取刷新频率 */
        获取刷新频率: () => number;

        /**
         * 开启图色调试模式,此模式会稍许降低图色速度,但是在调试时可以方便看到图色区域
         * @param enable 0: 关闭调试模式 1: 开启调试模式
         * @returns 0:失败 1:成功
         */
        EnableDisplayDebug(enable: number): number;

        /**
         * 设置是否对后台窗口的图色数据进行更新,如果关闭可以省CPU
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableFakeActive(enable: number): number;

        /**
         * 设置是否开启真实鼠标,如果开启,那么所有鼠标相关的操作都会使用真实鼠标进行
         * @param enable 0: 关闭 1: 开启
         * @param delay 操作延时,单位是毫秒
         * @param step 操作步长
         * @returns 0:失败 1:成功
         */
        EnableRealMouse(enable: number, delay?: number, step?: number): number;

        /**
         * 设置是否开启真实键盘,如果开启,那么所有键盘相关的操作都会使用真实键盘进行
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableRealKeypad(enable: number): number;

        // 中文别名
        /** 开启图色调试 */
        开启图色调试: (enable: number) => number;
        /** 开启后台更新 */
        开启后台更新: (enable: number) => number;
        /** 开启真实鼠标 */
        开启真实鼠标: (enable: number, delay?: number, step?: number) => number;
        /** 开启真实键盘 */
        开启真实键盘: (enable: number) => number;

        /**
         * 设置是否开启按键消息,如果开启,那么插件在按键时会向系统发送按键消息
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableKeypadMsg(enable: number): number;

        /**
         * 设置是否开启按键同步,如果开启,那么所有按键相关的操作都会等待按键结束后才返回
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableKeypadSync(enable: number): number;

        /**
         * 设置是否开启鼠标消息,如果开启,那么插件在鼠标点击时会向系统发送鼠标消息
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableMouseMsg(enable: number): number;

        /**
         * 设置是否开启鼠标同步,如果开启,那么所有鼠标相关的操作都会等待鼠标结束后才返回
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableMouseSync(enable: number): number;

        // 中文别名
        /** 开启按键消息 */
        开启按键消息: (enable: number) => number;
        /** 开启按键同步 */
        开启按键同步: (enable: number) => number;
        /** 开启鼠标消息 */
        开启鼠标消息: (enable: number) => number;
        /** 开启鼠标同步 */
        开启鼠标同步: (enable: number) => number;

        /**
         * 设置是否开启速度模式,如果开启,则所有操作都会以最快速度执行,但是可能会引起一些不稳定
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableSpeedDx(enable: number): number;

        /**
         * 锁定系统的输入,可以防止外部输入干扰,注意在锁定后需要解锁,否则会造成系统输入无法恢复
         * @param lock 0: 解锁 1: 锁定
         * @returns 0:失败 1:成功
         */
        LockInput(lock: number): number;

        /**
         * 设置是否关闭系统的Aero效果,可以提高图色的速度
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        SetAero(enable: number): number;

        /**
         * 设置是否显示错误信息,如果不显示,则所有操作都不会弹出错误提示
         * @param show 0: 不显示 1: 显示
         * @returns 0:失败 1:成功
         */
        SetShowErrorMsg(show: number): number;

        // 中文别名
        /** 开启速度模式 */
        开启速度模式: (enable: number) => number;
        /** 锁定输入 */
        锁定输入: (lock: number) => number;
        /** 设置Aero */
        设置Aero: (enable: number) => number;
        /** 设置错误提示 */
        设置错误提示: (show: number) => number;

        /**
         * 设置图色检测时,需要排除的行数,避免干扰项目
         * @param min_row_gap 设置的行数
         * @returns 0:失败 1:成功
         */
        SetMinRowGap(min_row_gap: number): number;

        /**
         * 设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔
         * @param type_id 鼠标操作类型
         * - "normal" : 对应normal鼠标模式
         * - "windows": 对应windows鼠标模式
         * - "dx" : 对应dx鼠标模式
         * @param delay 延时,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetMouseDelay(type_id: string, delay: number): number;

        /**
         * 设置键盘按键按下和弹起的时间间隔
         * @param type_id 键盘操作类型
         * - "normal" : 对应normal键盘模式
         * - "windows": 对应windows键盘模式
         * - "dx" : 对应dx键盘模式
         * @param delay 延时,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetKeypadDelay(type_id: string, delay: number): number;

        /**
         * 设置仿真模式,可以减少CPU占用,但是可能会降低图色速度
         * @param mode 0: 关闭仿真 1: 开启仿真
         * @returns 0:失败 1:成功
         */
        SetSimMode(mode: number): number;

        // 中文别名
        /** 设置最小行距 */
        设置最小行距: (min_row_gap: number) => number;
        /** 设置鼠标延时 */
        设置鼠标延时: (type_id: string, delay: number) => number;
        /** 设置按键延时 */
        设置按键延时: (type_id: string, delay: number) => number;
        /** 设置仿真模式 */
        设置仿真模式: (mode: number) => number;

        /**
         * 设置是否开启按键补丁,用于解决某些情况下按键无效的问题
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableKeypadPatch(enable: number): number;

        // 中文别名
        /** 开启按键补丁 */
        开启按键补丁: (enable: number) => number;
    }

    export interface DmFile {
        /**
         * 拷贝文件
         * @param src_file 原始文件名
         * @param dst_file 目标文件名
         * @param over 0: 不覆盖 1: 覆盖
         * @returns 0: 失败 1: 成功
         */
        CopyFile(src_file: string, dst_file: string, over: number): number;

        /**
         * 创建指定目录
         * @param folder 目录名
         * @returns 0: 失败 1: 成功
         */
        CreateFolder(folder: string): number;

        /**
         * 解密指定的文件
         * @param file 文件名
         * @param pwd 密码
         * @returns 0: 失败 1: 成功
         */
        DecodeFile(file: string, pwd: string): number;

        /**
         * 删除文件
         * @param file 文件名
         * @returns 0: 失败 1: 成功
         */
        DeleteFile(file: string): number;

        /**
         * 删除指定目录
         * @param folder 目录名
         * @returns 0: 失败 1: 成功
         */
        DeleteFolder(folder: string): number;

        /**
         * 删除指定的ini小节
         * @param section 小节名
         * @param key 变量名. 如果为空串则删除整个section小节
         * @param file ini文件名
         * @returns 0: 失败 1: 成功
         */
        DeleteIni(section: string, key: string, file: string): number;

        /**
         * 删除指定的ini小节.支持加密文件
         * @param section 小节名
         * @param key 变量名. 如果为空串则删除整个section小节
         * @param file ini文件名
         * @param pwd 密码
         * @returns 0: 失败 1: 成功
         */
        DeleteIniPwd(section: string, key: string, file: string, pwd: string): number;

        /**
         * 从internet上下载一个文件
         * @param url 下载的url地址
         * @param save_file 要保存的文件名
         * @param timeout 连接超时时间(毫秒)
         * @returns 1: 成功 -1: 网络连接失败 -2: 写入文件失败
         */
        DownloadFile(url: string, save_file: string, timeout: number): number;

        /**
         * 加密指定的文件
         * @param file 文件名
         * @param pwd 密码
         * @returns 0: 失败 1: 成功
         */
        EncodeFile(file: string, pwd: string): number;

        /**
         * 根据指定的ini文件以及section,枚举此section中所有的key名
         * @param section 小节名(不可为空)
         * @param file ini文件名
         * @returns 每个key用"|"连接的字符串,如"aaa|bbb|ccc"
         */
        EnumIniKey(section: string, file: string): string;

        /**
         * 根据指定的ini文件以及section,枚举此section中所有的key名.可支持加密文件
         * @param section 小节名(不可为空)
         * @param file ini文件名
         * @param pwd 密码
         * @returns 每个key用"|"连接的字符串,如"aaa|bbb|ccc"
         */
        EnumIniKeyPwd(section: string, file: string, pwd: string): string;

        /**
         * 根据指定的ini文件,枚举此ini中所有的Section(小节名)
         * @param file ini文件名
         * @returns 每个小节名用"|"连接的字符串,如"aaa|bbb|ccc"
         */
        EnumIniSection(file: string): string;

        /**
         * 获取指定的文件长度
         * @param file 文件名
         * @returns 文件长度(字节数)
         */
        GetFileLength(file: string): number;

        /**
         * 获取指定文件或目录的真实路径
         * @param path 路径名(必须是全路径)
         * @returns 真实路径,失败返回空字符串
         */
        GetRealPath(path: string): string;

        /**
         * 判断指定文件是否存在
         * @param file 文件名
         * @returns 0: 不存在 1: 存在
         */
        IsFileExist(file: string): number;

        /**
         * 判断指定目录是否存在
         * @param folder 目录名
         * @returns 0: 不存在 1: 存在
         */
        IsFolderExist(folder: string): number;

        /**
         * 移动文件
         * @param src_file 原始文件名
         * @param dst_file 目标文件名
         * @returns 0: 失败 1: 成功
         */
        MoveFile(src_file: string, dst_file: string): number;

        /**
         * 从指定的文件读取内容
         * @param file 文件名
         * @returns 读入的文件内容
         */
        ReadFile(file: string): string;

        /**
         * 从Ini中读取指定信息
         * @param section 小节名
         * @param key 变量名
         * @param file ini文件名
         * @returns 读取到的内容
         */
        ReadIni(section: string, key: string, file: string): string;

        /**
         * 从Ini中读取指定信息.可支持加密文件
         * @param section 小节名
         * @param key 变量名
         * @param file ini文件名
         * @param pwd 密码
         * @returns 读取到的内容
         */
        ReadIniPwd(section: string, key: string, file: string, pwd: string): string;

        /**
         * 弹出选择文件夹对话框
         * @returns 选择的文件夹全路径
         */
        SelectDirectory(): string;

        /**
         * 弹出选择文件对话框
         * @returns 选择的文件全路径
         */
        SelectFile(): string;

        /**
         * 向指定文件追加字符串
         * @param file 文件名
         * @param content 写入的字符串
         * @returns 0: 失败 1: 成功
         */
        WriteFile(file: string, content: string): number;

        /**
         * 向指定的Ini写入信息
         * @param section 小节名
         * @param key 变量名
         * @param value 变量内容
         * @param file ini文件名
         * @returns 0: 失败 1: 成功
         */
        WriteIni(section: string, key: string, value: string, file: string): number;

        /**
         * 向指定的Ini写入信息.支持加密文件
         * @param section 小节名
         * @param key 变量名
         * @param value 变量内容
         * @param file ini文件名
         * @param pwd 密码
         * @returns 0: 失败 1: 成功
         */
        WriteIniPwd(section: string, key: string, value: string, file: string, pwd: string): number;

        // 中文别名
        /** 复制文件 */
        复制文件: (src_file: string, dst_file: string, over: number) => number;
        /** 创建目录 */
        创建目录: (folder: string) => number;
        /** 解密文件 */
        解密文件: (file: string, pwd: string) => number;
        /** 删除文件 */
        删除文件: (file: string) => number;
        /** 删除目录 */
        删除目录: (folder: string) => number;
        /** 删除配置项 */
        删除配置项: (section: string, key: string, file: string) => number;
        /** 删除加密配置项 */
        删除加密配置项: (section: string, key: string, file: string, pwd: string) => number;
        /** 下载文件 */
        下载文件: (url: string, save_file: string, timeout: number) => number;
        /** 加密文件 */
        加密文件: (file: string, pwd: string) => number;
        /** 枚举配置项 */
        枚举配置项: (section: string, file: string) => string;
        /** 枚举加密配置项 */
        枚举加密配置项: (section: string, file: string, pwd: string) => string;
        /** 枚举配置节 */
        枚举配置节: (file: string) => string;
        /** 获取文件长度 */
        获取文件长度: (file: string) => number;
        /** 获取真实路径 */
        获取真实路径: (path: string) => string;
        /** 文件是否存在 */
        文件是否存在: (file: string) => number;
        /** 目录是否存在 */
        目录是否存在: (folder: string) => number;
        /** 移动文件 */
        移动文件: (src_file: string, dst_file: string) => number;
        /** 读取文件 */
        读取文件: (file: string) => string;
        /** 读取配置项 */
        读取配置项: (section: string, key: string, file: string) => string;
        /** 读取加密配置项 */
        读取加密配置项: (section: string, key: string, file: string, pwd: string) => string;
        /** 选择目录 */
        选择目录: () => string;
        /** 选择文件 */
        选择文件: () => string;
        /** 写入文件 */
        写入文件: (file: string, content: string) => number;
        /** 写入配置项 */
        写入配置项: (section: string, key: string, value: string, file: string) => number;
        /** 写入加密配置项 */
        写入加密配置项: (section: string, key: string, value: string, file: string, pwd: string) => number;
    }

    export interface DmSystem {
        /**
         * 蜂鸣器
         * @param f 频率
         * @param duration 时长(ms)
         * @returns 0:失败 1:成功
         */
        Beep(f: number, duration: number): number;
        
        /**
         * 检测当前系统是否有开启屏幕字体平滑
         * @returns 0:系统没开启平滑字体 1:系统有开启平滑字体
         */
        CheckFontSmooth(): number;
        
        /**
         * 检测当前系统是否有开启UAC(用户账户控制)
         * @returns 0:没开启UAC 1:开启了UAC
         */
        CheckUAC(): number;
        
        /**
         * 延时指定的毫秒
         * @param mis 毫秒数,必须大于0
         * @returns 0:失败 1:成功
         */
        Delay(mis: number): number;
        
        /**
         * 延时指定范围内随机毫秒
         * @param mis_min 最小毫秒数,必须大于0
         * @param mis_max 最大毫秒数,必须大于0
         * @returns 0:失败 1:成功
         */
        Delays(mis_min: number, mis_max: number): number;
        
        /**
         * 设置当前的电源设置，禁止关闭显示器，禁止关闭硬盘，禁止睡眠，禁止待机
         * @returns 0:失败 1:成功
         */
        DisableCloseDisplayAndSleep(): number;
        
        /**
         * 关闭当前系统屏幕字体平滑
         * @returns 0:失败 1:成功
         */
        DisableFontSmooth(): number;
        
        /**
         * 关闭电源管理，不会进入睡眠
         * @returns 0:失败 1:成功
         */
        DisablePowerSave(): number;
        
        /**
         * 关闭屏幕保护
         * @returns 0:失败 1:成功
         */
        DisableScreenSave(): number;
        
        /**
         * 开启当前系统屏幕字体平滑
         * @returns 0:失败 1:成功
         */
        EnableFontSmooth(): number;
        
        /**
         * 退出系统(注销/重启/关机)
         * @param type 0:注销系统 1:关机 2:重新启动
         * @returns 0:失败 1:成功
         */
        ExitOs(type: number): number;
        
        /**
         * 获取剪贴板的内容
         * @returns 剪贴板内容
         */
        GetClipboard(): string;
        
        /**
         * 获取当前CPU类型
         * @returns 0:未知 1:Intel cpu 2:AMD cpu
         */
        GetCpuType(): number;
        
        /**
         * 获取当前CPU的使用率
         * @returns 0-100表示的百分比
         */
        GetCpuUsage(): number;
        
        /**
         * 得到系统的路径
         * @param type 0:当前路径 1:系统路径 2:windows路径 3:临时目录路径 4:当前进程路径
         * @returns 路径字符串
         */
        GetDir(type: number): string;
        
        /**
         * 获取本机的指定硬盘的厂商信息
         * @param index 硬盘序号(0-5)
         * @returns 硬盘厂商信息
         */
        GetDiskModel(index: number): string;
        
        /**
         * 获取本机的指定硬盘的修正版本信息
         * @param index 硬盘序号(0-5)
         * @returns 修正版本信息
         */
        GetDiskReversion(index: number): string;
        
        /**
         * 获取本机的指定硬盘的序列号
         * @param index 硬盘序号(0-5)
         * @returns 硬盘序列号
         */
        GetDiskSerial(index: number): string;
        
        /**
         * 获取本机的显卡信息
         * @returns 显卡信息字符串,多个显卡用|分隔
         */
        GetDisplayInfo(): string;
        
        /**
         * 判断当前系统的DPI是否是100%缩放
         * @returns 0:不是 1:是
         */
        GetDPI(): number;
        
        /**
         * 判断当前系统使用的非UNICODE字符集是否是GB2312
         * @returns 0:不是GB2312 1:是GB2312
         */
        GetLocale(): number;
        
        /**
         * 获取本机的机器码(带网卡)
         * @returns 机器码字符串
         */
        GetMachineCode(): string;
        
        /**
         * 获取本机的机器码(不带网卡)
         * @returns 机器码字符串
         */
        GetMachineCodeNoMac(): string;
        
        /**
         * 获取当前内存的使用率
         * @returns 0-100表示的百分比
         */
        GetMemoryUsage(): number;
        
        /**
         * 从网络获取当前北京时间
         * @returns 时间字符串,格式"yyyy-MM-dd HH:mm:ss"
         */
        GetNetTime(): string;
        
        /**
         * 根据指定时间服务器IP获取网络时间
         * @param ip IP或域名,支持多个用|分隔
         * @returns 时间字符串,格式"yyyy-MM-dd HH:mm:ss"
         */
        GetNetTimeByIp(ip: string): string;
        
        /**
         * 得到操作系统的build版本号
         * @returns build版本号,失败返回0
         */
        GetOsBuildNumber(): number;
        
        /**
         * 得到操作系统的类型
         * @returns 系统类型代码
         */
        GetOsType(): number;
        
        /**
         * 获取屏幕的色深
         * @returns 系统颜色深度
         */
        GetScreenDepth(): number;
        
        /**
         * 获取屏幕的高度
         * @returns 屏幕高度
         */
        GetScreenHeight(): number;
        
        /**
         * 获取屏幕的宽度
         * @returns 屏幕宽度
         */
        GetScreenWidth(): number;
        
        /**
         * 获取当前系统从开机到现在所经历的时间
         * @returns 时间(毫秒)
         */
        GetTime(): number;
        
        /**
         * 判断当前系统是否是64位操作系统
         * @returns 0:不是64位系统 1:是64位系统
         */
        Is64Bit(): number;
        
        /**
         * 判断当前CPU是否支持vt,并且是否在bios中开启了vt
         * @returns 0:不支持 1:支持
         */
        IsSupportVt(): number;
        
        /**
         * 播放指定的MP3或者wav文件
         * @param media_file 音乐文件名或完整路径
         * @returns 0:失败 非0:播放ID
         */
        Play(media_file: string): number;
        
        /**
         * 运行指定的应用程序
         * @param app_path 程序路径
         * @param mode 0:普通模式 1:加强模式
         * @returns 0:失败 1:成功
         */
        RunApp(app_path: string, mode: number): number;
        
        /**
         * 设置剪贴板的内容
         * @param value 要设置的内容
         * @returns 0:失败 1:成功
         */
        SetClipboard(value: string): number;
        
        /**
         * 设置系统的分辨率和色深
         * @param width 屏幕宽度
         * @param height 屏幕高度
         * @param depth 系统色深
         * @returns 0:失败 1:成功
         */
        SetScreen(width: number, height: number, depth: number): number;
        
        /**
         * 设置当前系统的UAC
         * @param enable 0:关闭UAC 1:开启UAC
         * @returns 0:失败 1:成功
         */
        SetUAC(enable: number): number;
        
        /**
         * 显示或隐藏指定窗口在任务栏的图标
         * @param hwnd 窗口句柄
         * @param is_show 0:隐藏 1:显示
         * @returns 0:失败 1:成功
         */
        ShowTaskBarIcon(hwnd: number, is_show: number): number;
        
        /**
         * 停止指定的音乐
         * @param id Play返回的播放ID
         * @returns 0:失败 1:成功
         */
        Stop(id: number): number;
        
        /**
         * 激活指定窗口所在进程的输入法
         * @param hwnd 窗口句柄
         * @param input_method 输入法名字
         * @returns 0:失败 1:成功
         */
        ActiveInputMethod(hwnd: number, input_method: string): number;
        
        /**
         * 检测指定窗口所在线程输入法是否开启
         * @param hwnd 窗口句柄
         * @param input_method 输入法名字
         * @returns 0:未开启 1:开启
         */
        CheckInputMethod(hwnd: number, input_method: string): number;
        
        /**
         * 检测是否可以进入临界区
         * @returns 0:不可以进入 1:已经进入临界区
         */
        enter_cri(): number;
        
        /**
         * 运行指定的cmd指令
         * @param cmd 指令
         * @param current_dir 运行的目录
         * @returns 运行指令的输出结果
         */
        execute_cmd(cmd: string, current_dir: string): string;
        
        /**
         * 根据指定的输入法名字查找系统中对应的输入法
         * @param input_method 输入法名字
         * @returns 输入法键盘布局字符串,失败返回空串
         */
        find_input_method(input_method: string): string;
        
        /**
         * 初始化临界区
         * @returns 0:失败 1:成功
         */
        init_cri(): number;
        
        /**
         * 离开临界区
         * @returns 0:失败 1:成功
         */
        leave_cri(): number;
        
        /**
         * 释放引用
         * @returns 0:失败 1:成功
         */
        release_ref(): number;
        
        /**
         * 设置是否允许脚本调用此对象的退出线程
         * @param enable 0:不允许 1:允许
         * @returns 0:失败 1:成功
         */
        set_exit_thread(enable: number): number;
        
        /**
         * 排除指定范围内的坐标
         * @param all_pos 坐标描述串
         * @param type 类型
         * @param x1 左上角X坐标
         * @param y1 左上角Y坐标
         * @param x2 右下角X坐标
         * @param y2 右下角Y坐标
         * @returns 处理后的坐标描述串
         */
        exclude_pos(all_pos: string, type: number, x1: number, y1: number, x2: number, y2: number): string;
        
        /**
         * 查找最近指定坐标的坐标
         * @param all_pos 坐标描述串
         * @param type 类型
         * @param x X坐标
         * @param y Y坐标
         * @returns 最近的坐标描述串
         */
        find_nearest_pos(all_pos: string, type: number, x: number, y: number): string;
        
        /**
         * 对所有坐标根据距离进行排序
         * @param all_pos 坐标描述串
         * @param type 类型
         * @param x X坐标
         * @param y Y坐标
         * @returns 排序后的坐标描述串
         */
        sort_pos_distance(all_pos: string, type: number, x: number, y: number): string;
        
        /**
         * 获取指定的系统信息
         * @param type 信息类型
         * @param method 获取方法
         * @returns 系统信息字符串
         */
        GetSystemInfo(type: string, method: number): string;
        
        /**
         * 设置当前系统的硬件加速级别
         * @param level 加速级别(0-5)
         * @returns 0:失败 1:成功
         */
        SetDisplayAcceler(level: number): number;
        
        /**
         * 设置当前系统的非UNICODE字符集
         * @returns 0:失败 1:成功
         */
        SetLocale(): number;

        // 中文别名
        蜂鸣(f: number, duration: number): number;
        检查字体平滑(): number;
        检查UAC(): number;
        延时(mis: number): number;
        随机延时(mis_min: number, mis_max: number): number;
        禁止关闭显示器和睡眠(): number;
        禁用字体平滑(): number;
        禁用电源管理(): number;
        禁用屏幕保护(): number;
        启用字体平滑(): number;
        退出系统(type: number): number;
        获取剪贴板(): string;
        获取CPU类型(): number;
        获取CPU使用率(): number;
        获取目录(type: number): string;
        获取硬盘型号(index: number): string;
        获取硬盘版本(index: number): string;
        获取硬盘序列号(index: number): string;
        获取显卡信息(): string;
        获取DPI(): number;
        获取区域设置(): number;
        获取机器码(): string;
        获取机器码NoMac(): string;
        获取内存使用率(): number;
        获取网络时间(): string;
        获取网络时间ByIP(ip: string): string;
        获取系统版本号(): number;
        获取系统类型(): number;
        获取屏幕色深(): number;
        获取屏幕高度(): number;
        获取屏幕宽度(): number;
        获取时间(): number;
        是否64位(): number;
        是否支持VT(): number;
        播放(media_file: string): number;
        运行程序(app_path: string, mode: number): number;
        设置剪贴板(value: string): number;
        设置屏幕(width: number, height: number, depth: number): number;
        设置UAC(enable: number): number;
        显示任务栏图标(hwnd: number, is_show: number): number;
        停止(id: number): number;
        激活输入法(hwnd: number, input_method: string): number;
        检查输入法(hwnd: number, input_method: string): number;
        进入临界区(): number;
        执行CMD指令(cmd: string, current_dir: string): string;
        查找输入法(input_method: string): string;
        初始化临界区(): number;
        离开临界区(): number;
        释放引用(): number;
        设置退出线程(enable: number): number;
        排除坐标(all_pos: string, type: number, x1: number, y1: number, x2: number, y2: number): string;
        查找最近坐标(all_pos: string, type: number, x: number, y: number): string;
        坐标距离排序(all_pos: string, type: number, x: number, y: number): string;
        获取系统信息(type: string, method: number): string;
        设置显示加速(level: number): number;
        设置区域(): number;
    }

    export interface DmMemory {
        /**
         * 读取指定地址的二进制数据
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param length 要读取的长度
         * @returns 读取到的数据,以16进制字符串表示,每个字节以空格分隔
         */
        ReadData(hwnd: number, addr: string, length: number): string;
        
        /**
         * 读取指定地址的二进制数据
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param length 要读取的长度
         * @returns 读取到的数据,以16进制字符串表示,每个字节以空格分隔
         */
        ReadDataAddr(hwnd: number, addr: number, length: number): string;
        
        /**
         * 读取指定地址的二进制数据到指针
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param length 要读取的长度
         * @returns 读取到的数据指针,0表示失败
         */
        ReadDataToBin(hwnd: number, addr: string, length: number): number;
        
        /**
         * 读取指定地址的二进制数据到指针
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param length 要读取的长度
         * @returns 读取到的数据指针,0表示失败
         */
        ReadDataAddrToBin(hwnd: number, addr: number, length: number): number;
        
        /**
         * 读取指定地址的双精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @returns 读取到的双精度浮点数
         */
        ReadDouble(hwnd: number, addr: string): number;
        
        /**
         * 读取指定地址的双精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @returns 读取到的双精度浮点数
         */
        ReadDoubleAddr(hwnd: number, addr: number): number;
        
        /**
         * 读取指定地址的单精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @returns 读取到的单精度浮点数
         */
        ReadFloat(hwnd: number, addr: string): number;
        
        /**
         * 读取指定地址的单精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @returns 读取到的单精度浮点数
         */
        ReadFloatAddr(hwnd: number, addr: number): number;
        
        /**
         * 读取指定地址的整数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param type 整数类型 0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
         * @returns 读取到的整数
         */
        ReadInt(hwnd: number, addr: string, type: number): number;
        
        /**
         * 读取指定地址的整数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param type 整数类型 0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
         * @returns 读取到的整数
         */
        ReadIntAddr(hwnd: number, addr: number, type: number): number;
        
        /**
         * 搜索指定的二进制数据
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param data 要搜索的数据
         * @param step 搜索步长
         * @param multi_thread 是否多线程 0:否 1:是
         * @param mode 搜索模式 0:所有内存 1:仅可写内存
         * @returns 搜索到的地址列表,以|分隔
         */
        FindDataEx(hwnd: number, addr_range: string, data: string, step: number, multi_thread: number, mode: number): string;
        
        /**
         * 搜索指定的双精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param double_value_min 最小值
         * @param double_value_max 最大值
         * @returns 搜索到的地址列表,以|分隔
         */
        FindDouble(hwnd: number, addr_range: string, double_value_min: number, double_value_max: number): string;
        
        /**
         * 搜索指定的单精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param float_value_min 最小值
         * @param float_value_max 最大值
         * @returns 搜索到的地址列表,以|分隔
         */
        FindFloat(hwnd: number, addr_range: string, float_value_min: number, float_value_max: number): string;
        
        /**
         * 搜索指定的整数
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param int_value_min 最小值
         * @param int_value_max 最大值
         * @param type 整数类型 0:32位 1:16位 2:8位 3:64位
         * @returns 搜索到的地址列表,以|分隔
         */
        FindInt(hwnd: number, addr_range: string, int_value_min: number, int_value_max: number, type: number): string;
        
        /**
         * 搜索指定的字符串
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param string_value 要搜索的字符串
         * @param type 字符串类型 0:Ascii 1:Unicode 2:UTF8
         * @returns 搜索到的地址列表,以|分隔
         */
        FindString(hwnd: number, addr_range: string, string_value: string, type: number): string;
        
        /**
         * 写入二进制数据
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param data 要写入的数据
         * @returns 是否成功
         */
        WriteData(hwnd: number, addr: string, data: string): number;
        
        /**
         * 写入二进制数据
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param data 要写入的数据
         * @returns 是否成功
         */
        WriteDataAddr(hwnd: number, addr: number, data: string): number;
        
        /**
         * 写入双精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param v 要写入的值
         * @returns 是否成功
         */
        WriteDouble(hwnd: number, addr: string, v: number): number;
        
        /**
         * 写入双精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param v 要写入的值
         * @returns 是否成功
         */
        WriteDoubleAddr(hwnd: number, addr: number, v: number): number;
        
        /**
         * 写入单精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param v 要写入的值
         * @returns 是否成功
         */
        WriteFloat(hwnd: number, addr: string, v: number): number;
        
        /**
         * 写入单精度浮点数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param v 要写入的值
         * @returns 是否成功
         */
        WriteFloatAddr(hwnd: number, addr: number, v: number): number;
        
        /**
         * 写入整数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param type 整数类型 0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
         * @param v 要写入的值
         * @returns 是否成功
         */
        WriteInt(hwnd: number, addr: string, type: number, v: number): number;
        
        /**
         * 写入整数
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param type 整数类型 0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
         * @param v 要写入的值
         * @returns 是否成功
         */
        WriteIntAddr(hwnd: number, addr: number, type: number, v: number): number;
        
        /**
         * 写入字符串
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址字符串
         * @param type 字符串类型 0:Ascii 1:Unicode 2:UTF8
         * @param v 要写入的字符串
         * @returns 是否成功
         */
        WriteString(hwnd: number, addr: string, type: number, v: string): number;
        
        /**
         * 写入字符串
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param type 字符串类型 0:Ascii 1:Unicode 2:UTF8
         * @param v 要写入的字符串
         * @returns 是否成功
         */
        WriteStringAddr(hwnd: number, addr: number, type: number, v: string): number;
        
        /**
         * 分配内存
         * @param hwnd 窗口句柄或进程ID
         * @param addr 预期地址,0表示自动分配
         * @param size 内存大小
         * @param type 内存类型 0:可读写执行 1:可读执行 2:可读写
         * @returns 分配的内存地址,0表示失败
         */
        VirtualAllocEx(hwnd: number, addr: number, size: number, type: number): number;
        
        /**
         * 释放内存
         * @param hwnd 窗口句柄或进程ID
         * @param addr 要释放的内存地址
         * @returns 是否成功
         */
        VirtualFreeEx(hwnd: number, addr: number): number;
        
        /**
         * 修改内存属性
         * @param hwnd 窗口句柄或进程ID
         * @param addr 内存地址
         * @param size 内存大小
         * @param type 属性类型 0:可读写执行 1:使用old_protect指定
         * @param old_protect 原属性
         * @returns 修改前的属性,0表示失败
         */
        VirtualProtectEx(hwnd: number, addr: number, size: number, type: number, old_protect: number): number;
        
        /**
         * 查询内存属性
         * @param hwnd 窗口句柄或进程ID
         * @param addr 内存地址
         * @param pmbi 结构体地址,可为0
         * @returns 内存信息字符串
         */
        VirtualQueryEx(hwnd: number, addr: number, pmbi: number): string;
        
        /**
         * 设置是否使用进程ID模式
         * @param en 0:关闭 1:开启
         * @returns 是否成功
         */
        SetMemoryHwndAsProcessId(en: number): number;
        
        /**
         * 设置内存查找结果保存到文件
         * @param file 文件路径,空字符串表示取消
         * @returns 是否成功
         */
        SetMemoryFindResultToFile(file: string): number;
        
        /**
         * 打开进程
         * @param pid 进程ID
         * @returns 进程句柄,0表示失败
         */
        OpenProcess(pid: number): number;
        
        /**
         * 结束进程
         * @param pid 进程ID
         * @returns 是否成功
         */
        TerminateProcess(pid: number): number;
        
        /**
         * 结束进程及其子进程
         * @param pid 进程ID
         * @returns 是否成功
         */
        TerminateProcessTree(pid: number): number;
        
        /**
         * 获取进程命令行
         * @param hwnd 窗口句柄或进程ID
         * @returns 命令行字符串
         */
        GetCommandLine(hwnd: number): string;
        
        /**
         * 获取模块基址
         * @param hwnd 窗口句柄或进程ID
         * @param module 模块名
         * @returns 模块基址
         */
        GetModuleBaseAddr(hwnd: number, module: string): number;
        
        /**
         * 获取模块大小
         * @param hwnd 窗口句柄或进程ID
         * @param module 模块名
         * @returns 模块大小
         */
        GetModuleSize(hwnd: number, module: string): number;
        
        /**
         * 释放进程内存
         * @param hwnd 窗口句柄或进程ID
         * @returns 是否成功
         */
        FreeProcessMemory(hwnd: number): number;
        
        /**
         * 浮点数转二进制数据
         * @param value 浮点数
         * @returns 二进制数据字符串
         */
        FloatToData(value: number): string;
        
        /**
         * 整数转二进制数据
         * @param value 整数
         * @param type 类型 0:4字节 1:2字节 2:1字节 3:8字节
         * @returns 二进制数据字符串
         */
        IntToData(value: number, type: number): string;
        
        /**
         * 字符串转二进制数据
         * @param value 字符串
         * @param type 类型 0:Ascii 1:Unicode
         * @returns 二进制数据字符串
         */
        StringToData(value: string, type: number): string;

        // 中文别名
        读取数据(hwnd: number, addr: string, length: number): string;
        读取数据_地址(hwnd: number, addr: number, length: number): string;
        读取数据到指针(hwnd: number, addr: string, length: number): number;
        读取数据到指针_地址(hwnd: number, addr: number, length: number): number;
        读取双精度浮点数(hwnd: number, addr: string): number;
        读取双精度浮点数_地址(hwnd: number, addr: number): number;
        读取单精度浮点数(hwnd: number, addr: string): number;
        读取单精度浮点数_地址(hwnd: number, addr: number): number;
        读取整数(hwnd: number, addr: string, type: number): number;
        读取整数_地址(hwnd: number, addr: number, type: number): number;
        查找数据Ex(hwnd: number, addr_range: string, data: string, step: number, multi_thread: number, mode: number): string;
        查找双精度浮点数(hwnd: number, addr_range: string, double_value_min: number, double_value_max: number): string;
        查找单精度浮点数(hwnd: number, addr_range: string, float_value_min: number, float_value_max: number): string;
        查找整数(hwnd: number, addr_range: string, int_value_min: number, int_value_max: number, type: number): string;
        查找字符串(hwnd: number, addr_range: string, string_value: string, type: number): string;
        写入数据(hwnd: number, addr: string, data: string): number;
        写入数据_地址(hwnd: number, addr: number, data: string): number;
        写入双精度浮点数(hwnd: number, addr: string, v: number): number;
        写入双精度浮点数_地址(hwnd: number, addr: number, v: number): number;
        写入单精度浮点数(hwnd: number, addr: string, v: number): number;
        写入单精度浮点数_地址(hwnd: number, addr: number, v: number): number;
        写入整数(hwnd: number, addr: string, type: number, v: number): number;
        写入整数_地址(hwnd: number, addr: number, type: number, v: number): number;
        写入字符串(hwnd: number, addr: string, type: number, v: string): number;
        写入字符串_地址(hwnd: number, addr: number, type: number, v: string): number;
        分配内存(hwnd: number, addr: number, size: number, type: number): number;
        释放内存(hwnd: number, addr: number): number;
        修改内存属性(hwnd: number, addr: number, size: number, type: number, old_protect: number): number;
        查询内存属性(hwnd: number, addr: number, pmbi: number): string;
        设置进程ID模式(en: number): number;
        设置查找结果保存(file: string): number;
        打开进程(pid: number): number;
        结束进程(pid: number): number;
        结束进程树(pid: number): number;
        获取命令行(hwnd: number): string;
        获取模块基址(hwnd: number, module: string): number;
        获取模块大小(hwnd: number, module: string): number;
        释放进程内存(hwnd: number): number;
        浮点数转数据(value: number): string;
        整数转数据(value: number, type: number): string;
        字符串转数据(value: string, type: number): string;

        /**
         * 搜索指定的双精度浮点数(扩展版)
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param double_value_min 最小值
         * @param double_value_max 最大值
         * @param step 搜索步长
         * @param multi_thread 是否多线程 0:否 1:是
         * @param mode 搜索模式 0:所有内存 1:仅可写内存
         * @returns 搜索到的地址列表,以|分隔
         */
        FindDoubleEx(hwnd: number, addr_range: string, double_value_min: number, double_value_max: number, step: number, multi_thread: number, mode: number): string;
        
        /**
         * 搜索指定的单精度浮点数(扩展版)
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param float_value_min 最小值
         * @param float_value_max 最大值
         * @param step 搜索步长
         * @param multi_thread 是否多线程 0:否 1:是
         * @param mode 搜索模式 0:所有内存 1:仅可写内存
         * @returns 搜索到的地址列表,以|分隔
         */
        FindFloatEx(hwnd: number, addr_range: string, float_value_min: number, float_value_max: number, step: number, multi_thread: number, mode: number): string;
        
        /**
         * 搜索指定的整数(扩展版)
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param int_value_min 最小值
         * @param int_value_max 最大值
         * @param type 整数类型 0:32位 1:16位 2:8位 3:64位
         * @param step 搜索步长
         * @param multi_thread 是否多线程 0:否 1:是
         * @param mode 搜索模式 0:所有内存 1:仅可写内存
         * @returns 搜索到的地址列表,以|分隔
         */
        FindIntEx(hwnd: number, addr_range: string, int_value_min: number, int_value_max: number, type: number, step: number, multi_thread: number, mode: number): string;
        
        /**
         * 搜索指定的字符串(扩展版)
         * @param hwnd 窗口句柄或进程ID
         * @param addr_range 地址范围
         * @param string_value 要搜索的字符串
         * @param type 字符串类型 0:Ascii 1:Unicode 2:UTF8
         * @param step 搜索步长
         * @param multi_thread 是否多线程 0:否 1:是
         * @param mode 搜索模式 0:所有内存 1:仅可写内存
         * @returns 搜索到的地址列表,以|分隔
         */
        FindStringEx(hwnd: number, addr_range: string, string_value: string, type: number, step: number, multi_thread: number, mode: number): string;
        
        /**
         * 从数据指针写入二进制数据
         * @param hwnd 窗口句柄或进程ID
         * @param addr 地址
         * @param data 数据指针
         * @param len 数据长度
         * @returns 是否成功
         */
        WriteDataAddrFromBin(hwnd: number, addr: number, data: number, len: number): number;
        
        /**
         * 设置64位参数转指针(E语言兼容)
         * @returns 是否成功
         */
        SetParam64ToPointer(): number;
        
        /**
         * 64位整数转32位
         * @param value 64位整数
         * @returns 32位整数
         */
        Int64ToInt32(value: number): number;

        // 中文别名
        查找双精度浮点数Ex(hwnd: number, addr_range: string, double_value_min: number, double_value_max: number, step: number, multi_thread: number, mode: number): string;
        查找单精度浮点数Ex(hwnd: number, addr_range: string, float_value_min: number, float_value_max: number, step: number, multi_thread: number, mode: number): string;
        查找整数Ex(hwnd: number, addr_range: string, int_value_min: number, int_value_max: number, type: number, step: number, multi_thread: number, mode: number): string;
        查找字符串Ex(hwnd: number, addr_range: string, string_value: string, type: number, step: number, multi_thread: number, mode: number): string;
        写入数据从指针(hwnd: number, addr: number, data: number, len: number): number;
        设置64位参数转指针(): number;
        转换64位到32位(value: number): number;
    }

    export interface DmOcr {
        /**
         * 给指定的字库中添加一条字库信息
         * @param index 字库的序号(0-99)
         * @param dict_info 字库描述串
         * @returns 0: 失败 1: 成功
         */
        AddDict(index: number, dict_info: string): number;

        /**
         * 清空指定的字库
         * @param index 字库的序号(0-99)
         * @returns 0: 失败 1: 成功
         */
        ClearDict(index: number): number;

        /**
         * 允许当前调用的对象使用全局字库
         * @param enable 0: 关闭 1: 打开
         * @returns 0: 失败 1: 成功
         */
        EnableShareDict(enable: number): number;

        /**
         * 根据指定的范围和颜色描述，提取点阵信息
         * @param x1 左上角X坐标
         * @param y1 左上角Y坐标
         * @param x2 右下角X坐标
         * @param y2 右下角Y坐标
         * @param color 颜色格式串
         * @param word 待定义的文字
         * @returns 识别到的点阵信息，失败返回空
         */
        FetchWord(x1: number, y1: number, x2: number, y2: number, color: string, word: string): string;

        /**
         * 在屏幕范围内查找字符串
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param string 待查找的字符串
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns [index, x, y] index为字符串索引,-1表示未找到
         */
        FindStr(x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number): [number, number, number];

        /**
         * 在屏幕范围内查找字符串(返回字符串格式)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param string 待查找的字符串
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns "id|x|y"格式的字符串,未找到返回"-1|-1|-1"
         */
        FindStrE(x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number): string;

        /**
         * 设置字库文件
         * @param index 字库的序号(0-99)
         * @param file 字库文件名
         * @returns 0: 失败 1: 成功
         */
        SetDict(index: number, file: string): number;

        /**
         * 从内存中设置字库
         * @param index 字库的序号(0-99)
         * @param addr 数据地址
         * @param size 字库长度
         * @returns 0: 失败 1: 成功
         */
        SetDictMem(index: number, addr: number, size: number): number;

        /**
         * 设置字库的密码
         * @param pwd 字库密码
         * @returns 0: 失败 1: 成功
         */
        SetDictPwd(pwd: string): number;

        /**
         * 设定是否开启精准识别
         * @param exact_ocr 0: 关闭 1: 开启
         * @returns 0: 失败 1: 成功
         */
        SetExactOcr(exact_ocr: number): number;

        /**
         * 设定列间距
         * @param min_col_gap 最小列间距
         * @returns 0: 失败 1: 成功
         */
        SetMinColGap(min_col_gap: number): number;

        /**
         * 设定行间距
         * @param min_row_gap 最小行间距
         * @returns 0: 失败 1: 成功
         */
        SetMinRowGap(min_row_gap: number): number;

        /**
         * 设定文字的行距(不使用字库)
         * @param row_gap 文字行距
         * @returns 0: 失败 1: 成功
         */
        SetRowGapNoDict(row_gap: number): number;

        /**
         * 设定词组间的间隔
         * @param word_gap 单词间距
         * @returns 0: 失败 1: 成功
         */
        SetWordGap(word_gap: number): number;

        /**
         * 设定词组间的间隔(不使用字库)
         * @param word_gap 单词间距
         * @returns 0: 失败 1: 成功
         */
        SetWordGapNoDict(word_gap: number): number;

        /**
         * 设定文字的平均行高
         * @param line_height 行高
         * @returns 0: 失败 1: 成功
         */
        SetWordLineHeight(line_height: number): number;

        /**
         * 设定文字的平均行高(不使用字库)
         * @param line_height 行高
         * @returns 0: 失败 1: 成功
         */
        SetWordLineHeightNoDict(line_height: number): number;

        /**
         * 使用指定的字库文件进行识别
         * @param index 字库编号(0-99)
         * @returns 0: 失败 1: 成功
         */
        UseDict(index: number): number;

        // 中文别名
        /** 添加字库 */
        添加字库: (index: number, dict_info: string) => number;
        /** 清空字库 */
        清空字库: (index: number) => number;
        /** 开启全局字库 */
        开启全局字库: (enable: number) => number;
        /** 提取文字 */
        提取文字: (x1: number, y1: number, x2: number, y2: number, color: string, word: string) => string;
        /** 查找文字 */
        查找文字: (x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number) => [number, number, number];
        /** 查找文字Ex */
        查找文字Ex: (x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number) => string;
        /** 设置字库 */
        设置字库: (index: number, file: string) => number;
        /** 设置内存字库 */
        设置内存字库: (index: number, addr: number, size: number) => number;
        /** 设置字库密码 */
        设置字库密码: (pwd: string) => number;
        /** 设置精准识别 */
        设置精准识别: (exact_ocr: number) => number;
        /** 设置最小列间距 */
        设置最小列间距: (min_col_gap: number) => number;
        /** 设置最小行间距 */
        设置最小行间距: (min_row_gap: number) => number;
        /** 设置无字库行距 */
        设置无字库行距: (row_gap: number) => number;
        /** 设置词间距 */
        设置词间距: (word_gap: number) => number;
        /** 设置无字库词间距 */
        设置无字库词间距: (word_gap: number) => number;
        /** 设置行高 */
        设置行高: (line_height: number) => number;
        /** 设置无字库行高 */
        设置无字库行高: (line_height: number) => number;
        /** 使用字库 */
        使用字库: (index: number) => number;

        /**
         * 在屏幕范围内查找字符串,返回所有位置
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param string 待查找的字符串
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns "id,x,y|id,x,y..|id,x,y"格式的字符串
         */
        FindStrEx(x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number): string;

        /**
         * 快速查找字符串,返回字符串格式
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param string 待查找的字符串
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns "id|x|y"格式的字符串,未找到返回"-1|-1|-1"
         */
        FindStrFastE(x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number): string;

        /**
         * 快速查找字符串,返回所有位置
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param string 待查找的字符串
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns "id,x,y|id,x,y..|id,x,y"格式的字符串
         */
        FindStrFastEx(x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number): string;

        /**
         * 查找字符串,返回坐标
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param string 待查找的字符串
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns [x, y] 坐标,未找到返回[-1, -1]
         */
        FindStrS(x1: number, y1: number, x2: number, y2: number, string: string, color_format: string, sim: number): [number, number];

        /**
         * 识别屏幕范围内的字符串
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns 识别到的字符串
         */
        Ocr(x1: number, y1: number, x2: number, y2: number, color_format: string, sim: number): string;

        /**
         * 识别屏幕范围内的字符串,返回识别到的字符串及坐标
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns "字符串1,x1,y1|字符串2,x2,y2|..."格式的字符串
         */
        OcrEx(x1: number, y1: number, x2: number, y2: number, color_format: string, sim: number): string;

        /**
         * 保存字库到文件
         * @param index 字库的序号(0-99)
         * @param file 字库文件名
         * @returns 0: 失败 1: 成功
         */
        SaveDict(index: number, file: string): number;

        /**
         * 从文件中识别文字
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片文件名
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns 识别到的字符串
         */
        OcrInFile(x1: number, y1: number, x2: number, y2: number, pic_name: string, color_format: string, sim: number): string;

        /**
         * 设定列间距(不使用字库)
         * @param col_gap 列间距
         * @returns 0: 失败 1: 成功
         */
        SetColGapNoDict(col_gap: number): number;

        /**
         * 设置字库密码(不使用字库)
         * @param pwd 字库密码
         * @returns 0: 失败 1: 成功
         */
        SetDictPwdNoDict(pwd: string): number;

        // 中文别名
        /** 文件识别 */
        文件识别: (x1: number, y1: number, x2: number, y2: number, pic_name: string, color_format: string, sim: number) => string;
        /** 设置无字库列间距 */
        设置无字库列间距: (col_gap: number) => number;
        /** 设置无字库密码 */
        设置无字库密码: (pwd: string) => number;

        /**
         * 获取字库数量
         * @returns 字库数量
         */
        GetDictCount(): number;

        /**
         * 获取字库详细信息
         * @param index 字库序号(0-99)
         * @returns 字库详细信息
         */
        GetDictInfo(index: number): string;

        /**
         * 获取当前使用的字库序号
         * @returns 当前使用的字库序号
         */
        GetNowDict(): number;

        /**
         * 获取识别到的字符数量
         * @returns 识别到的字符数量
         */
        GetWordResultCount(): number;

        /**
         * 获取识别到的字符坐标
         * @param index 字符序号
         * @returns [x1, y1, x2, y2] 字符的左上角和右下角坐标
         */
        GetWordResultPos(index: number): [number, number, number, number];

        /**
         * 获取指定字库中的字符
         * @param index 字库序号(0-99)
         * @param color_format 颜色格式串
         * @returns 字库中的字符
         */
        GetWords(index: number, color_format: string): string;

        /**
         * 不使用字库时，获取识别到的字符
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color_format 颜色格式串
         * @returns 识别到的字符
         */
        GetWordsNoDict(x1: number, y1: number, x2: number, y2: number, color_format: string): string;

        /**
         * 识别屏幕范围内的字符串(返回第一个)
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param color_format 颜色格式串
         * @param sim 相似度(0.1-1.0)
         * @returns [str, x, y] 识别到的字符串及其坐标
         */
        OcrExOne(x1: number, y1: number, x2: number, y2: number, color_format: string, sim: number): [string, number, number];

        // 中文别名
        /** 获取字库数量 */
        获取字库数量: () => number;
        /** 获取字库信息 */
        获取字库信息: (index: number) => string;
        /** 获取当前字库 */
        获取当前字库: () => number;
        /** 获取识别结果数量 */
        获取识别结果数量: () => number;
        /** 获取识别结果位置 */
        获取识别结果位置: (index: number) => [number, number, number, number];
        /** 获取字库字符 */
        获取字库字符: (index: number, color_format: string) => string;
        /** 获取无字库字符 */
        获取无字库字符: (x1: number, y1: number, x2: number, y2: number, color_format: string) => string;
        /** 文字识别单个 */
        文字识别单个: (x1: number, y1: number, x2: number, y2: number, color_format: string, sim: number) => [string, number, number];

        /**
         * 设置OCR引擎
         * @param engine 引擎类型 0: 默认引擎 1: 精准引擎
         * @returns 0: 失败 1: 成功
         */
        SetOcrEngine(engine: number): number;

        /**
         * 设置OCR匹配模式
         * @param mode 匹配模式 0: 精准匹配 1: 模糊匹配
         * @returns 0: 失败 1: 成功
         */
        SetOcrMatchMode(mode: number): number;

        /**
         * 设置OCR输出长度
         * @param len 输出长度
         * @returns 0: 失败 1: 成功
         */
        SetOcrOutputLen(len: number): number;

        /**
         * 设置OCR超时时间
         * @param timeout 超时时间(毫秒)
         * @returns 0: 失败 1: 成功
         */
        SetOcrTimeout(timeout: number): number;

        /**
         * 使用OCR引擎
         * @param engine 引擎类型 0: 默认引擎 1: 精准引擎
         * @returns 0: 失败 1: 成功
         */
        UseOcrEngine(engine: number): number;

        /**
         * 使用OCR匹配模式
         * @param mode 匹配模式 0: 精准匹配 1: 模糊匹配
         * @returns 0: 失败 1: 成功
         */
        UseOcrMatchMode(mode: number): number;

        /**
         * 使用OCR输出长度
         * @param len 输出长度
         * @returns 0: 失败 1: 成功
         */
        UseOcrOutputLen(len: number): number;

        // 中文别名
        /** 设置OCR引擎 */
        设置OCR引擎: (engine: number) => number;
        /** 设置OCR匹配模式 */
        设置OCR匹配模式: (mode: number) => number;
        /** 设置OCR输出长度 */
        设置OCR输出长度: (len: number) => number;
        /** 设置OCR超时 */
        设置OCR超时: (timeout: number) => number;
        /** 使用OCR引擎 */
        使用OCR引擎: (engine: number) => number;
        /** 使用OCR匹配模式 */
        使用OCR匹配模式: (mode: number) => number;
        /** 使用OCR输出长度 */
        使用OCR输出长度: (len: number) => number;
    }

    export interface DmFoobar {
        /**
         * 根据指定的位图创建一个自定义形状的窗口
         * @param hwnd 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param pic_name 位图名字. 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制.
         * @param trans_color 透明色(RRGGBB)
         * @param sim 透明色的相似值 0.1-1.0
         * @returns 创建成功的窗口句柄
         */
        CreateFoobarCustom(hwnd: number, x: number, y: number, pic_name: string, trans_color: string, sim: number): number;

        /**
         * 创建一个椭圆窗口
         * @param hwnd 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param w 矩形区域的宽度
         * @param h 矩形区域的高度
         * @returns 创建成功的窗口句柄
         */
        CreateFoobarEllipse(hwnd: number, x: number, y: number, w: number, h: number): number;

        /**
         * 创建一个矩形窗口
         * @param hwnd 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param w 矩形区域的宽度
         * @param h 矩形区域的高度
         * @returns 创建成功的窗口句柄
         */
        CreateFoobarRect(hwnd: number, x: number, y: number, w: number, h: number): number;

        /**
         * 创建一个圆角矩形窗口
         * @param hwnd 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param w 矩形区域的宽度
         * @param h 矩形区域的高度
         * @param rw 圆角的宽度
         * @param rh 圆角的高度
         * @returns 创建成功的窗口句柄
         */
        CreateFoobarRoundRect(hwnd: number, x: number, y: number, w: number, h: number, rw: number, rh: number): number;

        /**
         * 清除指定的Foobar滚动文本区
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @returns 0:失败 1:成功
         */
        FoobarClearText(hwnd: number): number;

        /**
         * 关闭一个Foobar,注意,必须调用此函数来关闭窗口,用SetWindowState也可以关闭,但会造成内存泄漏
         * @param hwnd 指定的Foobar窗口句柄
         * @returns 0:失败 1:成功
         */
        FoobarClose(hwnd: number): number;

        /**
         * 在指定的Foobar窗口内部画线条
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @param x1 左上角X坐标(相对于hwnd客户区坐标)
         * @param y1 左上角Y坐标(相对于hwnd客户区坐标)
         * @param x2 右下角X坐标(相对于hwnd客户区坐标)
         * @param y2 右下角Y坐标(相对于hwnd客户区坐标)
         * @param color 填充的颜色值
         * @param style 画笔类型. 0为实线. 1为虚线
         * @param width 线条宽度
         * @returns 0:失败 1:成功
         */
        FoobarDrawLine(hwnd: number, x1: number, y1: number, x2: number, y2: number, color: string, style: number, width: number): number;

        /**
         * 在指定的Foobar窗口绘制图像
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param pic_name 图像文件名 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制.
         * @param trans_color 图像透明色
         * @returns 0:失败 1:成功
         */
        FoobarDrawPic(hwnd: number, x: number, y: number, pic_name: string, trans_color: string): number;

        /**
         * 在指定的Foobar窗口绘制文字
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param w 矩形区域的宽度
         * @param h 矩形区域的高度
         * @param text 字符串
         * @param color 文字颜色值
         * @param align 对齐方式 1:左对齐 2:中间对齐 4:右对齐
         * @returns 0:失败 1:成功
         */
        FoobarDrawText(hwnd: number, x: number, y: number, w: number, h: number, text: string, color: string, align: number): number;

        /**
         * 在指定的Foobar窗口内部填充矩形
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @param x1 左上角X坐标(相对于hwnd客户区坐标)
         * @param y1 左上角Y坐标(相对于hwnd客户区坐标)
         * @param x2 右下角X坐标(相对于hwnd客户区坐标)
         * @param y2 右下角Y坐标(相对于hwnd客户区坐标)
         * @param color 填充的颜色值
         * @returns 0:失败 1:成功
         */
        FoobarFillRect(hwnd: number, x1: number, y1: number, x2: number, y2: number, color: string): number;

        /**
         * 锁定指定的Foobar窗口,不能通过鼠标来移动
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @returns 0:失败 1:成功
         */
        FoobarLock(hwnd: number): number;

        /**
         * 向指定的Foobar窗口区域内输出滚动文字
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param text 文本内容
         * @param color 文本颜色
         * @returns 0:失败 1:成功
         */
        FoobarPrintText(hwnd: number, text: string, color: string): number;

        /**
         * 设置指定Foobar窗口的字体
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param font_name 系统字体名,注意,必须保证系统中有此字体
         * @param size 字体大小
         * @param flag 字体类型 0:正常 1:粗体 2:斜体 4:下划线
         * @returns 0:失败 1:成功
         */
        FoobarSetFont(hwnd: number, font_name: string, size: number, flag: number): number;

        /**
         * 设置保存指定的Foobar滚动文本区信息到文件
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param file 保存的文件名
         * @param enable 0:关闭向文件输出 1:开启向文件输出
         * @param header 输出的附加头信息
         * @returns 0:失败 1:成功
         */
        FoobarSetSave(hwnd: number, file: string, enable: number, header: string): number;

        /**
         * 设置指定Foobar窗口的是否透明
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param is_trans 是否透明 0:不透明 1:透明
         * @param color 透明色(RRGGBB)
         * @param sim 透明色的相似值 0.1-1.0
         * @returns 0:失败 1:成功
         */
        FoobarSetTrans(hwnd: number, is_trans: number, color: string, sim: number): number;

        /**
         * 在指定的Foobar窗口绘制gif动画
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param pic_name 图像文件名 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制.
         * @param repeat_limit 重复次数 0:一直循环 >0:循环指定次数
         * @param delay 帧间隔时间(毫秒) 0:使用GIF内置的时间 >0:使用指定的时间
         * @returns 0:失败 1:成功
         */
        FoobarStartGif(hwnd: number, x: number, y: number, pic_name: string, repeat_limit: number, delay: number): number;

        /**
         * 停止在指定foobar里显示的gif动画
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @param x 左上角X坐标(相对于hwnd客户区坐标)
         * @param y 左上角Y坐标(相对于hwnd客户区坐标)
         * @param pic_name 图像文件名
         * @returns 0:失败 1:成功
         */
        FoobarStopGif(hwnd: number, x: number, y: number, pic_name: string): number;

        /**
         * 设置滚动文本区的文字行间距,默认是3
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param line_gap 文本行间距
         * @returns 0:失败 1:成功
         */
        FoobarTextLineGap(hwnd: number, line_gap: number): number;

        /**
         * 设置滚动文本区的文字输出方向,默认是0
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param dir 0:向下输出 1:向上输出
         * @returns 0:失败 1:成功
         */
        FoobarTextPrintDir(hwnd: number, dir: number): number;

        /**
         * 设置指定Foobar窗口的滚动文本框范围,默认的文本框范围是窗口区域
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @param x x坐标
         * @param y y坐标
         * @param w 宽度
         * @param h 高度
         * @returns 0:失败 1:成功
         */
        FoobarTextRect(hwnd: number, x: number, y: number, w: number, h: number): number;

        /**
         * 解锁指定的Foobar窗口,可以通过鼠标来移动
         * @param hwnd 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
         * @returns 0:失败 1:成功
         */
        FoobarUnlock(hwnd: number): number;

        /**
         * 刷新指定的Foobar窗口
         * @param hwnd 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
         * @returns 0:失败 1:成功
         */
        FoobarUpdate(hwnd: number): number;

        // 中文别名
        创建自定义形状窗口: DmFoobar['CreateFoobarCustom'];
        创建椭圆窗口: DmFoobar['CreateFoobarEllipse'];
        创建矩形窗口: DmFoobar['CreateFoobarRect'];
        创建圆角矩形窗口: DmFoobar['CreateFoobarRoundRect'];
        清除文本: DmFoobar['FoobarClearText'];
        关闭窗口: DmFoobar['FoobarClose'];
        画线: DmFoobar['FoobarDrawLine'];
        绘制图片: DmFoobar['FoobarDrawPic'];
        绘制文字: DmFoobar['FoobarDrawText'];
        填充矩形: DmFoobar['FoobarFillRect'];
        锁定窗口: DmFoobar['FoobarLock'];
        打印文字: DmFoobar['FoobarPrintText'];
        设置字体: DmFoobar['FoobarSetFont'];
        设置保存: DmFoobar['FoobarSetSave'];
        设置透明: DmFoobar['FoobarSetTrans'];
        播放动画: DmFoobar['FoobarStartGif'];
        停止动画: DmFoobar['FoobarStopGif'];
        设置行间距: DmFoobar['FoobarTextLineGap'];
        设置文字方向: DmFoobar['FoobarTextPrintDir'];
        设置文本区域: DmFoobar['FoobarTextRect'];
        解锁窗口: DmFoobar['FoobarUnlock'];
        刷新窗口: DmFoobar['FoobarUpdate'];
    }

    export interface DmAi {
        /**
         * 需要先加载Ai模块. 在指定范围内检测对象.
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param prob 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测
         * @param iou 用于对多个检测框进行合并. 越大越不容易合并(很多框重叠). 越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间.
         * @returns 返回的是所有检测到的对象.格式是"类名,置信度,x,y,w,h|....". 如果没检测到任何对象,返回空字符串.
         */
        AiYoloDetectObjects(x1: number, y1: number, x2: number, y2: number, prob: number, iou: number): string;

        /**
         * 需要先加载Ai模块. 在指定范围内检测对象,把结果输出到BMP图像数据.用于二次开发.
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param prob 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测
         * @param iou 用于对多个检测框进行合并. 越大越不容易合并(很多框重叠). 越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间.
         * @param data 返回图片的数据指针
         * @param size 返回图片的数据长度
         * @param mode 0表示绘制的文字信息里包含置信度. 1表示不包含.
         * @returns 0:失败 1:成功
         */
        AiYoloDetectObjectsToDataBmp(x1: number, y1: number, x2: number, y2: number, prob: number, iou: number, data: number, size: number, mode: number): number;

        /**
         * 需要先加载Ai模块. 在指定范围内检测对象,把结果输出到指定的BMP文件.
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param prob 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测
         * @param iou 用于对多个检测框进行合并. 越大越不容易合并(很多框重叠). 越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间.
         * @param file 图片名,比如"test.bmp"
         * @param mode 0表示绘制的文字信息里包含置信度. 1表示不包含.
         * @returns 0:失败 1:成功
         */
        AiYoloDetectObjectsToFile(x1: number, y1: number, x2: number, y2: number, prob: number, iou: number, file: string, mode: number): number;

        /**
         * 需要先加载Ai模块. 卸载指定的模型
         * @param index 模型的序号. 最多支持20个. 从0开始
         * @returns 1:成功 0:失败
         */
        AiYoloFreeModel(index: number): number;

        /**
         * 需要先加载Ai模块. 把通过AiYoloDetectObjects或者是AiYoloSortsObjects的结果,按照顺序把class信息连接输出.
         * @param objects AiYoloDetectObjects或者AiYoloSortsObjects的返回值
         * @returns 返回的是class信息连接后的信息
         */
        AiYoloObjectsToString(objects: string): string;

        /**
         * 需要先加载Ai模块. 从文件加载指定的模型.
         * @param index 模型的序号. 最多支持20个. 从0开始
         * @param file 模型文件名. 比如"xxxx.onnx"或者"xxxx.dmx"
         * @param pwd 模型的密码. 仅对dmx格式有效.
         * @returns 1:成功 0:失败
         */
        AiYoloSetModel(index: number, file: string, pwd: string): number;

        /**
         * 需要先加载Ai模块. 从内存加载指定的模型. 仅支持dmx格式的内存
         * @param index 模型的序号. 最多支持20个. 从0开始
         * @param data dmx模型的内存地址
         * @param size dmx模型的大小
         * @param pwd dmx模型的密码
         * @returns 1:成功 0:失败
         */
        AiYoloSetModelMemory(index: number, data: number, size: number, pwd: string): number;

        /**
         * 需要先加载Ai模块. 设置Yolo的版本
         * @param ver Yolo的版本信息. 需要在加载Ai模块后,第一时间调用. 目前可选的值只有"v5-7.0"
         * @returns 1:成功 0:失败
         */
        AiYoloSetVersion(ver: string): number;

        /**
         * 需要先加载Ai模块. 把通过AiYoloDetectObjects的结果进行排序. 排序按照从上到下,从左到右.
         * @param objects AiYoloDetectObjects的返回值
         * @param height 行高信息. 排序时需要使用此行高. 用于确定两个检测框是否处于同一行. 如果两个框的Y坐标相差绝对值小于此行高,认为是同一行.
         * @returns 返回的是所有检测到的对象.格式是"类名,置信度,x,y,w,h|....". 如果没检测到任何对象,返回空字符串.
         */
        AiYoloSortsObjects(objects: string, height?: number): string;

        /**
         * 需要先加载Ai模块. 切换当前使用的模型序号.用于AiYoloDetectXX等系列接口.
         * @param index 模型的序号. 最多支持20个. 从0开始
         * @returns 1:成功 0:失败
         */
        AiYoloUseModel(index: number): number;

        /**
         * 加载Ai模块. Ai模块从后台下载. 模块加载仅支持所有的正式版本。具体可以看DmGuard里系统版本的说明.
         * @param file ai模块的路径. 比如绝对路径c:\\ai.module或者相对路径ai.module等.
         * @returns 1:成功 -1:打开文件失败 -2:内存初始化失败 -3:参数错误 -4:加载错误 -5:Ai模块初始化失败 -6:内存分配失败
         */
        LoadAi(file: string): number;

        /**
         * 从内存加载Ai模块. Ai模块从后台下载. 模块加载仅支持所有的正式版本。具体可以看DmGuard里系统版本的说明.
         * @param data ai模块在内存中的地址
         * @param size ai模块在内存中的大小
         * @returns 1:成功 -1:打开文件失败 -2:内存初始化失败 -3:参数错误 -4:加载错误 -5:Ai模块初始化失败 -6:内存分配失败
         */
        LoadAiMemory(data: number, size: number): number;

        /**
         * 设置是否在调用AiFindPicXX系列接口时,是否弹出找图结果的窗口. 方便调试. 默认是关闭的.
         * @param enable 0:关闭 1:开启
         * @returns 0:失败 1:成功
         */
        AiEnableFindPicWindow(enable: number): number;

        // 中文别名
        /** Yolo对象检测 */
        Yolo对象检测(x1: number, y1: number, x2: number, y2: number, prob: number, iou: number): string;
        /** Yolo对象检测到BMP数据 */
        Yolo对象检测到BMP数据(x1: number, y1: number, x2: number, y2: number, prob: number, iou: number, data: number, size: number, mode: number): number;
        /** Yolo对象检测到BMP文件 */
        Yolo对象检测到BMP文件(x1: number, y1: number, x2: number, y2: number, prob: number, iou: number, file: string, mode: number): number;
        /** Yolo释放模型 */
        Yolo释放模型(index: number): number;
        /** Yolo对象转字符串 */
        Yolo对象转字符串(objects: string): string;
        /** Yolo设置模型 */
        Yolo设置模型(index: number, file: string, pwd: string): number;
        /** Yolo从内存设置模型 */
        Yolo从内存设置模型(index: number, data: number, size: number, pwd: string): number;
        /** Yolo设置版本 */
        Yolo设置版本(ver: string): number;
        /** Yolo对象排序 */
        Yolo对象排序(objects: string, height?: number): string;
        /** Yolo使用模型 */
        Yolo使用模型(index: number): number;
        /** 加载AI */
        加载AI(file: string): number;
        /** 从内存加载AI */
        从内存加载AI(data: number, size: number): number;
        /** AI启用找图窗口 */
        AI启用找图窗口(enable: number): number;

        /**
         * 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
         * 这个函数可以查找多个图片,只返回第一个找到的X Y坐标.
         * 此接口使用Ai模块来实现,比传统的FindPic的效果更好. 不需要训练
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @param intX 返回图片左上角的X坐标
         * @param intY 返回图片左上角的Y坐标
         * @returns 找到的图片序号(从0开始索引),没找到返回-1
         */
        AiFindPic(x1: number, y1: number, x2: number, y2: number, pic_name: string, sim: number, dir: number, intX?: number, intY?: number): number;

        /**
         * 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
         * 这个函数可以查找多个图片,并且返回所有找到的图像的坐标.
         * 此接口使用Ai模块来实现,比传统的FindPicEx的效果更好.不需要训练
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_name 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        AiFindPicEx(x1: number, y1: number, x2: number, y2: number, pic_name: string, sim: number, dir: number): string;

        /**
         * 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
         * 这个函数可以查找多个图片,只返回第一个找到的X Y坐标. 这个函数要求图片是数据地址.
         * 此接口使用Ai模块来实现,比传统的FindPicMem的效果更好.不需要训练
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @param intX 返回图片左上角的X坐标
         * @param intY 返回图片左上角的Y坐标
         * @returns 找到的图片序号(从0开始索引),没找到返回-1
         */
        AiFindPicMem(x1: number, y1: number, x2: number, y2: number, pic_info: string, sim: number, dir: number, intX?: number, intY?: number): number;

        /**
         * 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
         * 这个函数可以查找多个图片,并且返回所有找到的图像的坐标. 这个函数要求图片是数据地址.
         * 此接口使用Ai模块来实现,比传统的FindPicMemEx的效果更好.不需要训练
         * @param x1 区域的左上X坐标
         * @param y1 区域的左上Y坐标
         * @param x2 区域的右下X坐标
         * @param y2 区域的右下Y坐标
         * @param pic_info 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
         * @param sim 相似度,取值范围0.1-1.0
         * @param dir 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
         * @returns 返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
         */
        AiFindPicMemEx(x1: number, y1: number, x2: number, y2: number, pic_info: string, sim: number, dir: number): string;

        // 中文别名
        /** AI找图 */
        AI找图(x1: number, y1: number, x2: number, y2: number, pic_name: string, sim: number, dir: number, intX?: number, intY?: number): number;
        /** AI找图Ex */
        AI找图Ex(x1: number, y1: number, x2: number, y2: number, pic_name: string, sim: number, dir: number): string;
        /** AI找图内存 */
        AI找图内存(x1: number, y1: number, x2: number, y2: number, pic_info: string, sim: number, dir: number, intX?: number, intY?: number): number;
        /** AI找图内存Ex */
        AI找图内存Ex(x1: number, y1: number, x2: number, y2: number, pic_info: string, sim: number, dir: number): string;
    }

    export interface DmFaq {
        /**
         * 可以把上次FaqPost的发送取消,接着下一次FaqPost
         * @returns 0:失败 1:成功
         */
        FaqCancel(): number;

        /**
         * 截取指定范围内的动画或者图像,并返回此句柄
         * @param x1 左上角X坐标
         * @param y1 左上角Y坐标
         * @param x2 右下角X坐标
         * @param y2 右下角Y坐标
         * @param quality 图像或动画品质,取值范围(1-100或者250) 当此值为250时,会截取无损bmp图像数据
         * @param delay 截取动画时用,表示相隔两帧间的时间间隔,单位毫秒 (如果只是截取静态图像,这个参数必须是0)
         * @param time 表示总共截取多久的动画,单位毫秒 (如果只是截取静态图像,这个参数必须是0)
         * @returns 图像或者动画句柄
         */
        FaqCapture(x1: number, y1: number, x2: number, y2: number, quality: number, delay: number, time: number): number;

        /**
         * 截取指定图片中的图像,并返回此句柄
         * @param x1 左上角X坐标
         * @param y1 左上角Y坐标
         * @param x2 右下角X坐标
         * @param y2 右下角Y坐标
         * @param file 图片文件名,图像格式基本都支持
         * @param quality 图像品质,取值范围(1-100或者250) 当此值为250时,会截取无损bmp图像数据
         * @returns 图像句柄
         */
        FaqCaptureFromFile(x1: number, y1: number, x2: number, y2: number, file: string, quality: number): number;

        /**
         * 从给定的字符串获取此句柄 (此接口必须配合答题器v30以后的版本)
         * @param str 文字类型的问题
         * @returns 文字句柄
         */
        FaqCaptureString(str: string): number;

        /**
         * 获取由FaqPost发送后,由服务器返回的答案
         * @returns 如果此函数调用失败,返回"Error:错误描述"
         * 如果函数调用成功,返回"OK:答案"
         * 根据FaqPost中 request_type取值的不同,返回值不同:
         * 0: 答案格式为"x,y"
         * 1: 答案格式为"1" "2" "3" "4" "5" "6"
         * 2: 答案就是要求的答案如"李白"
         * 3: 答案格式为"x1,y1|..|xn,yn"
         * 如果返回空字符串,表示FaqPost还未处理完毕,或者没有调用过FaqPost
         */
        FaqFetch(): string;

        /**
         * 获取句柄所对应的数据包的大小,单位是字节
         * @param handle 由FaqCapture返回的句柄
         * @returns 数据包大小
         */
        FaqGetSize(handle: number): number;

        /**
         * 用于判断当前对象是否有发送过答题(FaqPost)
         * @returns 0:没有 1:有发送过
         */
        FaqIsPosted(): number;

        /**
         * 发送指定的图像句柄到指定的服务器,并立即返回(异步操作)
         * @param server 服务器地址以及端口,格式为(ip:port),例如"192.168.1.100:12345"
         * @param handle 由FaqCapture获取到的句柄
         * @param request_type 取值定义如下:
         * 0: 要求获取坐标
         * 1: 要求获取选项,比如(ABCDE)
         * 2: 要求获取文字答案
         * 3: 要求获取N个坐标
         * @param time_out 表示等待多久,单位是毫秒
         * @returns 0:失败 1:成功
         */
        FaqPost(server: string, handle: number, request_type: number, time_out: number): number;

        /**
         * 发送指定的图像句柄到指定的服务器,并等待返回结果(同步等待)
         * @param server 服务器地址以及端口,格式为(ip:port),例如"192.168.1.100:12345"
         * @param handle 由FaqCapture获取到的句柄
         * @param request_type 取值定义如下:
         * 0: 要求获取坐标
         * 1: 要求获取选项,比如(ABCDE)
         * 2: 要求获取文字答案
         * 3: 要求获取N个坐标
         * @param time_out 表示等待多久,单位是毫秒
         * @returns 如果此函数调用失败,返回"Error:错误描述"
         * 如果函数调用成功,返回"OK:答案"
         * 根据request_type取值的不同,返回值不同:
         * 0: 答案格式为"x,y"
         * 1: 答案格式为"1" "2" "3" "4" "5" "6"
         * 2: 答案就是要求的答案如"李白"
         * 3: 答案格式为"x1,y1|..|xn,yn"
         */
        FaqSend(server: string, handle: number, request_type: number, time_out: number): string;

        // 中文别名
        取消答题: () => number;
        截取动画: (x1: number, y1: number, x2: number, y2: number, quality: number, delay: number, time: number) => number;
        从文件截取图像: (x1: number, y1: number, x2: number, y2: number, file: string, quality: number) => number;
        获取文字句柄: (str: string) => number;
        获取答题结果: () => string;
        获取数据包大小: (handle: number) => number;
        是否已发送答题: () => number;
        发送答题: (server: string, handle: number, request_type: number, time_out: number) => number;
        同步发送答题: (server: string, handle: number, request_type: number, time_out: number) => string;
    }

    export interface DmDmg {
        /**
         * 针对部分检测措施的保护盾
         * @param enable 0表示关闭保护盾 1表示打开保护盾
         * @param type_str 保护盾类型,可以是以下值:
         * - ★"np": 防止NP检测(已过时,不建议使用)
         * - ★"memory": 保护内存系列接口和汇编接口(需加载驱动)
         * - ★"memory2": 同memory(需加载驱动)
         * - "memory3 pid addr_start addr_end": 保护指定PID的内存访问
         * - "memory4"/"memory5"/"memory6": 其他内存保护模式
         * - "phide [pid]": 隐藏和保护指定进程
         * - ★"display2": 极端反截图保护
         * - ★"display3 <hwnd>": 保护指定窗口不被截图
         * - ★"block [pid]": 保护进程不被非法访问
         * - 更多类型请参考文档
         * @returns 0:不支持的类型 1:成功 负数:各种错误码
         */
        DmGuard(enable: number, type_str: string): number;

        /**
         * 释放插件用的驱动,可以自己拿去签名
         * @param type_str 需要释放的驱动类型,这里写"common"即可
         * @param path 释放出的驱动文件全路径,比如"c:\\test.sys"
         * @returns 0:不支持的type 1:成功 -2:释放失败
         */
        DmGuardExtract(type_str: string, path: string): number;

        /**
         * 加载用DmGuardExtract释放出的驱动
         * @param type_str 需要释放的驱动类型,这里写"common"即可
         * @param path 驱动文件全路径,比如"c:\\test.sys"
         * @returns 返回值同DmGuard
         */
        DmGuardLoadCustom(type_str: string, path: string): number;

        /**
         * DmGuard的加强接口,用于获取一些额外信息
         * @param cmd 盾类型,取值为"gr"或"th"
         * @param subcmd 针对具体的盾类型,需要获取的具体信息
         * @param param 参数信息
         * @returns 根据不同的cmd和subcmd,返回值不同
         */
        DmGuardParams(cmd: string, subcmd: string, param: string): string;

        /**
         * 卸载插件相关的所有驱动,仅对64位系统的驱动生效
         * @returns 0:失败 1:成功
         */
        UnLoadDriver(): number;

        // 中文别名
        /** 针对部分检测措施的保护盾 */
        开启防护盾: (enable: number, type_str: string) => number;
        /** 释放插件用的驱动 */
        释放驱动: (type_str: string, path: string) => number;
        /** 加载自定义驱动 */
        加载自定义驱动: (type_str: string, path: string) => number;
        /** DmGuard的加强接口 */
        获取防护盾参数: (cmd: string, subcmd: string, param: string) => string;
        /** 卸载插件相关的所有驱动 */
        卸载驱动: () => number;
    }

    export interface DmBg {
        /**
         * 绑定指定的窗口,并指定这个窗口的屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式,以及模式设定
         * @param hwnd 指定的窗口句柄
         * @param display 屏幕颜色获取方式,取值有:
         * - "normal": 正常模式,前台截屏
         * - "gdi": gdi模式,用于GDI窗口
         * - "gdi2": gdi2模式,兼容性较强但较慢
         * - "dx2": dx2模式,用于dx窗口
         * - "dx3": dx3模式,dx2的兼容性增强版
         * - "dx": dx模式,等同于BindWindowEx的dx.graphic.2d|dx.graphic.3d
         * @param mouse 鼠标仿真模式,取值有:
         * - "normal": 正常前台模式
         * - "windows": Windows模式,模拟消息
         * - "windows2": Windows2模式,锁定鼠标位置
         * - "windows3": Windows3模式,支持多子窗口
         * - "dx": dx模式,后台锁定鼠标
         * - "dx2": dx2模式,后台不锁定鼠标
         * @param keypad 键盘仿真模式,取值有:
         * - "normal": 正常前台模式
         * - "windows": Windows模式,模拟消息
         * - "dx": dx模式,后台键盘模式
         * @param mode 模式,取值有:
         * - 0: 推荐模式,通用性好
         * - 2: 同模式0,兼容性模式
         * - 101: 超级绑定模式,可隐藏DLL
         * - 103: 同模式101,兼容性模式
         * - 11: 需要驱动,用于特殊窗口(不支持32位)
         * - 13: 同模式11,兼容性模式
         * @returns 0:失败 1:成功
         */
        BindWindow(hwnd: number, display: string, mouse: string, keypad: string, mode: number): number;

        /**
         * 解除绑定窗口,并释放系统资源
         * @returns 0:失败 1:成功
         */
        UnBindWindow(): number;

        /**
         * 绑定指定的窗口(增强版)
         * @param hwnd 指定的窗口句柄
         * @param display 屏幕颜色获取方式,支持dx模式的详细参数
         * @param mouse 鼠标仿真模式,支持dx模式的详细参数
         * @param keypad 键盘仿真模式,支持dx模式的详细参数
         * @param public 公共属性,可以为空,支持详细的dx参数
         * @param mode 模式同BindWindow
         * @returns 0:失败 1:成功
         */
        BindWindowEx(hwnd: number, display: string, mouse: string, keypad: string, public: string, mode: number): number;

        /**
         * 在不解绑的情况下,切换绑定窗口(必须是同进程窗口)
         * @param hwnd 需要切换过去的窗口句柄
         * @returns 0:失败 1:成功
         */
        SwitchBindWindow(hwnd: number): number;

        /**
         * 设置当前对象用于输入的对象,结合图色对象和键鼠对象,用一个对象完成操作
         * @param dm_id 接口GetId的返回值
         * @param rx 两个对象绑定的窗口的左上角坐标的x偏移,一般是0
         * @param ry 两个对象绑定的窗口的左上角坐标的y偏移,一般是0
         * @returns 0:失败 1:成功
         */
        SetInputDm(dm_id: number, rx: number, ry: number): number;

        // 中文别名
        /** 绑定指定的窗口 */
        绑定窗口: (hwnd: number, display: string, mouse: string, keypad: string, mode: number) => number;
        /** 解除绑定窗口 */
        解除绑定窗口: () => number;
        /** 绑定指定的窗口(增强版) */
        绑定窗口EX: (hwnd: number, display: string, mouse: string, keypad: string, public: string, mode: number) => number;
        /** 切换绑定窗口 */
        切换绑定窗口: (hwnd: number) => number;
        /** 设置输入对象 */
        设置输入对象: (dm_id: number, rx: number, ry: number) => number;

        /**
         * 设置图色检测的延时,默认是0,当图色检测太频繁时(或者在虚拟机下),如果CPU占用过高,可以设置此参数,把图色检测的频率降低
         * @param delay 延时值,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetDisplayDelay(delay: number): number;

        /**
         * 设置opengl图色检测的最长等待时间,在每次检测图色之前,会等待窗口刷新,如果超过此时间,那么就不等待,直接进行图色检测
         * @param delay 等待刷新的时间,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetDisplayRefreshDelay(delay: number): number;

        // 中文别名
        /** 设置图色延时 */
        设置图色延时: (delay: number) => number;
        /** 设置刷新延时 */
        设置刷新延时: (delay: number) => number;

        /**
         * 获取当前绑定的窗口句柄
         * @returns 返回绑定的窗口句柄,如果没有绑定,则返回0
         */
        GetBindWindow(): number;

        /**
         * 判断当前对象是否已经绑定窗口
         * @returns 0: 未绑定 1: 已绑定
         */
        IsBind(): number;

        /**
         * 获取当前绑定窗口的FPS(刷新频率)
         * @returns 返回FPS值
         */
        GetFps(): number;

        // 中文别名
        /** 获取绑定窗口 */
        获取绑定窗口: () => number;
        /** 是否绑定 */
        是否绑定: () => number;
        /** 获取刷新频率 */
        获取刷新频率: () => number;

        /**
         * 开启图色调试模式,此模式会稍许降低图色速度,但是在调试时可以方便看到图色区域
         * @param enable 0: 关闭调试模式 1: 开启调试模式
         * @returns 0:失败 1:成功
         */
        EnableDisplayDebug(enable: number): number;

        /**
         * 设置是否对后台窗口的图色数据进行更新,如果关闭可以省CPU
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableFakeActive(enable: number): number;

        /**
         * 设置是否开启真实鼠标,如果开启,那么所有鼠标相关的操作都会使用真实鼠标进行
         * @param enable 0: 关闭 1: 开启
         * @param delay 操作延时,单位是毫秒
         * @param step 操作步长
         * @returns 0:失败 1:成功
         */
        EnableRealMouse(enable: number, delay?: number, step?: number): number;

        /**
         * 设置是否开启真实键盘,如果开启,那么所有键盘相关的操作都会使用真实键盘进行
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableRealKeypad(enable: number): number;

        // 中文别名
        /** 开启图色调试 */
        开启图色调试: (enable: number) => number;
        /** 开启后台更新 */
        开启后台更新: (enable: number) => number;
        /** 开启真实鼠标 */
        开启真实鼠标: (enable: number, delay?: number, step?: number) => number;
        /** 开启真实键盘 */
        开启真实键盘: (enable: number) => number;

        /**
         * 设置是否开启按键消息,如果开启,那么插件在按键时会向系统发送按键消息
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableKeypadMsg(enable: number): number;

        /**
         * 设置是否开启按键同步,如果开启,那么所有按键相关的操作都会等待按键结束后才返回
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableKeypadSync(enable: number): number;

        /**
         * 设置是否开启鼠标消息,如果开启,那么插件在鼠标点击时会向系统发送鼠标消息
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableMouseMsg(enable: number): number;

        /**
         * 设置是否开启鼠标同步,如果开启,那么所有鼠标相关的操作都会等待鼠标结束后才返回
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableMouseSync(enable: number): number;

        // 中文别名
        /** 开启按键消息 */
        开启按键消息: (enable: number) => number;
        /** 开启按键同步 */
        开启按键同步: (enable: number) => number;
        /** 开启鼠标消息 */
        开启鼠标消息: (enable: number) => number;
        /** 开启鼠标同步 */
        开启鼠标同步: (enable: number) => number;

        /**
         * 设置是否开启速度模式,如果开启,则所有操作都会以最快速度执行,但是可能会引起一些不稳定
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableSpeedDx(enable: number): number;

        /**
         * 锁定系统的输入,可以防止外部输入干扰,注意在锁定后需要解锁,否则会造成系统输入无法恢复
         * @param lock 0: 解锁 1: 锁定
         * @returns 0:失败 1:成功
         */
        LockInput(lock: number): number;

        /**
         * 设置是否关闭系统的Aero效果,可以提高图色的速度
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        SetAero(enable: number): number;

        /**
         * 设置是否显示错误信息,如果不显示,则所有操作都不会弹出错误提示
         * @param show 0: 不显示 1: 显示
         * @returns 0:失败 1:成功
         */
        SetShowErrorMsg(show: number): number;

        // 中文别名
        /** 开启速度模式 */
        开启速度模式: (enable: number) => number;
        /** 锁定输入 */
        锁定输入: (lock: number) => number;
        /** 设置Aero */
        设置Aero: (enable: number) => number;
        /** 设置错误提示 */
        设置错误提示: (show: number) => number;

        /**
         * 设置图色检测时,需要排除的行数,避免干扰项目
         * @param min_row_gap 设置的行数
         * @returns 0:失败 1:成功
         */
        SetMinRowGap(min_row_gap: number): number;

        /**
         * 设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔
         * @param type_id 鼠标操作类型
         * - "normal" : 对应normal鼠标模式
         * - "windows": 对应windows鼠标模式
         * - "dx" : 对应dx鼠标模式
         * @param delay 延时,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetMouseDelay(type_id: string, delay: number): number;

        /**
         * 设置键盘按键按下和弹起的时间间隔
         * @param type_id 键盘操作类型
         * - "normal" : 对应normal键盘模式
         * - "windows": 对应windows键盘模式
         * - "dx" : 对应dx键盘模式
         * @param delay 延时,单位是毫秒
         * @returns 0:失败 1:成功
         */
        SetKeypadDelay(type_id: string, delay: number): number;

        /**
         * 设置仿真模式,可以减少CPU占用,但是可能会降低图色速度
         * @param mode 0: 关闭仿真 1: 开启仿真
         * @returns 0:失败 1:成功
         */
        SetSimMode(mode: number): number;

        // 中文别名
        /** 设置最小行距 */
        设置最小行距: (min_row_gap: number) => number;
        /** 设置鼠标延时 */
        设置鼠标延时: (type_id: string, delay: number) => number;
        /** 设置按键延时 */
        设置按键延时: (type_id: string, delay: number) => number;
        /** 设置仿真模式 */
        设置仿真模式: (mode: number) => number;

        /**
         * 设置是否开启按键补丁,用于解决某些情况下按键无效的问题
         * @param enable 0: 关闭 1: 开启
         * @returns 0:失败 1:成功
         */
        EnableKeypadPatch(enable: number): number;

        // 中文别名
        /** 开启按键补丁 */
        开启按键补丁: (enable: number) => number;
    }

    export interface DmAsm {
        /**
         * 添加指定的MASM汇编指令
         * @param asm_ins MASM汇编指令,如"mov eax,1"
         * @returns 0: 失败 1: 成功
         */
        AsmAdd(asm_ins: string): number;

        /**
         * 执行用AsmAdd加到缓冲中的指令
         * @param hwnd 窗口句柄
         * @param mode 执行模式
         * - 0: 在本进程中执行(创建线程)
         * - 1: 在目标进程中执行(创建远程线程)
         * - 2: 在目标进程中执行(需要先注入)
         * - 3: 在目标窗口线程中执行(不创建线程)
         * - 4: 在当前线程中执行
         * - 5: 在目标进程中执行(APC方式,需要开启memory盾)
         * - 6: 在目标窗口线程中执行
         * @returns EAX/RAX的值,-200表示执行出错,-201表示未开启memory盾
         */
        AsmCall(hwnd: number, mode: number): number;

        /**
         * 执行用AsmAdd加到缓冲中的指令(指定内存地址)
         * @param hwnd 窗口句柄
         * @param mode 执行模式(同AsmCall)
         * @param base_addr 指定的内存地址(16进制字符串)
         * @returns EAX/RAX的值,-200表示执行出错,-201表示未开启memory盾
         */
        AsmCallEx(hwnd: number, mode: number, base_addr: string): number;

        /**
         * 清除汇编指令缓冲区
         * @returns 0: 失败 1: 成功
         */
        AsmClear(): number;

        /**
         * 设置AsmCall的超时参数
         * @param time_out 超时时间(毫秒),-1表示无限等待
         * @param param 模式6的执行间隔(毫秒)
         * @returns 0: 失败 1: 成功
         */
        AsmSetTimeout(time_out: number, param: number): number;

        /**
         * 把汇编指令转换为机器码
         * @param base_addr 第一条指令的地址
         * @param is_64bit 是否64位指令(0:32位 1:64位)
         * @returns 机器码字符串(如"aa bb cc")
         */
        Assemble(base_addr: number, is_64bit: number): string;

        /**
         * 把机器码转换为汇编指令
         * @param asm_code 机器码字符串(如"aa bb cc")
         * @param base_addr 指令所在地址
         * @param is_64bit 是否64位指令(0:32位 1:64位)
         * @returns 汇编指令字符串(多条指令用|分隔)
         */
        DisAssemble(asm_code: string, base_addr: number, is_64bit: number): string;

        /**
         * 设置是否显示汇编错误提示
         * @param show 0:不显示 1:显示
         * @returns 0: 失败 1: 成功
         */
        SetShowAsmErrorMsg(show: number): number;

        // 中文别名
        /** 添加汇编指令 */
        添加汇编指令: (asm_ins: string) => number;
        /** 执行汇编指令 */
        执行汇编指令: (hwnd: number, mode: number) => number;
        /** 执行汇编指令Ex */
        执行汇编指令Ex: (hwnd: number, mode: number, base_addr: string) => number;
        /** 清空汇编指令 */
        清空汇编指令: () => number;
        /** 设置汇编超时 */
        设置汇编超时: (time_out: number, param: number) => number;
        /** 汇编转机器码 */
        汇编转机器码: (base_addr: number, is_64bit: number) => string;
        /** 机器码转汇编 */
        机器码转汇编: (asm_code: string, base_addr: number, is_64bit: number) => string;
        /** 设置显示汇编错误 */
        设置显示汇编错误: (show: number) => number;
    }
}

declare global {
    interface Window {
        pywebview: {
            api: {
                /** 大漠插件对象 */
                dm: DmSoftType.DmSoft;
            }
        }
    }
}

export = DmSoftType;
export as namespace DmSoftType; 