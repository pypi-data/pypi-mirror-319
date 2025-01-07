#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件鼠标模块API封装
用于鼠标操作相关的功能
'''

class DmMouse:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 获取鼠标位置(self) -> tuple:
        """
        函数简介:
            获取鼠标位置。
        
        函数原型:
            long GetCursorPos(long x, long y)
        
        参数定义:
            无参数
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        
        示例:
            ret, x, y = dm.mouse.获取鼠标位置()
            if ret == 1:
                print(f"鼠标位置:({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取鼠标位置: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.GetCursorPos()
        except Exception as e:
            print(f"Error in 获取鼠标位置: {str(e)}")
            return 0, 0, 0

    def 获取鼠标指向(self, x: int, y: int) -> int:
        """
        函数简介:
            获取指定坐标点的颜色。
            注意,此函数获取的是真实的RGB值,如果需要获取游戏窗口内的颜色,请用GetColor函数。
        
        函数原型:
            long GetMousePointWindow(long x, long y)
        
        参数定义:
            x 整形数: X坐标
            y 整形数: Y坐标
        
        返回值:
            整形数: 返回坐标所在的窗口句柄
        
        示例:
            hwnd = dm.mouse.获取鼠标指向(100, 200)
            print(f"坐标所在窗口句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取鼠标指向: {msg}")
            return 0
            
        try:
            return self._dm.GetMousePointWindow(x, y)
        except Exception as e:
            print(f"Error in 获取鼠标指向: {str(e)}")
            return 0

    def 左键单击(self, x: int = None, y: int = None) -> int:
        """
        函数简介:
            按下鼠标左键。
            如果提供了坐标参数,会先移动到目标位置再点击。
        
        函数原型:
            long LeftClick()
        
        参数定义:
            x 整形数: 可选参数,X坐标
            y 整形数: 可选参数,Y坐标
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            # 在当前位置点击
            ret = dm.mouse.左键单击()
            # 移动到指定位置点击
            ret = dm.mouse.左键单击(100, 200)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 左键单击: {msg}")
            return 0
            
        try:
            if x is not None and y is not None:
                self._dm.MoveTo(x, y)
            return self._dm.LeftClick()
        except Exception as e:
            print(f"Error in 左键单击: {str(e)}")
            return 0

    def 左键按下(self) -> int:
        """
        函数简介:
            按住鼠标左键不放。
        
        函数原型:
            long LeftDown()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.左键按下()
            if ret == 1:
                print("按下鼠标左键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 左键按下: {msg}")
            return 0
            
        try:
            return self._dm.LeftDown()
        except Exception as e:
            print(f"Error in 左键按下: {str(e)}")
            return 0

    def 左键弹起(self) -> int:
        """
        函数简介:
            弹起鼠标左键。
        
        函数原型:
            long LeftUp()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.左键弹起()
            if ret == 1:
                print("弹起鼠标左键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 左键弹起: {msg}")
            return 0
            
        try:
            return self._dm.LeftUp()
        except Exception as e:
            print(f"Error in 左键弹起: {str(e)}")
            return 0

    def 中键单击(self) -> int:
        """
        函数简介:
            按下鼠标中键。
        
        函数原型:
            long MiddleClick()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.中键单击()
            if ret == 1:
                print("点击鼠标中键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 中键单击: {msg}")
            return 0
            
        try:
            return self._dm.MiddleClick()
        except Exception as e:
            print(f"Error in 中键单击: {str(e)}")
            return 0

    def 中键按下(self) -> int:
        """
        函数简介:
            按住鼠标中键不放。
        
        函数原型:
            long MiddleDown()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.中键按下()
            if ret == 1:
                print("按下鼠标中键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 中键按下: {msg}")
            return 0
            
        try:
            return self._dm.MiddleDown()
        except Exception as e:
            print(f"Error in 中键按下: {str(e)}")
            return 0

    def 中键弹起(self) -> int:
        """
        函数简介:
            弹起鼠标中键。
        
        函数原型:
            long MiddleUp()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.中键弹起()
            if ret == 1:
                print("弹起鼠标中键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 中键弹起: {msg}")
            return 0
            
        try:
            return self._dm.MiddleUp()
        except Exception as e:
            print(f"Error in 中键弹起: {str(e)}")
            return 0

    def 移动到(self, x: int, y: int) -> int:
        """
        函数简介:
            把鼠标移动到目的点(x,y)。
        
        函数原型:
            long MoveTo(long x, long y)
        
        参数定义:
            x 整形数: X坐标
            y 整形数: Y坐标
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.移动到(100, 200)
            if ret == 1:
                print("移动鼠标到指定位置")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 移动到: {msg}")
            return 0
            
        try:
            return self._dm.MoveTo(x, y)
        except Exception as e:
            print(f"Error in 移动到: {str(e)}")
            return 0

    def 右键单击(self) -> int:
        """
        函数简介:
            按下鼠标右键。
        
        函数原型:
            long RightClick()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.右键单击()
            if ret == 1:
                print("点击鼠标右键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 右键单击: {msg}")
            return 0
            
        try:
            return self._dm.RightClick()
        except Exception as e:
            print(f"Error in 右键单击: {str(e)}")
            return 0

    def 右键按下(self) -> int:
        """
        函数简介:
            按住鼠标右键不放。
        
        函数原型:
            long RightDown()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.右键按下()
            if ret == 1:
                print("按下鼠标右键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 右键按下: {msg}")
            return 0
            
        try:
            return self._dm.RightDown()
        except Exception as e:
            print(f"Error in 右键按下: {str(e)}")
            return 0

    def 右键弹起(self) -> int:
        """
        函数简介:
            弹起鼠标右键。
        
        函数原型:
            long RightUp()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.mouse.右键弹起()
            if ret == 1:
                print("弹起鼠标右键")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 右键弹起: {msg}")
            return 0
            
        try:
            return self._dm.RightUp()
        except Exception as e:
            print(f"Error in 右键弹起: {str(e)}")
            return 0

    def 滚轮(self, 滚动量: int) -> int:
        """
        函数简介:
            滚动鼠标滚轮。
        
        函数原型:
            long WheelDown()
            long WheelUp()
        
        参数定义:
            滚动量 整形数: 正数表示向上滚动,负数表示向下滚动,数值表示滚动次数
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            # 向上滚动3次
            ret = dm.mouse.滚轮(3)
            # 向下滚动2次
            ret = dm.mouse.滚轮(-2)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 滚轮: {msg}")
            return 0
            
        try:
            if 滚动量 > 0:
                for _ in range(滚动量):
                    ret = self._dm.WheelUp()
                    if ret == 0:
                        return 0
            else:
                for _ in range(-滚动量):
                    ret = self._dm.WheelDown()
                    if ret == 0:
                        return 0
            return 1
        except Exception as e:
            print(f"Error in 滚轮: {str(e)}")
            return 0

    # 添加英文别名
    def GetCursorPos(self, *args, **kwargs):
        """英文别名，调用获取鼠标位置"""
        return self.获取鼠标位置(*args, **kwargs)

    def GetMousePointWindow(self, *args, **kwargs):
        """英文别名，调用获取鼠标指向"""
        return self.获取鼠标指向(*args, **kwargs)

    def LeftClick(self, *args, **kwargs):
        """英文别名，调用左键单击"""
        return self.左键单击(*args, **kwargs)

    def LeftDown(self, *args, **kwargs):
        """英文别名，调用左键按下"""
        return self.左键按下(*args, **kwargs)

    def LeftUp(self, *args, **kwargs):
        """英文别名，调用左键弹起"""
        return self.左键弹起(*args, **kwargs)

    def MiddleClick(self, *args, **kwargs):
        """英文别名，调用中键单击"""
        return self.中键单击(*args, **kwargs)

    def MiddleDown(self, *args, **kwargs):
        """英文别名，调用中键按下"""
        return self.中键按下(*args, **kwargs)

    def MiddleUp(self, *args, **kwargs):
        """英文别名，调用中键弹起"""
        return self.中键弹起(*args, **kwargs)

    def MoveTo(self, *args, **kwargs):
        """英文别名，调用移动到"""
        return self.移动到(*args, **kwargs)

    def RightClick(self, *args, **kwargs):
        """英文别名，调用右键单击"""
        return self.右键单击(*args, **kwargs)

    def RightDown(self, *args, **kwargs):
        """英文别名，调用右键按下"""
        return self.右键按下(*args, **kwargs)

    def RightUp(self, *args, **kwargs):
        """英文别名，调用右键弹起"""
        return self.右键弹起(*args, **kwargs)

    def WheelDown(self, *args, **kwargs):
        """英文别名，调用滚轮向下"""
        return self.滚轮(-1)

    def WheelUp(self, *args, **kwargs):
        """英文别名，调用滚轮向上"""
        return self.滚轮(1)