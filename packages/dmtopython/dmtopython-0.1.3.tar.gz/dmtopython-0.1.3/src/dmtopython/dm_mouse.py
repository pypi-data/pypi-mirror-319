import win32com.client

class DmMouse:
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
                
    def EnableMouseAccuracy(self, enable):
        """函数简介:
        设置当前系统鼠标的精确度开关. 如果所示。 此接口仅仅对前台MoveR接口起作用.
        
        函数原型:
        long EnableMouseAccuracy(enable)
        
        参数定义:
        enable整形数: 0 关闭指针精确度开关. 1打开指针精确度开关. 一般推荐关闭.
        
        返回值:
        整形数:
        设置之前的精确度开关. 
        
        示例:
        dm.SetMouseAccuracy 0
        """
        return self._dm.EnableMouseAccuracy(enable)
    
    def GetCursorPos(self):
        """函数简介:
        获取鼠标位置.
        
        函数原型:
        long GetCursorPos(x,y)
        
        参数定义:
        x 变参指针: 返回X坐标
        y 变参指针: 返回Y坐标
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.GetCursorPos x,y
        MessageBox x&","&y
        
        注: 此接口在3.1223版本之后，返回的值的定义修改。 同大多数接口一样,返回的x,y坐标是根据绑定的鼠标参数来决定. 
        如果绑定了窗口，那么获取的坐标是相对于绑定窗口，否则是屏幕坐标.
        另外，此函数获取的坐标是真实的鼠标坐标，对于某些自绘鼠标位置不一定准确。请自行测试.
        """
        return self._dm.GetCursorPos(0, 0)
        
    def GetCursorShape(self):
        """函数简介:
        获取鼠标特征码. 当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，
        获取到的是后台鼠标特征，否则是前台鼠标特征. 关于如何识别后台鼠标特征.
        
        函数原型:
        string GetCursorShape()
        
        参数定义:
        
        返回值:
        字符串:
        成功时，返回鼠标特征码.
        失败时，返回空的串.
        
        示例:
        mouse_tz = dm.GetCursorShape()
        If mouse_tz = "7d7160fe" Then
        MessageBox "找到特征码"
        End If
        
        注:此接口和GetCursorShapeEx(0)等效. 相当于工具里的方式1获取的特征码. 当此特征码在某些情况下无法区分鼠标形状时，
        可以考虑使用GetCursorShapeEx(1).
        另要特别注意,WIN7以及以上系统，必须在字体显示设置里把文字大小调整为默认(100%),否则特征码会变.如图所示.
        """
        return self._dm.GetCursorShape()
        
    def GetCursorShapeEx(self, type):
        """函数简介:
        获取鼠标特征码. 当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，
        获取到的是后台鼠标特征，否则是前台鼠标特征. 关于如何识别后台鼠标特征.
        
        函数原型:
        string GetCursorShapeEx(int type)
        
        参数定义:
        type 整形数:获取鼠标特征码的方式. 和工具中的方式1 方式2对应. 方式1此参数值为0. 方式2此参数值为1.
        
        返回值:
        字符串:
        成功时，返回鼠标特征码.
        失败时，返回空的串.
        
        示例:
        mouse_tz = dm.GetCursorShapeEx(0)
        If mouse_tz = "7d7160fe" Then
        MessageBox "找到特征码"
        End If
        
        注: 当type为0时，和GetCursorShape等效.
        另要特别注意,WIN7以及以上系统，必须在字体显示设置里把文字大小调整为默认(100%),否则特征码会变.如图所示.
        """
        return self._dm.GetCursorShapeEx(type)
        
    def GetCursorSpot(self):
        """函数简介:
        获取鼠标热点位置.(参考工具中抓取鼠标后，那个闪动的点就是热点坐标,不是鼠标坐标)
        当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，
        获取到的是后台鼠标热点位置，否则是前台鼠标热点位置. 关于如何识别后台鼠标特征.
        
        函数原型:
        string GetCursorSpot()
        
        参数定义:
        
        返回值:
        字符串:
        成功时，返回形如"x,y"的字符串
        失败时，返回空的串.
        
        示例:
        hot_pos = dm.GetCursorSpot()
        if len(hot_pos) > 0 Then
        hot_pos = split(hot_pos,",")
        x = int(hot_pos(0))
        y = int(hot_pos(1))
        end if
        """
        return self._dm.GetCursorSpot()
        
    def GetMouseSpeed(self):
        """函数简介:
        获取系统鼠标的移动速度. 如图所示红色区域. 一共分为11个级别. 从1开始,11结束. 这仅是前台鼠标的速度. 后台不用理会这个.
        
        函数原型:
        long GetMouseSpeed()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        其他值,当前系统鼠标的移动速度
        
        示例:
        TracePrint dm.GetMouseSpeed()
        """
        return self._dm.GetMouseSpeed()
        
    def LeftClick(self):
        """函数简介:
        按下鼠标左键
        
        函数原型:
        long LeftClick()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.LeftClick
        """
        return self._dm.LeftClick()
        
    def LeftDoubleClick(self):
        """函数简介:
        双击鼠标左键
        
        函数原型:
        long LeftDoubleClick()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.LeftDoubleClick
        """
        return self._dm.LeftDoubleClick()
        
    def LeftDown(self):
        """函数简介:
        按住鼠标左键
        
        函数原型:
        long LeftDown()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.LeftDown
        """
        return self._dm.LeftDown()
        
    def LeftUp(self):
        """函数简介:
        弹起鼠标左键
        
        函数原型:
        long LeftUp()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.LeftUp
        """
        return self._dm.LeftUp()
        
    def MiddleClick(self):
        """函数简介:
        按下鼠标中键
        
        函数原型:
        long MiddleClick()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.MiddleClick
        """
        return self._dm.MiddleClick()
        
    def MiddleDown(self):
        """函数简介:
        按住鼠标中键
        
        函数原型:
        long MiddleDown()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.MiddleDown
        """
        return self._dm.MiddleDown()
        
    def MiddleUp(self):
        """函数简介:
        弹起鼠标中键
        
        函数原型:
        long MiddleUp()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.MiddleUp
        """
        return self._dm.MiddleUp()
        
    def MoveR(self, rx, ry):
        """函数简介:
        鼠标相对于上次的位置移动rx,ry. 如果您要使前台鼠标移动的距离和指定的rx,ry一致,最好配合EnableMouseAccuracy函数来使用.
        
        函数原型:
        long MoveR(rx,ry)
        
        参数定义:
        rx 整形数:相对于上次的X偏移
        ry 整形数:相对于上次的Y偏移
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.MoveR rx,ry
        
        注: 此函数从6.1550开始，为了兼容某些特殊输入，不再自动设置鼠标的速度和精确度。如果您要使前台鼠标移动的距离和指定的rx,ry一致,
        那么最好配合EnableMouseAccuracy函数来使用
        因为rx和ry的偏移量不一定就是鼠标真实的偏移,而是代表了物理鼠标DPI偏移. 如果您需要这个偏移和真实鼠标偏移一致，那么需要如下调用这个函数，如下所示:
        old_accuracy = dm.EnableMouseAccuracy(0) // 关闭精确度开关
        dm.MoveR 30,30
        dm.EnableMouseAccuracy old_accuracy
        当然你也可以永久关闭精确度开关. 一般来说精确度开关默认都是关闭的.
        以上这些设置都仅对前台有效. 后台是不需要这样设置的.
        """
        return self._dm.MoveR(rx, ry)
        
    def MoveTo(self, x, y):
        """函数简介:
        把鼠标移动到目的点(x,y)
        
        函数原型:
        long MoveTo(x,y)
        
        参数定义:
        x 整形数:X坐标
        y 整形数:Y坐标
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.MoveTo x,y
        """
        return self._dm.MoveTo(x, y)
        
    def MoveToEx(self, x, y, w, h):
        """函数简介:
        把鼠标移动到目的范围内的任意一点
        
        函数原型:
        string MoveToEx(x,y,w,h)
        
        参数定义:
        x 整形数:X坐标
        y 整形数:Y坐标
        w 整形数:宽度(从x计算起)
        h 整形数:高度(从y计算起)
        
        返回值:
        字符串:
        返回要移动到的目标点. 格式为x,y. 比如MoveToEx 100,100,10,10,返回值可能是101,102
        
        示例:
        // 移动鼠标到(100,100)到(110,110)这个矩形范围内的任意一点.
        dm.MoveToEx 100,100,10,10
        
        注: 此函数的意思是移动鼠标到指定的范围(x,y,x+w,y+h)内的任意随机一点.
        """
        return self._dm.MoveToEx(x, y, w, h)
        
    def RightClick(self):
        """函数简介:
        按下鼠标右键
        
        函数原型:
        long RightClick()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.RightClick
        """
        return self._dm.RightClick()
        
    def RightDown(self):
        """函数简介:
        按住鼠标右键
        
        函数原型:
        long RightDown()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.RightDown
        """
        return self._dm.RightDown()
        
    def RightUp(self):
        """函数简介:
        弹起鼠标右键
        
        函数原型:
        long RightUp()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.RightUp
        """
        return self._dm.RightUp()
        
    def SetMouseDelay(self, type, delay):
        """函数简介:
        设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔。高级用户使用。某些窗口可能需要调整这个参数才可以正常点击。
        
        函数原型:
        long SetMouseDelay(type,delay)
        
        参数定义:
        type 字符串: 鼠标类型,取值有以下
        "normal" : 对应normal鼠标 默认内部延时为 30ms
        "windows": 对应windows 鼠标 默认内部延时为 10ms
        "dx" : 对应dx鼠标 默认内部延时为40ms
        delay 整形数: 延时,单位是毫秒
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.SetMouseDelay "dx",10
        
        注 : 此函数影响的接口有LeftClick RightClick MiddleClick LeftDoubleClick
        """
        return self._dm.SetMouseDelay(type, delay)
        
    def SetMouseSpeed(self, speed):
        """函数简介:
        设置系统鼠标的移动速度. 如图所示红色区域. 一共分为11个级别. 从1开始,11结束。此接口仅仅对前台鼠标有效.
        
        函数原型:
        long SetMouseSpeed(speed)
        
        参数定义:
        speed 整形数:鼠标移动速度, 最小1，最大11. 居中为6. 推荐设置为6
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.SetMouseSpeed 6
        """
        return self._dm.SetMouseSpeed(speed)
        
    def WheelDown(self):
        """函数简介:
        滚轮向下滚
        
        函数原型:
        long WheelDown()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.WheelDown
        """
        return self._dm.WheelDown()
        
    def WheelUp(self):
        """函数简介:
        滚轮向上滚
        
        函数原型:
        long WheelUp()
        
        参数定义:
        
        返回值:
        整形数:
        0:失败
        1:成功
        
        示例:
        dm.WheelUp
        """
        return self._dm.WheelUp()
        
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
    启用鼠标精确度 = EnableMouseAccuracy
    获取鼠标位置 = GetCursorPos
    获取鼠标特征码 = GetCursorShape
    获取鼠标特征码EX = GetCursorShapeEx
    获取鼠标热点位置 = GetCursorSpot
    获取鼠标速度 = GetMouseSpeed
    左键单击 = LeftClick
    左键双击 = LeftDoubleClick
    左键按下 = LeftDown
    左键弹起 = LeftUp
    中键单击 = MiddleClick
    中键按下 = MiddleDown
    中键弹起 = MiddleUp
    相对移动 = MoveR
    移动到 = MoveTo
    移动到范围 = MoveToEx
    右键单击 = RightClick
    右键按下 = RightDown
    右键弹起 = RightUp
    设置鼠标延时 = SetMouseDelay
    设置鼠标速度 = SetMouseSpeed
    滚轮向下 = WheelDown
    滚轮向上 = WheelUp
    等待按键 = WaitKey 