#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件键盘模块API封装
'''

class DmKeyboard:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 按键(self, key_code: int) -> int:
        """
        模拟按下指定的虚拟键码

        Args:
            key_code: 按键码

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.按键(65);  // 按下A键
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 按键: {msg}")
            return 0
            
        try:
            return self._dm.KeyPress(key_code)
        except Exception as e:
            print(f"Error in 按键: {str(e)}")
            return 0

    def 按住键(self, key_code: int) -> int:
        """
        按住指定的虚拟键码

        Args:
            key_code: 按键码

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.按住键(65);  // 按住A键
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 按住键: {msg}")
            return 0
            
        try:
            return self._dm.KeyDown(key_code)
        except Exception as e:
            print(f"Error in 按住键: {str(e)}")
            return 0

    def 弹起键(self, key_code: int) -> int:
        """
        弹起指定的虚拟键码

        Args:
            key_code: 按键码

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.弹起键(65);  // 弹起A键
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 弹起键: {msg}")
            return 0
            
        try:
            return self._dm.KeyUp(key_code)
        except Exception as e:
            print(f"Error in 弹起键: {str(e)}")
            return 0

    def 输入文本(self, text: str) -> int:
        """
        向指定窗口输入文本,输入的文本不支持中文

        Args:
            text: 要输入的文本串. 

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.输入文本("hello");
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 输入文本: {msg}")
            return 0
            
        try:
            return self._dm.SendString(text)
        except Exception as e:
            print(f"Error in 输入文本: {str(e)}")
            return 0

    def 组合按键(self, key_str: str) -> int:
        """
        模拟按下指定的组合键。例如"A"表示单键A，"^A"表示组合键Ctrl+A，"~A"表示组合键Alt+A，"%A"表示组合键Shift+A。

        Args:
            key_str: 组合键字符串。例如"A"，"^A"，"~A"，"%A"等. 字母区分大小写

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.组合按键("^A");  // 按下Ctrl+A
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 组合按键: {msg}")
            return 0
        
        try:
            return self._dm.KeyPressChar(key_str)
        except Exception as e:
            print(f"Error in 组合按键: {str(e)}")
            return 0

    def 组合按下(self, key_str: str) -> int:
        """
        模拟按下指定的组合键。例如"A"表示单键A，"^A"表示组合键Ctrl+A，"~A"表示组合键Alt+A，"%A"表示组合键Shift+A。

        Args:
            key_str: 组合键字符串。例如"A"，"^A"，"~A"，"%A"等. 字母区分大小写

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.组合按下("^A");  // 按下Ctrl+A
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 组合按下: {msg}")
            return 0
        
        try:
            return self._dm.KeyDownChar(key_str)
        except Exception as e:
            print(f"Error in 组合按下: {str(e)}")
            return 0

    def 组合弹起(self, key_str: str) -> int:
        """
        模拟弹起指定的组合键。例如"A"表示单键A，"^A"表示组合键Ctrl+A，"~A"表示组合键Alt+A，"%A"表示组合键Shift+A。

        Args:
            key_str: 组合键字符串。例如"A"，"^A"，"~A"，"%A"等. 字母区分大小写

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.组合弹起("^A");  // 弹起Ctrl+A
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 组合弹起: {msg}")
            return 0
        
        try:
            return self._dm.KeyUpChar(key_str)
        except Exception as e:
            print(f"Error in 组合弹起: {str(e)}")
            return 0

    def 设置按键延迟(self, type: int, delay: int) -> int:
        """
        设置按键时,键盘按下和弹起的时间间隔。高级用户使用。

        Args:
            type: 键盘类型,取值有以下几种
                  0 : 正常按键延时
                  1 : 按住按键延时
                  2 : 组合按键延时
            delay: 延时,单位是毫秒

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.设置按键延迟(0, 100);  // 设置正常按键延时为100毫秒
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置按键延迟: {msg}")
            return 0
        
        try:
            return self._dm.SetKeypadDelay(type, delay)
        except Exception as e:
            print(f"Error in 设置按键延迟: {str(e)}")
            return 0

    def 获取按键延迟(self, type: int) -> int:
        """
        获取按键时,键盘按下和弹起的时间间隔。高级用户使用。

        Args:
            type: 键盘类型,取值有以下几种
                  0 : 正常按键延时
                  1 : 按住按键延时
                  2 : 组合按键延时

        Returns:
            int: 延时,单位是毫秒

        示例:
            let delay = window.pywebview.api.dm.keyboard.获取按键延迟(0);  // 获取正常按键延时
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取按键延迟: {msg}")
            return 0
        
        try:
            return self._dm.GetKeypadDelay(type)
        except Exception as e:
            print(f"Error in 获取按键延迟: {str(e)}")
            return 0

    def 设置按键间隔(self, delay: int) -> int:
        """
        设置两个按键之间的时间间隔。高级用户使用。

        Args:
            delay: 延时,单位是毫秒

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.设置按键间隔(100);  // 设置按键间隔为100毫秒
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置按键间隔: {msg}")
            return 0
        
        try:
            return self._dm.SetKeypadDelay2(delay)
        except Exception as e:
            print(f"Error in 设置按键间隔: {str(e)}")
            return 0

    def 获取按键间隔(self) -> int:
        """
        获取两个按键之间的时间间隔。高级用户使用。

        Returns:
            int: 延时,单位是毫秒

        示例:
            let delay = window.pywebview.api.dm.keyboard.获取按键间隔();  // 获取按键间隔
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取按键间隔: {msg}")
            return 0
        
        try:
            return self._dm.GetKeypadDelay2()
        except Exception as e:
            print(f"Error in 获取按键间隔: {str(e)}")
            return 0

    def 获取按键状态(self, vk_code: int) -> int:
        """
        获取指定的按键状态.(前台信息,不是后台)

        Args:
            vk_code: 虚拟按键码

        Returns:
            int: 0: 失败 
                 1: 按下 
                 2: 弹起

        示例:
            let state = window.pywebview.api.dm.keyboard.获取按键状态(65);  // 获取A键的状态
            if(state == 1) {
                console.log("A键处于按下状态");
            } else if(state == 2) {
                console.log("A键处于弹起状态");
            }
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取按键状态: {msg}")
            return 0
        
        try:
            return self._dm.GetKeyState(vk_code)
        except Exception as e:
            print(f"Error in 获取按键状态: {str(e)}")
            return 0

    def 启用真实键盘(self, enable: int) -> int:
        """
        键盘按键使用真实键盘，如果不调用此函数，则默认使用模拟键盘。
        注: 此接口为老的写法，建议使用 EnableRealKeypad

        Args:
            enable: 0: 关闭 1: 开启

        Returns:
            int: 1: 成功 0: 失败

        示例:
            let ret = window.pywebview.api.dm.keyboard.启用真实键盘(1);  // 启用真实键盘
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用真实键盘: {msg}")
            return 0
        
        try:
            return self._dm.EnableRealKeypad(enable)
        except Exception as e:
            print(f"Error in 启用真实键盘: {str(e)}")
            return 0