import win32com.client

class DmWindow:
    def __init__(self, dm:win32com.client.CDispatch=None, code=None, key=None):
        if dm:
            self._dm = dm
        else:
            if not code or not key:
                raise Exception("自注册,code和key不能为空,或者大漠对象不是cdispatch");
            try:
                self._dm = win32com.client.Dispatch('dm.dmsoft')
                self.regstats = self._dm.Reg(code, key)
                if self.regstats == 1:
                    print("大漠注册成功")
                else:
                    self._dm = None
                    raise Exception("注册失败，错误码："+str(self.regstats))
            except Exception as e:
                raise Exception("创建大漠对象失败，错误提示："+str(e))

    def ClientToScreen(self, hwnd, x, y):
        """
        函数简介:
            把窗口坐标转换为屏幕坐标
        函数原型:
            long ClientToScreen(hwnd,x,y)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            x 变参指针: 窗口X坐标
            y 变参指针: 窗口Y坐标
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.ClientToScreen(hwnd, x, y)

    def EnumProcess(self, name):
        """
        函数简介:
            根据指定进程名,枚举系统中符合条件的进程PID,并且按照进程打开顺序排序.
        函数原型:
            string EnumProcess(name)
        参数定义:
            name 字符串: 进程名,比如qq.exe
        返回值:
            字符串: 返回所有匹配的进程PID,并按打开顺序排序,格式"pid1,pid2,pid3"
        """
        return self._dm.EnumProcess(name)

    def EnumWindow(self, parent, title, class_name, filter):
        """
        函数简介:
            根据指定条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口
        函数原型:
            string EnumWindow(parent,title,class_name,filter)
        参数定义:
            parent 整形数: 获得的窗口句柄是该窗口的子窗口的窗口句柄,取0时为获得桌面句柄
            title 字符串: 窗口标题. 此参数是模糊匹配.
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            filter 整形数: 取值定义如下
                1: 匹配窗口标题,参数title有效
                2: 匹配窗口类名,参数class_name有效
                4: 只匹配指定父窗口的第一层孩子窗口
                8: 匹配父窗口为0的窗口,即顶级窗口
                16: 匹配可见的窗口
                32: 匹配出的窗口按照窗口打开顺序依次排列
                这些值可以相加,比如4+8+16就是类似于任务管理器中的窗口列表
        返回值:
            字符串: 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self._dm.EnumWindow(parent, title, class_name, filter)

    def EnumWindowByProcess(self, process_name, title, class_name, filter):
        """
        函数简介:
            根据指定进程以及其它条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口
        函数原型:
            string EnumWindowByProcess(process_name,title,class_name,filter)
        参数定义:
            process_name 字符串: 进程映像名.比如(svchost.exe). 此参数是精确匹配,但不区分大小写.
            title 字符串: 窗口标题. 此参数是模糊匹配.
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            filter 整形数: 取值定义如下
                1: 匹配窗口标题,参数title有效
                2: 匹配窗口类名,参数class_name有效
                4: 只匹配指定映像的所对应的第一个进程
                8: 匹配父窗口为0的窗口,即顶级窗口
                16: 匹配可见的窗口
                32: 匹配出的窗口按照窗口打开顺序依次排列
                这些值可以相加,比如4+8+16
        返回值:
            字符串: 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self._dm.EnumWindowByProcess(process_name, title, class_name, filter)

    def EnumWindowByProcessId(self, pid, title, class_name, filter):
        """
        函数简介:
            根据指定进程pid以及其它条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口
        函数原型:
            string EnumWindowByProcessId(pid,title,class_name,filter)
        参数定义:
            pid 整形数: 进程pid.
            title 字符串: 窗口标题. 此参数是模糊匹配.
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            filter 整形数: 取值定义如下
                1: 匹配窗口标题,参数title有效
                2: 匹配窗口类名,参数class_name有效
                8: 匹配父窗口为0的窗口,即顶级窗口
                16: 匹配可见的窗口
                这些值可以相加,比如2+8+16
        返回值:
            字符串: 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self._dm.EnumWindowByProcessId(pid, title, class_name, filter)

    def EnumWindowSuper(self, spec1, flag1, type1, spec2, flag2, type2, sort):
        """
        函数简介:
            根据两组设定条件来枚举指定窗口.
        函数原型:
            string EnumWindowSuper(spec1,flag1,type1,spec2,flag2,type2,sort)
        参数定义:
            spec1 字符串: 查找串1. (内容取决于flag1的值)
            flag1 整形数: 取值如下:
                0表示spec1的内容是标题
                1表示spec1的内容是程序名字. (比如notepad)
                2表示spec1的内容是类名
                3表示spec1的内容是程序路径.(不包含盘符,比如\\windows\\system32)
                4表示spec1的内容是父句柄.(十进制表达的串)
                5表示spec1的内容是父窗口标题
                6表示spec1的内容是父窗口类名
                7表示spec1的内容是顶级窗口句柄.(十进制表达的串)
                8表示spec1的内容是顶级窗口标题
                9表示spec1的内容是顶级窗口类名
            type1 整形数: 取值如下
                0精确判断
                1模糊判断
            spec2 字符串: 查找串2. (内容取决于flag2的值)
            flag2 整形数: 取值同flag1
            type2 整形数: 取值同type1
            sort 整形数: 取值如下
                0不排序
                1对枚举出的窗口进行排序,按照窗口打开顺序
        返回值:
            字符串: 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self._dm.EnumWindowSuper(spec1, flag1, type1, spec2, flag2, type2, sort)

    def FindWindow(self, class_name, title):
        """
        函数简介:
            查找符合条件的窗口
        函数原型:
            long FindWindow(class_name,title)
        参数定义:
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            title 字符串: 窗口标题. 此参数是模糊匹配.
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        """
        return self._dm.FindWindow(class_name, title)

    def FindWindowByProcess(self, process_name, class_name, title):
        """
        函数简介:
            根据指定进程以及其它条件,查找符合条件的窗口
        函数原型:
            long FindWindowByProcess(process_name,class_name,title)
        参数定义:
            process_name 字符串: 进程映像名. 此参数是精确匹配,但不区分大小写.
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            title 字符串: 窗口标题. 此参数是模糊匹配.
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        """
        return self._dm.FindWindowByProcess(process_name, class_name, title)

    def FindWindowByProcessId(self, process_id, class_name, title):
        """
        函数简介:
            根据指定进程pid以及其它条件,查找符合条件的窗口
        函数原型:
            long FindWindowByProcessId(process_id,class_name,title)
        参数定义:
            process_id 整形数: 进程pid.
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            title 字符串: 窗口标题. 此参数是模糊匹配.
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        """
        return self._dm.FindWindowByProcessId(process_id, class_name, title)

    def SendString(self, hwnd, text):
        """
        函数简介:
            向指定窗口发送文本数据
        函数原型:
            long SendString(hwnd,text)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            text 字符串: 发送的文本数据
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SendString(hwnd, text)

    def SendString2(self, hwnd, text):
        """
        函数简介:
            向指定窗口发送文本数据(另一种模式)
        函数原型:
            long SendString2(hwnd,text)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            text 字符串: 发送的文本数据
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SendString2(hwnd, text)

    def SendStringIme(self, text):
        """
        函数简介:
            向绑定的窗口发送文本数据(使用输入法)
        函数原型:
            long SendStringIme(text)
        参数定义:
            text 字符串: 发送的文本数据
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SendStringIme(text)

    def SendStringIme2(self, hwnd, text, mode):
        """
        函数简介:
            向指定窗口发送文本数据(使用输入法)
        函数原型:
            long SendStringIme2(hwnd,text,mode)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            text 字符串: 发送的文本数据
            mode 整形数: 取值意义如下:
                0: 向hwnd的窗口输入文字(前提是必须先用模式200安装了输入法)
                1: 同模式0,如果由于保护无效，可以尝试此模式.(前提是必须先用模式200安装了输入法)
                2: 同模式0,如果由于保护无效，可以尝试此模式. (前提是必须先用模式200安装了输入法)
                200: 向系统中安装输入法,多次调用没问题. 全局只用安装一次.
                300: 卸载系统中的输入法. 全局只用卸载一次. 多次调用没关系.
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 如果要同时对此窗口进行绑定，并且绑定的模式是1 3 5 7 101 103，那么您必须要在绑定之前,
            先执行加载输入法的操作. 否则会造成绑定失败!.
            卸载时，没有限制.
        """
        return self._dm.SendStringIme2(hwnd, text, mode)

    def SetClientSize(self, hwnd, width, height):
        """
        函数简介:
            设置窗口客户区域的宽度和高度
        函数原型:
            long SetClientSize(hwnd,width,height)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            width 整形数: 宽度
            height 整形数: 高度
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SetClientSize(hwnd, width, height)

    def SetWindowSize(self, hwnd, width, height):
        """
        函数简介:
            设置窗口的大小
        函数原型:
            long SetWindowSize(hwnd,width,height)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            width 整形数: 宽度
            height 整形数: 高度
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SetWindowSize(hwnd, width, height)

    def SetWindowState(self, hwnd, flag):
        """
        函数简介:
            设置窗口的状态
        函数原型:
            long SetWindowState(hwnd,flag)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            flag 整形数: 取值定义如下
                0: 关闭指定窗口
                1: 激活指定窗口
                2: 最小化指定窗口,但不激活
                3: 最小化指定窗口,并释放内存,但同时也会激活窗口
                4: 最大化指定窗口,同时激活窗口
                5: 恢复指定窗口,但不激活
                6: 隐藏指定窗口
                7: 显示指定窗口
                8: 置顶指定窗口
                9: 取消置顶指定窗口
                10: 禁止指定窗口
                11: 取消禁止指定窗口
                12: 恢复并激活指定窗口
                13: 强制结束窗口所在进程
                14: 闪烁指定的窗口
                15: 使指定的窗口获取输入焦点
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SetWindowState(hwnd, flag)

    def SetWindowText(self, hwnd, title):
        """
        函数简介:
            设置窗口的标题
        函数原型:
            long SetWindowText(hwnd,title)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            title 字符串: 标题
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SetWindowText(hwnd, title)

    def SetWindowTransparent(self, hwnd, trans):
        """
        函数简介:
            设置窗口的透明度
        函数原型:
            long SetWindowTransparent(hwnd,trans)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            trans 整形数: 透明度取值(0-255) 越小透明度越大 0为完全透明(不可见) 255为完全显示(不透明)
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 此接口不支持WIN98
        """
        return self._dm.SetWindowTransparent(hwnd, trans)

    def SetSendStringDelay(self, delay):
        """
        函数简介:
            设置SendString和SendString2的每个字符之间的发送间隔. 有些窗口必须设置延迟才可以正常发送. 否则可能会顺序错乱.
        函数原型:
            long SetSendStringDelay(delay)
        参数定义:
            delay 整形数: 大于等于0的延迟数值. 单位是毫秒. 默认是0
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.SetSendStringDelay(delay)

    def ScreenToClient(self, hwnd, x, y):
        """
        函数简介:
            把屏幕坐标转换为窗口坐标
        函数原型:
            long ScreenToClient(hwnd,x,y)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            x 变参指针: 屏幕X坐标
            y 变参指针: 屏幕Y坐标
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.ScreenToClient(hwnd, x, y)

    def GetClientRect(self, hwnd):
        """
        函数简介:
            获取窗口客户区域在屏幕上的位置
        函数原型:
            string GetClientRect(hwnd)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
        返回值:
            字符串: 窗口客户区域在屏幕上的位置,格式为"left,top,right,bottom"
        """
        return self._dm.GetClientRect(hwnd)

    def GetClientSize(self, hwnd):
        """
        函数简介:
            获取窗口客户区域的宽度和高度
        函数原型:
            string GetClientSize(hwnd)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
        返回值:
            字符串: 窗口客户区域的宽度和高度,格式为"width,height"
        """
        return self._dm.GetClientSize(hwnd)

    def GetForegroundFocus(self):
        """
        函数简介:
            获取顶层活动窗口中具有输入焦点的窗口句柄
        函数原型:
            long GetForegroundFocus()
        参数定义:
            无参数
        返回值:
            整形数: 返回整形表示的窗口句柄
        """
        return self._dm.GetForegroundFocus()

    def GetForegroundWindow(self):
        """
        函数简介:
            获取顶层活动窗口
        函数原型:
            long GetForegroundWindow()
        参数定义:
            无参数
        返回值:
            整形数: 返回整形表示的窗口句柄
        """
        return self._dm.GetForegroundWindow()

    def GetMousePointWindow(self):
        """
        函数简介:
            获取鼠标指向的可见窗口句柄
        函数原型:
            long GetMousePointWindow()
        参数定义:
            无参数
        返回值:
            整形数: 返回整形表示的窗口句柄
        """
        return self._dm.GetMousePointWindow()

    def GetProcessInfo(self, pid):
        """
        函数简介:
            根据指定的进程pid获取进程详细信息
        函数原型:
            string GetProcessInfo(pid)
        参数定义:
            pid 整形数: 进程pid
        返回值:
            字符串: 
            格式为:
            "进程名|进程全路径|CPU使用率|内存使用率|打开时间|线程数|父进程ID|父进程名|父进程全路径"
            失败返回空
        """
        return self._dm.GetProcessInfo(pid)

    def GetSpecialWindow(self, flag):
        """
        函数简介:
            获取特殊窗口
        函数原型:
            long GetSpecialWindow(flag)
        参数定义:
            flag 整形数: 取值定义如下
                0 : 获取桌面窗口
                1 : 获取任务栏窗口
        返回值:
            整形数: 以整形数表示的窗口句柄
        """
        return self._dm.GetSpecialWindow(flag)

    def GetWindow(self, hwnd, flag):
        """
        函数简介:
            获取给定窗口相关的窗口句柄
        函数原型:
            long GetWindow(hwnd,flag)
        参数定义:
            hwnd 整形数: 窗口句柄
            flag 整形数: 取值定义如下
                0 : 获取父窗口
                1 : 获取第一个儿子窗口
                2 : 获取First窗口
                3 : 获取Last窗口
                4 : 获取下一个窗口
                5 : 获取上一个窗口
                6 : 获取拥有者窗口
                7 : 获取顶层窗口
        返回值:
            整形数: 返回整形表示的窗口句柄
        """
        return self._dm.GetWindow(hwnd, flag)

    def GetWindowClass(self, hwnd):
        """
        函数简介:
            获取窗口的类名
        函数原型:
            string GetWindowClass(hwnd)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
        返回值:
            字符串: 窗口的类名
        """
        return self._dm.GetWindowClass(hwnd)

    def GetWindowProcessId(self, hwnd):
        """
        函数简介:
            获取指定窗口所在的进程ID
        函数原型:
            long GetWindowProcessId(hwnd)
        参数定义:
            hwnd 整形数: 窗口句柄
        返回值:
            整形数: 返回整形表示的是进程ID
        """
        return self._dm.GetWindowProcessId(hwnd)

    def GetWindowProcessPath(self, hwnd):
        """
        函数简介:
            获取指定窗口所在的进程的exe文件全路径
        函数原型:
            string GetWindowProcessPath(hwnd)
        参数定义:
            hwnd 整形数: 窗口句柄
        返回值:
            字符串: 返回进程所在的文件路径
        """
        return self._dm.GetWindowProcessPath(hwnd)

    def GetWindowRect(self, hwnd):
        """
        函数简介:
            获取窗口在屏幕上的位置
        函数原型:
            string GetWindowRect(hwnd)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
        返回值:
            字符串: 窗口在屏幕上的位置,格式为"left,top,right,bottom"
        """
        return self._dm.GetWindowRect(hwnd)

    def GetWindowState(self, hwnd, flag):
        """
        函数简介:
            获取指定窗口的一些属性
        函数原型:
            long GetWindowState(hwnd,flag)
        参数定义:
            hwnd 整形数: 窗口句柄
            flag 整形数: 取值定义如下
                0 : 判断窗口是否存在
                1 : 判断窗口是否处于激活
                2 : 判断窗口是否可见
                3 : 判断窗口是否最小化
                4 : 判断窗口是否最大化
                5 : 判断窗口是否置顶
                6 : 判断窗口是否无响应
                7 : 判断窗口是否可用(灰色为不可用)
                8 : 判断窗口是否可鼠标穿透
                9 : 判断窗口是否置顶
        返回值:
            整形数:
            0: 不满足条件
            1: 满足条件
        """
        return self._dm.GetWindowState(hwnd, flag)

    def GetWindowTitle(self, hwnd):
        """
        函数简介:
            获取窗口的标题
        函数原型:
            string GetWindowTitle(hwnd)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
        返回值:
            字符串: 窗口的标题
        """
        return self._dm.GetWindowTitle(hwnd)

    def MoveWindow(self, hwnd, x, y):
        """
        函数简介:
            移动指定窗口到指定位置
        函数原型:
            long MoveWindow(hwnd,x,y)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            x 整形数: X坐标
            y 整形数: Y坐标
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.MoveWindow(hwnd, x, y)

    def FindWindowEx(self, parent, class_name, title):
        """
        函数简介:
            在父窗口的第一层子窗口中查找符合类名或者标题名的窗口
        函数原型:
            long FindWindowEx(parent,class_name,title)
        参数定义:
            parent 整形数: 父窗口句柄
            class_name 字符串: 窗口类名. 此参数是模糊匹配.
            title 字符串: 窗口标题. 此参数是模糊匹配.
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        """
        return self._dm.FindWindowEx(parent, class_name, title)

    def SendPaste(self, hwnd):
        """
        函数简介:
            向指定窗口发送粘贴命令. 把剪贴板的内容发送到指定窗口.
        函数原型:
            long SendPaste(hwnd)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 剪贴板是公共资源，多个线程同时设置剪贴板时,会产生冲突，必须用互斥信号保护.
        """
        return self._dm.SendPaste(hwnd)

    # 补充中文别名
    屏幕坐标转窗口坐标 = ScreenToClient
    获取窗口客户区域位置 = GetClientRect
    获取窗口客户区域大小 = GetClientSize
    获取焦点窗口句柄 = GetForegroundFocus
    获取顶层活动窗口 = GetForegroundWindow
    获取鼠标指向窗口 = GetMousePointWindow
    获取进程信息 = GetProcessInfo
    获取特殊窗口 = GetSpecialWindow
    获取相关窗口句柄 = GetWindow
    获取窗口类名 = GetWindowClass
    获取窗口进程ID = GetWindowProcessId
    获取窗口进程路径 = GetWindowProcessPath
    获取窗口位置 = GetWindowRect
    获取窗口状态 = GetWindowState
    获取窗口标题 = GetWindowTitle
    移动窗口 = MoveWindow
    查找子窗口 = FindWindowEx
    发送粘贴 = SendPaste
    枚举进程 = EnumProcess
    枚举窗口 = EnumWindow
    按进程名枚举窗口 = EnumWindowByProcess
    按进程ID枚举窗口 = EnumWindowByProcessId
    超级枚举窗口 = EnumWindowSuper
    查找窗口 = FindWindow
    按进程名查找窗口 = FindWindowByProcess
    按进程ID查找窗口 = FindWindowByProcessId
    发送文本 = SendString
    发送文本2 = SendString2
    发送文本到输入法 = SendStringIme
    发送文本到输入法2 = SendStringIme2
    设置客户区大小 = SetClientSize
    设置窗口大小 = SetWindowSize
    设置窗口状态 = SetWindowState
    设置窗口标题 = SetWindowText
    设置窗口透明度 = SetWindowTransparent
    设置发送文本延迟 = SetSendStringDelay 