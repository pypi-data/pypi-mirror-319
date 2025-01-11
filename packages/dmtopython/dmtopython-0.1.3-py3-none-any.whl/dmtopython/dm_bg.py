import win32com.client

class DmBg:
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

    def BindWindow(self, hwnd: int, display: str, mouse: str, keypad: str, mode: int) -> int:
        """
        函数简介:
            绑定指定的窗口,并指定这个窗口的屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式,以及模式设定
        函数原型:
            long BindWindow(hwnd,display,mouse,keypad,mode)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            display 字符串: 屏幕颜色获取方式,取值有:
                "normal": 正常模式,前台截屏
                "gdi": gdi模式,用于GDI窗口
                "gdi2": gdi2模式,兼容性较强但较慢
                "dx2": dx2模式,用于dx窗口
                "dx3": dx3模式,dx2的兼容性增强版
                "dx": dx模式,等同于BindWindowEx的dx.graphic.2d|dx.graphic.3d
            mouse 字符串: 鼠标仿真模式,取值有:
                "normal": 正常前台模式
                "windows": Windows模式,模拟消息
                "windows2": Windows2模式,锁定鼠标位置
                "windows3": Windows3模式,支持多子窗口
                "dx": dx模式,后台锁定鼠标
                "dx2": dx2模式,后台不锁定鼠标
            keypad 字符串: 键盘仿真模式,取值有:
                "normal": 正常前台模式
                "windows": Windows模式,模拟消息
                "dx": dx模式,后台键盘模式
            mode 整形数: 模式,取值有:
                0: 推荐模式,通用性好
                2: 同模式0,兼容性模式
                101: 超级绑定模式,可隐藏DLL
                103: 同模式101,兼容性模式
                11: 需要驱动,用于特殊窗口(不支持32位)
                13: 同模式11,兼容性模式
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.BindWindow(hwnd, display, mouse, keypad, mode)

    def UnBindWindow(self) -> int:
        """
        函数简介:
            解除绑定窗口,并释放系统资源
        函数原型:
            long UnBindWindow()
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.UnBindWindow()

    def BindWindowEx(self, hwnd: int, display: str, mouse: str, keypad: str, public: str, mode: int) -> int:
        """
        函数简介:
            绑定指定的窗口(增强版)
        函数原型:
            long BindWindowEx(hwnd,display,mouse,keypad,public,mode)
        参数定义:
            hwnd 整形数: 指定的窗口句柄
            display 字符串: 屏幕颜色获取方式,支持dx模式的详细参数
            mouse 字符串: 鼠标仿真模式,支持dx模式的详细参数
            keypad 字符串: 键盘仿真模式,支持dx模式的详细参数
            public 字符串: 公共属性,可以为空,支持详细的dx参数
            mode 整形数: 模式同BindWindow
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.BindWindowEx(hwnd, display, mouse, keypad, public, mode)

    def SwitchBindWindow(self, hwnd: int) -> int:
        """
        函数简介:
            在不解绑的情况下,切换绑定窗口(必须是同进程窗口)
        函数原型:
            long SwitchBindWindow(hwnd)
        参数定义:
            hwnd 整形数: 需要切换过去的窗口句柄
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SwitchBindWindow(hwnd)

    def SetInputDm(self, dm_id: int, rx: int, ry: int) -> int:
        """
        函数简介:
            设置当前对象用于输入的对象,结合图色对象和键鼠对象,用一个对象完成操作
        函数原型:
            long SetInputDm(dm_id,rx,ry)
        参数定义:
            dm_id 整形数: 接口GetId的返回值
            rx 整形数: 两个对象绑定的窗口的左上角坐标的x偏移,一般是0
            ry 整形数: 两个对象绑定的窗口的左上角坐标的y偏移,一般是0
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetInputDm(dm_id, rx, ry)

    def SetDisplayDelay(self, delay: int) -> int:
        """
        函数简介:
            设置图色检测的延时,默认是0,当图色检测太频繁时(或者在虚拟机下),如果CPU占用过高,可以设置此参数,把图色检测的频率降低
        函数原型:
            long SetDisplayDelay(delay)
        参数定义:
            delay 整形数: 延时值,单位是毫秒
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetDisplayDelay(delay)

    def SetDisplayRefreshDelay(self, delay: int) -> int:
        """
        函数简介:
            设置opengl图色检测的最长等待时间,在每次检测图色之前,会等待窗口刷新,如果超过此时间,那么就不等待,直接进行图色检测
        函数原型:
            long SetDisplayRefreshDelay(delay)
        参数定义:
            delay 整形数: 等待刷新的时间,单位是毫秒
        返回值:
            整形数: 0:失败 1:成功
        注: 
            如果图色检测的窗口频繁刷新,那么等待时间设置大一些,可以提高图色检测的准确率,但是会影响图色检测的速度
            如果窗口刷新不频繁,那么等待时间设置小一些,可以提高图色检测的速度,但是可能会影响图色检测的准确率
        """
        return self._dm.SetDisplayRefreshDelay(delay)

    def GetBindWindow(self) -> int:
        """
        函数简介:
            获取当前绑定的窗口句柄
        函数原型:
            long GetBindWindow()
        返回值:
            整形数: 返回绑定的窗口句柄,如果没有绑定,则返回0
        """
        return self._dm.GetBindWindow()

    def IsBind(self) -> int:
        """
        函数简介:
            判断当前对象是否已经绑定窗口
        函数原型:
            long IsBind()
        返回值:
            整形数: 0: 未绑定 1: 已绑定
        """
        return self._dm.IsBind()

    def GetFps(self) -> int:
        """
        函数简介:
            获取当前绑定窗口的FPS(刷新频率)
        函数原型:
            long GetFps()
        返回值:
            整形数: 返回FPS值
        """
        return self._dm.GetFps()

    def EnableDisplayDebug(self, enable: int) -> int:
        """
        函数简介:
            开启图色调试模式,此模式会稍许降低图色速度,但是在调试时可以方便看到图色区域
        函数原型:
            long EnableDisplayDebug(enable)
        参数定义:
            enable 整形数: 0: 关闭调试模式 1: 开启调试模式
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableDisplayDebug(enable)

    def EnableFakeActive(self, enable: int) -> int:
        """
        函数简介:
            设置是否对后台窗口的图色数据进行更新,如果关闭可以省CPU
        函数原型:
            long EnableFakeActive(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableFakeActive(enable)

    def EnableRealMouse(self, enable: int, delay: int = 0, step: int = 0) -> int:
        """
        函数简介:
            设置是否开启真实鼠标,如果开启,那么所有鼠标相关的操作都会使用真实鼠标进行
        函数原型:
            long EnableRealMouse(enable, delay, step)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
            delay 整形数: 操作延时,单位是毫秒
            step 整形数: 操作步长
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableRealMouse(enable, delay, step)

    def EnableRealKeypad(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启真实键盘,如果开启,那么所有键盘相关的操作都会使用真实键盘进行
        函数原型:
            long EnableRealKeypad(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableRealKeypad(enable)

    def EnableKeypadMsg(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启按键消息,如果开启,那么插件在按键时会向系统发送按键消息
        函数原型:
            long EnableKeypadMsg(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableKeypadMsg(enable)

    def EnableKeypadSync(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启按键同步,如果开启,那么所有按键相关的操作都会等待按键结束后才返回
        函数原型:
            long EnableKeypadSync(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableKeypadSync(enable)

    def EnableMouseMsg(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启鼠标消息,如果开启,那么插件在鼠标点击时会向系统发送鼠标消息
        函数原型:
            long EnableMouseMsg(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableMouseMsg(enable)

    def EnableMouseSync(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启鼠标同步,如果开启,那么所有鼠标相关的操作都会等待鼠标结束后才返回
        函数原型:
            long EnableMouseSync(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableMouseSync(enable)

    def EnableSpeedDx(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启速度模式,如果开启,则所有操作都会以最快速度执行,但是可能会引起一些不稳定
        函数原型:
            long EnableSpeedDx(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableSpeedDx(enable)

    def LockInput(self, lock: int) -> int:
        """
        函数简介:
            锁定系统的输入,可以防止外部输入干扰,注意在锁定后需要解锁,否则会造成系统输入无法恢复
        函数原型:
            long LockInput(lock)
        参数定义:
            lock 整形数: 0: 解锁 1: 锁定
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.LockInput(lock)

    def SetAero(self, enable: int) -> int:
        """
        函数简介:
            设置是否关闭系统的Aero效果,可以提高图色的速度
        函数原型:
            long SetAero(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetAero(enable)

    def SetShowErrorMsg(self, show: int) -> int:
        """
        函数简介:
            设置是否显示错误信息,如果不显示,则所有操作都不会弹出错误提示
        函数原型:
            long SetShowErrorMsg(show)
        参数定义:
            show 整形数: 0: 不显示 1: 显示
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetShowErrorMsg(show)

    def SetMinRowGap(self, min_row_gap: int) -> int:
        """
        函数简介:
            设置图色检测时,需要排除的行数,避免干扰项目
        函数原型:
            long SetMinRowGap(min_row_gap)
        参数定义:
            min_row_gap 整形数: 设置的行数
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetMinRowGap(min_row_gap)

    def SetMouseDelay(self, type_id: str, delay: int) -> int:
        """
        函数简介:
            设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔
        函数原型:
            long SetMouseDelay(type_id, delay)
        参数定义:
            type_id 字符串: 鼠标操作类型
                "normal" : 对应normal鼠标模式
                "windows": 对应windows鼠标模式
                "dx" : 对应dx鼠标模式
            delay 整形数: 延时,单位是毫秒
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetMouseDelay(type_id, delay)

    def SetKeypadDelay(self, type_id: str, delay: int) -> int:
        """
        函数简介:
            设置键盘按键按下和弹起的时间间隔
        函数原型:
            long SetKeypadDelay(type_id, delay)
        参数定义:
            type_id 字符串: 键盘操作类型
                "normal" : 对应normal键盘模式
                "windows": 对应windows键盘模式
                "dx" : 对应dx键盘模式
            delay 整形数: 延时,单位是毫秒
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetKeypadDelay(type_id, delay)

    def SetSimMode(self, mode: int) -> int:
        """
        函数简介:
            设置仿真模式,可以减少CPU占用,但是可能会降低图色速度
        函数原型:
            long SetSimMode(mode)
        参数定义:
            mode 整形数: 0: 关闭仿真 1: 开启仿真
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.SetSimMode(mode)

    def EnableKeypadPatch(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启按键补丁,用于解决某些情况下按键无效的问题
        函数原型:
            long EnableKeypadPatch(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 开启
        返回值:
            整形数: 0:失败 1:成功
        """
        return self._dm.EnableKeypadPatch(enable)

    # 中文别名
    绑定窗口 = BindWindow
    解除绑定窗口 = UnBindWindow
    绑定窗口EX = BindWindowEx
    切换绑定窗口 = SwitchBindWindow
    设置输入对象 = SetInputDm
    设置图色延时 = SetDisplayDelay
    设置刷新延时 = SetDisplayRefreshDelay
    获取绑定窗口 = GetBindWindow
    是否绑定 = IsBind
    获取刷新频率 = GetFps
    开启图色调试 = EnableDisplayDebug
    开启后台更新 = EnableFakeActive
    开启真实鼠标 = EnableRealMouse
    开启真实键盘 = EnableRealKeypad
    开启按键消息 = EnableKeypadMsg
    开启按键同步 = EnableKeypadSync
    开启鼠标消息 = EnableMouseMsg
    开启鼠标同步 = EnableMouseSync
    开启速度模式 = EnableSpeedDx
    锁定输入 = LockInput
    设置Aero = SetAero
    设置错误提示 = SetShowErrorMsg
    设置最小行距 = SetMinRowGap
    设置鼠标延时 = SetMouseDelay
    设置按键延时 = SetKeypadDelay
    设置仿真模式 = SetSimMode
    开启按键补丁 = EnableKeypadPatch 