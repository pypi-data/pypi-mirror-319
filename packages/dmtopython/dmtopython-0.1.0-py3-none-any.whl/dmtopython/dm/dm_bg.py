#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件后台模块API封装
用于后台功能相关的操作
'''

class DmBg:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 绑定窗口(self, 窗口句柄: int) -> int:
        """
        函数简介:
            绑定指定的窗口,并将其后台化。
        
        函数原型:
            long BindWindow(hwnd)
        
        参数定义:
            窗口句柄 整形数: 指定的窗口句柄
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.绑定窗口(hwnd)
            if ret == 1:
                print("窗口绑定成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 绑定窗口: {msg}")
            return 0
            
        try:
            return self._dm.BindWindow(窗口句柄)
        except Exception as e:
            print(f"Error in 绑定窗口: {str(e)}")
            return 0

    def 绑定窗口Ex(self, 窗口句柄: int, 显示: str, 鼠标: str, 键盘: str, 模式: int) -> int:
        """
        函数简介:
            绑定指定的窗口,并指定这个窗口的屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式,以及模式设定。
        
        函数原型:
            long BindWindowEx(hwnd,display,mouse,keypad,mode)
        
        参数定义:
            窗口句柄 整形数: 指定的窗口句柄
            显示 字符串: 屏幕颜色获取方式 取值有以下几种:
                       "normal" : 正常模式,平常我们用的前台截屏模式
                       "gdi" : gdi模式,用于窗口采用GDI方式刷新时. 此模式占用CPU较大.
                       "gdi2" : gdi2模式,此模式兼容性较强,但是速度比gdi模式要慢许多,如果gdi模式发现后台不刷新时,可以考虑用gdi2模式.
                       "dx2" : dx2模式,用于窗口采用dx模式刷新,如果dx方式会出现窗口所在进程崩溃的状况,可以考虑采用这种.采用这种方式要保证窗口有一部分在屏幕外.win7或者vista不需要移动也可后台.此模式占用CPU较大.
                       "dx3" : dx3模式,同dx2模式,但是如果发现有些窗口后台不刷新时,可以考虑用dx3模式,此模式比dx2模式慢许多. 此模式占用CPU较大.
            鼠标 字符串: 鼠标仿真模式 取值有以下几种:
                       "normal" : 正常模式,平常我们用的前台鼠标模式
                       "windows": Windows模式,采取模拟windows消息方式 同按键自带后台插件
                       "windows2": Windows2 模式,采取模拟windows消息方式(锁定鼠标位置) 此模式等同于BindWindow中的mouse为以下组合
                       "windows3": Windows3模式，采取模拟windows消息方式(锁定鼠标位置)
                       "dx": dx模式,采用模拟dx后台鼠标模式,这种方式会锁定鼠标输入.有些窗口在此模式下绑定时，需要先激活窗口再绑定(或者绑定以后激活)，否则可能会出现绑定后鼠标无效的情况.
                       "dx2": dx2模式,同dx模式,但是不会锁定外部鼠标输入. 有些窗口在此模式下绑定时，需要先激活窗口再绑定(或者绑定以后激活)，否则可能会出现绑定后鼠标无效的情况.
            键盘 字符串: 键盘仿真模式 取值有以下几种:
                       "normal" : 正常模式,平常我们用的前台键盘模式
                       "windows": Windows模式,采取模拟windows消息方式 同按键的后台插件
                       "dx": dx模式,采用模拟dx后台键盘模式。有些窗口在此模式下绑定时，需要先激活窗口再绑定(或者绑定以后激活)，否则可能会出现绑定后键盘无效的情况.
            模式 整形数: 模式设定,取值定义如下:
                       0 : 推荐模式此模式比较通用，而且后台效果是最好的.
                       2 : 同模式0,但是如果模式0会失败时，可以尝试此模式.
                       4 : 同模式0,但是如果模式0会失败时，可以尝试此模式.
                       8 : 同模式0,但是如果模式0会失败时，可以尝试此模式.
                       16 : 同模式0,但是如果模式0会失败时，可以尝试此模式.
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            # 使用dx模式绑定窗口
            ret = dm.bg.绑定窗口Ex(hwnd, "dx2", "dx", "dx", 0)
            if ret == 1:
                print("窗口绑定成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 绑定窗口Ex: {msg}")
            return 0
            
        try:
            return self._dm.BindWindowEx(窗口句柄, 显示, 鼠标, 键盘, 模式)
        except Exception as e:
            print(f"Error in 绑定窗口Ex: {str(e)}")
            return 0

    def 解除绑定(self) -> int:
        """
        函数简介:
            解除绑定窗口,并恢复到前台模式。
        
        函数原型:
            long UnBindWindow()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.解除绑定()
            if ret == 1:
                print("解除绑定成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 解除绑定: {msg}")
            return 0
            
        try:
            return self._dm.UnBindWindow()
        except Exception as e:
            print(f"Error in 解除绑定: {str(e)}")
            return 0

    # 添加英文别名
    def BindWindow(self, *args, **kwargs):
        """英文别名，调用绑定窗口"""
        return self.绑定窗口(*args, **kwargs)

    def BindWindowEx(self, *args, **kwargs):
        """英文别名，调用绑定窗口Ex"""
        return self.绑定窗口Ex(*args, **kwargs)

    def UnBindWindow(self, *args, **kwargs):
        """英文别名，调用解除绑定"""
        return self.解除绑定(*args, **kwargs)

    def CPU优化(self, 优化级别: int) -> int:
        """
        函数简介:
            降低目标进程CPU占用。
        
        函数原型:
            long DownCpu(rate)
        
        参数定义:
            优化级别 整形数: 取值范围0到100   
                           0 表示关闭CPU优化
                           100 表示最大优化力度
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.CPU优化(50)  # 设置中等CPU优化
            if ret == 1:
                print("CPU优化设置成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in CPU优化: {msg}")
            return 0
            
        try:
            return self._dm.DownCpu(优化级别)
        except Exception as e:
            print(f"Error in CPU优化: {str(e)}")
            return 0

    def 启用绑定(self, 启用: int) -> int:
        """
        函数简介:
            设置是否允许绑定窗口。
        
        函数原型:
            long EnableBind(enable)
        
        参数定义:
            启用 整形数: 0: 禁止 1: 允许
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用绑定(1)
            if ret == 1:
                print("启用绑定成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用绑定: {msg}")
            return 0
            
        try:
            return self._dm.EnableBind(启用)
        except Exception as e:
            print(f"Error in 启用绑定: {str(e)}")
            return 0

    def 启用假激活(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台假激活功能。
        
        函数原型:
            long EnableFakeActive(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用假激活(1)
            if ret == 1:
                print("启用假激活成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用假激活: {msg}")
            return 0
            
        try:
            return self._dm.EnableFakeActive(启用)
        except Exception as e:
            print(f"Error in 启用假激活: {str(e)}")
            return 0

    def 启用输入法(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台输入法功能。
        
        函数原型:
            long EnableIme(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用输入法(1)
            if ret == 1:
                print("启用输入法成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用输入法: {msg}")
            return 0
            
        try:
            return self._dm.EnableIme(启用)
        except Exception as e:
            print(f"Error in 启用输入法: {str(e)}")
            return 0

    def 启用按键消息(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台按键消息。
        
        函数原型:
            long EnableKeypadMsg(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用按键消息(1)
            if ret == 1:
                print("启用按键消息成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用按键消息: {msg}")
            return 0
            
        try:
            return self._dm.EnableKeypadMsg(启用)
        except Exception as e:
            print(f"Error in 启用按键消息: {str(e)}")
            return 0

    def 启用按键补丁(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台按键补丁。
        
        函数原型:
            long EnableKeypadPatch(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用按键补丁(1)
            if ret == 1:
                print("启用按键补丁成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用按键补丁: {msg}")
            return 0
            
        try:
            return self._dm.EnableKeypadPatch(启用)
        except Exception as e:
            print(f"Error in 启用按键补丁: {str(e)}")
            return 0

    def 启用按键同步(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台按键同步功能。
        
        函数原型:
            long EnableKeypadSync(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用按键同步(1)
            if ret == 1:
                print("启用按键同步成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用按键同步: {msg}")
            return 0
            
        try:
            return self._dm.EnableKeypadSync(启用)
        except Exception as e:
            print(f"Error in 启用按键同步: {str(e)}")
            return 0

    def 启用鼠标消息(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台鼠标消息。
        
        函数原型:
            long EnableMouseMsg(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用鼠标消息(1)
            if ret == 1:
                print("启用鼠标消息成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用鼠标消息: {msg}")
            return 0
            
        try:
            return self._dm.EnableMouseMsg(启用)
        except Exception as e:
            print(f"Error in 启用鼠标消息: {str(e)}")
            return 0

    def 启用鼠标同步(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台鼠标同步功能。
        
        函数原型:
            long EnableMouseSync(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用鼠标同步(1)
            if ret == 1:
                print("启用鼠标同步成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用鼠标同步: {msg}")
            return 0
            
        try:
            return self._dm.EnableMouseSync(启用)
        except Exception as e:
            print(f"Error in 启用鼠标同步: {str(e)}")
            return 0

    def 启用真实按键(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台真实按键功能。
        
        函数原型:
            long EnableRealKeypad(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用真实按键(1)
            if ret == 1:
                print("启用真实按键成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用真实按键: {msg}")
            return 0
            
        try:
            return self._dm.EnableRealKeypad(启用)
        except Exception as e:
            print(f"Error in 启用真实按键: {str(e)}")
            return 0

    def 启用真实鼠标(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台真实鼠标功能。
        
        函数原型:
            long EnableRealMouse(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用真实鼠标(1)
            if ret == 1:
                print("启用真实鼠标成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用真实鼠标: {msg}")
            return 0
            
        try:
            return self._dm.EnableRealMouse(启用)
        except Exception as e:
            print(f"Error in 启用真实鼠标: {str(e)}")
            return 0

    def 启用速度DX(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启后台DX速度优化功能。
        
        函数原型:
            long EnableSpeedDx(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.启用速度DX(1)
            if ret == 1:
                print("启用速度DX成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用速度DX: {msg}")
            return 0
            
        try:
            return self._dm.EnableSpeedDx(启用)
        except Exception as e:
            print(f"Error in 启用速度DX: {str(e)}")
            return 0

    def 强制解除绑定(self) -> int:
        """
        函数简介:
            强制解除绑定窗口,并恢复到前台模式。
        
        函数原型:
            long ForceUnBindWindow()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.强制解除绑定()
            if ret == 1:
                print("强制解除绑定成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 强制解除绑定: {msg}")
            return 0
            
        try:
            return self._dm.ForceUnBindWindow()
        except Exception as e:
            print(f"Error in 强制解除绑定: {str(e)}")
            return 0

    def 获取绑定窗口(self) -> int:
        """
        函数简介:
            获取当前绑定的窗口句柄。
        
        函数原型:
            long GetBindWindow()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 返回绑定的窗口句柄,没有绑定返回0
        
        示例:
            hwnd = dm.bg.获取绑定窗口()
            if hwnd > 0:
                print(f"当前绑定窗口句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取绑定窗口: {msg}")
            return 0
            
        try:
            return self._dm.GetBindWindow()
        except Exception as e:
            print(f"Error in 获取绑定窗口: {str(e)}")
            return 0

    def 设置速度(self, 速度: int) -> int:
        """
        函数简介:
            设置当前系统的速度倍率。
        
        函数原型:
            long HackSpeed(rate)
        
        参数定义:
            速度 整形数: 取值范围大于0,一般最大为100,表示当前速度是原来的rate倍
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.设置速度(2)  # 设置2倍速
            if ret == 1:
                print("设置速度成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置速度: {msg}")
            return 0
            
        try:
            return self._dm.HackSpeed(速度)
        except Exception as e:
            print(f"Error in 设置速度: {str(e)}")
            return 0

    def 是否绑定(self) -> int:
        """
        函数简介:
            判断指定窗口是否已经被绑定。
        
        函数原型:
            long IsBind(hwnd)
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 没绑定 1: 已经绑定
        
        示例:
            if dm.bg.是否绑定():
                print("窗口已绑定")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 是否绑定: {msg}")
            return 0
            
        try:
            return self._dm.IsBind()
        except Exception as e:
            print(f"Error in 是否绑定: {str(e)}")
            return 0

    def 锁定输入(self, 锁定: int) -> int:
        """
        函数简介:
            锁定/解锁系统输入,不影响后台绑定窗口。
        
        函数原型:
            long LockInput(lock)
        
        参数定义:
            锁定 整形数: 0: 解锁 1: 锁定
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.锁定输入(1)
            if ret == 1:
                print("锁定输入成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 锁定输入: {msg}")
            return 0
            
        try:
            return self._dm.LockInput(锁定)
        except Exception as e:
            print(f"Error in 锁定输入: {str(e)}")
            return 0

    def 锁定鼠标区域(self, 左上角x: int, 左上角y: int, 右下角x: int, 右下角y: int) -> int:
        """
        函数简介:
            锁定/解锁系统鼠标移动范围。
        
        函数原型:
            long LockMouseRect(x1, y1, x2, y2)
        
        参数定义:
            左上角x 整形数: 区域的左上角X坐标
            左上角y 整形数: 区域的左上角Y坐标
            右下角x 整形数: 区域的右下角X坐标
            右下角y 整形数: 区域的右下角Y坐标
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.锁定鼠标区域(0, 0, 800, 600)
            if ret == 1:
                print("锁定鼠标区域成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 锁定鼠标区域: {msg}")
            return 0
            
        try:
            return self._dm.LockMouseRect(左上角x, 左上角y, 右下角x, 右下角y)
        except Exception as e:
            print(f"Error in 锁定鼠标区域: {str(e)}")
            return 0

    def 设置显示延迟(self, 延迟: int) -> int:
        """
        函数简介:
            设置图色获取时,是否开启精确模式,并指定精确度。
        
        函数原型:
            long SetDisplayDelay(delay)
        
        参数定义:
            延迟 整形数: 设置图色获取时的延迟,单位是毫秒
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.设置显示延迟(100)
            if ret == 1:
                print("设置显示延迟成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置显示延迟: {msg}")
            return 0
            
        try:
            return self._dm.SetDisplayDelay(延迟)
        except Exception as e:
            print(f"Error in 设置显示延迟: {str(e)}")
            return 0

    def 设置输入设备(self, 设备: str) -> int:
        """
        函数简介:
            设置当前使用的图色输入设备。
        
        函数原型:
            long SetInputDm(input)
        
        参数定义:
            设备 字符串: 图色输入设备,取值有以下几种:
                       "mouse" : 鼠标
                       "keyboard" : 键盘
                       "dx" : dx模式
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.设置输入设备("dx")
            if ret == 1:
                print("设置输入设备成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置输入设备: {msg}")
            return 0
            
        try:
            return self._dm.SetInputDm(设备)
        except Exception as e:
            print(f"Error in 设置输入设备: {str(e)}")
            return 0

    def 设置鼠标延迟(self, 延迟类型: str, 延迟: int) -> int:
        """
        函数简介:
            设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔。
        
        函数原型:
            long SetMouseDelay(type,delay)
        
        参数定义:
            延迟类型 字符串: 鼠标延迟类型
                           "normal" : 正常点击延迟
                           "dx" : dx模式点击延迟
            延迟 整形数: 延迟时间,单位是毫秒
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.设置鼠标延迟("normal", 100)
            if ret == 1:
                print("设置鼠标延迟成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置鼠标延迟: {msg}")
            return 0
            
        try:
            return self._dm.SetMouseDelay(延迟类型, 延迟)
        except Exception as e:
            print(f"Error in 设置鼠标延迟: {str(e)}")
            return 0

    def 设置图片密码(self, 密码: str) -> int:
        """
        函数简介:
            设置图片密码,如果图片本身没有加密,那么此函数无效。
        
        函数原型:
            long SetPicPwd(pwd)
        
        参数定义:
            密码 字符串: 图片密码
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.bg.设置图片密码("123456")
            if ret == 1:
                print("设置图片密码成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置图片密码: {msg}")
            return 0
            
        try:
            return self._dm.SetPicPwd(密码)
        except Exception as e:
            print(f"Error in 设置图片密码: {str(e)}")
            return 0

    # 添加英文别名
    def DownCpu(self, *args, **kwargs):
        """英文别名，调用CPU优化"""
        return self.CPU优化(*args, **kwargs)

    def EnableBind(self, *args, **kwargs):
        """英文别名，调用启用绑定"""
        return self.启用绑定(*args, **kwargs)

    def EnableFakeActive(self, *args, **kwargs):
        """英文别名，调用启用假激活"""
        return self.启用假激活(*args, **kwargs)

    def EnableIme(self, *args, **kwargs):
        """英文别名，调用启用输入法"""
        return self.启用输入法(*args, **kwargs)

    def EnableKeypadMsg(self, *args, **kwargs):
        """英文别名，调用启用按键消息"""
        return self.启用按键消息(*args, **kwargs)

    def EnableKeypadPatch(self, *args, **kwargs):
        """英文别名，调用启用按键补丁"""
        return self.启用按键补丁(*args, **kwargs)

    def EnableKeypadSync(self, *args, **kwargs):
        """英文别名，调用启用按键同步"""
        return self.启用按键同步(*args, **kwargs)

    def EnableMouseMsg(self, *args, **kwargs):
        """英文别名，调用启用鼠标消息"""
        return self.启用鼠标消息(*args, **kwargs)

    def EnableMouseSync(self, *args, **kwargs):
        """英文别名，调用启用鼠标同步"""
        return self.启用鼠标同步(*args, **kwargs)

    def EnableRealKeypad(self, *args, **kwargs):
        """英文别名，调用启用真实按键"""
        return self.启用真实按键(*args, **kwargs)

    def EnableRealMouse(self, *args, **kwargs):
        """英文别名，调用启用真实鼠标"""
        return self.启用真实鼠标(*args, **kwargs)

    def EnableSpeedDx(self, *args, **kwargs):
        """英文别名，调用启用速度DX"""
        return self.启用速度DX(*args, **kwargs)

    def ForceUnBindWindow(self, *args, **kwargs):
        """英文别名，调用强制解除绑定"""
        return self.强制解除绑定(*args, **kwargs)

    def GetBindWindow(self, *args, **kwargs):
        """英文别名，调用获取绑定窗口"""
        return self.获取绑定窗口(*args, **kwargs)

    def HackSpeed(self, *args, **kwargs):
        """英文别名，调用设置速度"""
        return self.设置速度(*args, **kwargs)

    def IsBind(self, *args, **kwargs):
        """英文别名，调用是否绑定"""
        return self.是否绑定(*args, **kwargs)

    def LockInput(self, *args, **kwargs):
        """英文别名，调用锁定输入"""
        return self.锁定输入(*args, **kwargs)

    def LockMouseRect(self, *args, **kwargs):
        """英文别名，调用锁定鼠标区域"""
        return self.锁定鼠标区域(*args, **kwargs)

    def SetDisplayDelay(self, *args, **kwargs):
        """英文别名，调用设置显示延迟"""
        return self.设置显示延迟(*args, **kwargs)

    def SetInputDm(self, *args, **kwargs):
        """英文别名，调用设置输入设备"""
        return self.设置输入设备(*args, **kwargs)

    def SetMouseDelay(self, *args, **kwargs):
        """英文别名，调用设置鼠标延迟"""
        return self.设置鼠标延迟(*args, **kwargs)

    def SetPicPwd(self, *args, **kwargs):
        """英文别名，调用设置图片密码"""
        return self.设置图片密码(*args, **kwargs)

    # ... 继续添加其他函数 ... 