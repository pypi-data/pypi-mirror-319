import win32com.client

class DmKeyboard:
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
                
    def GetKeyState(self, vk_code):
        """函数简介:
        获取指定的按键状态.(前台信息,不是后台)
        
        函数原型:
        long GetKeyState(vk_code)
        
        参数定义:
        vk_code 整形数:虚拟按键码
        
        返回值:
        整形数:
        0:弹起
        1:按下
        
        示例:
        TracePrint dm.GetKeyState(13)
        """
        return self._dm.GetKeyState(vk_code)
        
    def KeyDown(self, vk_code):
        """函数简介:
        按住指定的虚拟键码
        
        函数原型:
        long KeyDown(vk_code)
        
        参数定义:
        vk_code 整形数:虚拟按键码
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyDown 13
        """
        return self._dm.KeyDown(vk_code)
        
    def KeyDownChar(self, key_str):
        """函数简介:
        按住指定的虚拟键码
        
        函数原型:
        long KeyDownChar(key_str)
        
        参数定义:
        key_str 字符串: 字符串描述的键码. 大小写无所谓.
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyDownChar "enter"
        dm.KeyDownChar "1"
        dm.KeyDownChar "F1"
        dm.KeyDownChar "a"
        dm.KeyDownChar "B"
        """
        return self._dm.KeyDownChar(key_str)
        
    def KeyPress(self, vk_code):
        """函数简介:
        按下指定的虚拟键码
        
        函数原型:
        long KeyPress(vk_code)
        
        参数定义:
        vk_code 整形数:虚拟按键码
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyPress 13
        """
        return self._dm.KeyPress(vk_code)
        
    def KeyPressChar(self, key_str):
        """函数简介:
        按下指定的虚拟键码
        
        函数原型:
        long KeyPressChar(key_str)
        
        参数定义:
        key_str 字符串: 字符串描述的键码. 大小写无所谓.
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyPressChar "enter"
        dm.KeyPressChar "1"
        dm.KeyPressChar "F1"
        dm.KeyPressChar "a"
        dm.KeyPressChar "B"
        """
        return self._dm.KeyPressChar(key_str)
        
    def KeyPressStr(self, key_str, delay):
        """函数简介:
        根据指定的字符串序列，依次按顺序按下其中的字符.
        
        函数原型:
        long KeyPressStr(key_str,delay)
        
        参数定义:
        key_str 字符串: 需要按下的字符串序列. 比如"1234","abcd","7389,1462"等.
        delay 整形数: 每按下一个按键，需要延时多久. 单位毫秒.这个值越大，按的速度越慢。
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyPressStr "123,456",20
        
        注: 在某些情况下，SendString和SendString2都无法输入文字时，可以考虑用这个来输入.
        但这个接口只支持标准ASCII可见字符,其它字符一律不支持.(包括中文)
        """
        return self._dm.KeyPressStr(key_str, delay)
        
    def KeyUp(self, vk_code):
        """函数简介:
        弹起来虚拟键vk_code
        
        函数原型:
        long KeyUp(vk_code)
        
        参数定义:
        vk_code 整形数:虚拟按键码
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyUp 13
        """
        return self._dm.KeyUp(vk_code)
        
    def KeyUpChar(self, key_str):
        """函数简介:
        弹起来虚拟键key_str
        
        函数原型:
        long KeyUpChar(key_str)
        
        参数定义:
        key_str 字符串: 字符串描述的键码. 大小写无所谓.
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.KeyUpChar "enter"
        dm.KeyUpChar "1"
        dm.KeyUpChar "F1"
        dm.KeyUpChar "a"
        dm.KeyUpChar "B"
        """
        return self._dm.KeyUpChar(key_str)
        
    def SetKeypadDelay(self, type, delay):
        """函数简介:
        设置按键时,键盘按下和弹起的时间间隔。高级用户使用。某些窗口可能需要调整这个参数才可以正常按键。
        
        函数原型:
        long SetKeypadDelay(type,delay)
        
        参数定义:
        type 字符串: 键盘类型,取值有以下
        "normal" : 对应normal键盘 默认内部延时为30ms
        "windows": 对应windows 键盘 默认内部延时为10ms
        "dx" : 对应dx 键盘 默认内部延时为50ms
        delay 整形数: 延时,单位是毫秒
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.SetKeypadDelay "dx",10
        
        注 : 此函数影响的接口有KeyPress
        """
        return self._dm.SetKeypadDelay(type, delay)
        
    def SetSimMode(self, mode):
        """函数简介:
        设置前台键鼠的模拟方式。
        
        函数原型:
        long SetSimMode(mode)
        
        参数定义:
        mode 整形数: 
        0 正常模式(默认模式)
        1 硬件模拟
        2 硬件模拟2(ps2)
        3 硬件模拟3
        
        返回值:
        整形数:
        0 : 插件没注册
        -1 : 32位系统不支持
        -2 : 驱动释放失败
        -3 : 驱动加载失败
        -10: 设置失败
        -7 : 系统版本不支持
        1 : 成功
        
        示例:
        dm.SetSimMode 1
        """
        return self._dm.SetSimMode(mode)
        
    def WaitKey(self, vk_code, time_out):
        """函数简介:
        等待指定的按键按下 (前台,不是后台)
        
        函数原型:
        long WaitKey(vk_code,time_out)
        
        参数定义:
        vk_code 整形数:虚拟按键码,当此值为0，表示等待任意按键。 鼠标左键是1,鼠标右键时2,鼠标中键是4.
        time_out 整形数:等待多久,单位毫秒. 如果是0，表示一直等待
        
        返回值:
        整形数:
        0:超时
        1:指定的按键按下 (当vk_code不为0时)
        按下的按键码:(当vk_code为0时)
        
        示例:
        dm.WaitKey 66,0
        """
        return self._dm.WaitKey(vk_code, time_out)
        
    # 中文别名
    获取按键状态 = GetKeyState
    按下键码 = KeyDown
    按下键名 = KeyDownChar
    点击键码 = KeyPress
    点击键名 = KeyPressChar
    输入文本 = KeyPressStr
    弹起键码 = KeyUp
    弹起键名 = KeyUpChar
    设置按键延时 = SetKeypadDelay
    设置模拟方式 = SetSimMode
    等待按键 = WaitKey 