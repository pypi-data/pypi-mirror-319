#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件窗口模块API封装
用于窗口操作相关的功能
'''

class DmWindow:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 客户区转屏幕(self, 窗口句柄: int, 窗口x: int, 窗口y: int) -> tuple:
        """
        函数简介:
            把窗口坐标转换为屏幕坐标。
            把窗口客户区坐标转换为屏幕坐标。
        
        函数原型:
            long ClientToScreen(hwnd,x,y,rx,ry)
        
        参数定义:
            窗口句柄 整形数: 指定的窗口句柄
            窗口x 整形数: 窗口X坐标
            窗口y 整形数: 窗口Y坐标
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: 屏幕X坐标, 整形数: 屏幕Y坐标)
        
        示例:
            ret, rx, ry = dm.window.客户区转屏幕(hwnd, 100, 100)
            if ret == 1:
                print(f"屏幕坐标为:({rx}, {ry})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 客户区转屏幕: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.ClientToScreen(窗口句柄, 窗口x, 窗口y)
        except Exception as e:
            print(f"Error in 客户区转屏幕: {str(e)}")
            return 0, 0, 0

    def 枚举进程(self, 进程名: str) -> str:
        """
        函数简介:
            根据进程名枚举进程。
            可以枚举同名进程。
        
        函数原型:
            string EnumProcess(name)
        
        参数定义:
            进程名 字符串: 进程名,比如"notepad.exe"
        
        返回值:
            字符串: 返回所有匹配的进程PID,并按"|"分隔
                   比如"1234|5678|9012"
                   如果没有找到任何进程,返回空字符串
        
        示例:
            pids = dm.window.枚举进程("notepad.exe")
            if pids:
                for pid in pids.split("|"):
                    print(f"找到记事本进程,PID:{pid}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 枚举进程: {msg}")
            return ""
            
        try:
            return self._dm.EnumProcess(进程名)
        except Exception as e:
            print(f"Error in 枚举进程: {str(e)}")
            return ""

    def 枚举窗口(self, 父窗口句柄: int, 标题: str, 类名: str, 过滤: int) -> str:
        """
        函数简介:
            根据指定条件,枚举系统中符合条件的窗口。
            可以枚举多个窗口。
        
        函数原型:
            string EnumWindow(parent,title,class_name,filter)
        
        参数定义:
            父窗口句柄 整形数: 父窗口句柄,如果为0,则匹配所有窗口
            标题 字符串: 窗口标题. 此参数是模糊匹配.
            类名 字符串: 窗口类名. 此参数是模糊匹配.
            过滤 整形数: 取值定义如下:
                       0 : 匹配所有窗口
                       1 : 匹配可见的窗口
                       2 : 匹配最上层的窗口
                       4 : 匹配可激活的窗口
                       8 : 匹配有标题的窗口
                       这些值可以相加,比如6=2+4,表示匹配最上层的并且可激活的窗口
        
        返回值:
            字符串: 返回所有匹配的窗口句柄,并按"|"分隔
                   比如"123|456|789"
                   如果没有找到任何窗口,返回空字符串
        
        示例:
            # 查找所有可见的记事本窗口
            hwnds = dm.window.枚举窗口(0, "记事本", "", 1)
            if hwnds:
                for hwnd in hwnds.split("|"):
                    print(f"找到记事本窗口,句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 枚举窗口: {msg}")
            return ""
            
        try:
            return self._dm.EnumWindow(父窗口句柄, 标题, 类名, 过滤)
        except Exception as e:
            print(f"Error in 枚举窗口: {str(e)}")
            return ""

    def 枚举窗口按进程(self, 进程ID: int) -> str:
        """
        函数简介:
            根据指定进程以及其它条件,枚举系统中符合条件的窗口。
            可以枚举多个窗口。
        
        函数原型:
            string EnumWindowByProcess(process_name,title,class_name,filter)
        
        参数定义:
            进程ID 整形数: 进程ID
        
        返回值:
            字符串: 返回所有匹配的窗口句柄,并按"|"分隔
                   比如"123|456|789"
                   如果没有找到任何窗口,返回空字符串
        
        示例:
            # 查找指定进程的所有窗口
            hwnds = dm.window.枚举窗口按进程(1234)
            if hwnds:
                for hwnd in hwnds.split("|"):
                    print(f"找到窗口,句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 枚举窗口按进程: {msg}")
            return ""
            
        try:
            return self._dm.EnumWindowByProcess(进程ID)
        except Exception as e:
            print(f"Error in 枚举窗口按进程: {str(e)}")
            return ""

    def 查找窗口(self, 类名: str, 标题: str) -> int:
        """
        函数简介:
            查找符合类名或者标题名的窗口。
            如果有多个窗口符合条件,只返回第一个找到的窗口。
        
        函数原型:
            long FindWindow(class,title)
        
        参数定义:
            类名 字符串: 窗口类名,如果为空,则匹配所有类名
            标题 字符串: 窗口标题,如果为空,则匹配所有标题
        
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        
        示例:
            hwnd = dm.window.查找窗口("Notepad", "无标题 - 记事本")
            if hwnd > 0:
                print(f"找到记事本窗口,句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找窗口: {msg}")
            return 0
            
        try:
            return self._dm.FindWindow(类名, 标题)
        except Exception as e:
            print(f"Error in 查找窗口: {str(e)}")
            return 0

    def 查找窗口按进程(self, 进程名: str, 类名: str, 标题: str) -> int:
        """
        函数简介:
            根据指定的进程名,来查找符合类名或者标题名的窗口。
            如果有多个窗口符合条件,只返回第一个找到的窗口。
        
        函数原型:
            long FindWindowByProcess(process_name,class_name,title)
        
        参数定义:
            进程名 字符串: 进程名,比如"notepad.exe"
            类名 字符串: 窗口类名,如果为空,则匹配所有类名
            标题 字符串: 窗口标题,如果为空,则匹配所有标题
        
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        
        示例:
            hwnd = dm.window.查找窗口按进程("notepad.exe", "", "无标题 - 记事本")
            if hwnd > 0:
                print(f"找到记事本窗口,句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找窗口按进程: {msg}")
            return 0
            
        try:
            return self._dm.FindWindowByProcess(进程名, 类名, 标题)
        except Exception as e:
            print(f"Error in 查找窗口按进程: {str(e)}")
            return 0

    def 查找窗口按进程ID(self, 进程ID: int, 类名: str, 标题: str) -> int:
        """
        函数简介:
            根据指定的进程ID,来查找符合类名或者标题名的窗口。
            如果有多个窗口符合条件,只返回第一个找到的窗口。
        
        函数原型:
            long FindWindowByProcessId(process_id,class_name,title)
        
        参数定义:
            进程ID 整形数: 进程ID
            类名 字符串: 窗口类名,如果为空,则匹配所有类名
            标题 字符串: 窗口标题,如果为空,则匹配所有标题
        
        返回值:
            整形数: 整形表示的窗口句柄,没找到返回0
        
        示例:
            hwnd = dm.window.查找窗口按进程ID(1234, "", "无标题 - 记事本")
            if hwnd > 0:
                print(f"找到记事本窗口,句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找窗口按进程ID: {msg}")
            return 0
            
        try:
            return self._dm.FindWindowByProcessId(进程ID, 类名, 标题)
        except Exception as e:
            print(f"Error in 查找窗口按进程ID: {str(e)}")
            return 0

    def 查找窗口Ex(self, 类名: str, 标题: str) -> str:
        """
        函数简介:
            根据指定的条件,枚举系统中符合条件的窗口。
            可以枚举多个窗口。
        
        函数原型:
            string FindWindowEx(parent,class_name,title)
        
        参数定义:
            类名 字符串: 窗口类名,如果为空,则匹配所有类名
            标题 字符串: 窗口标题,如果为空,则匹配所有标题
        
        返回值:
            字符串: 返回所有匹配的窗口句柄,并按"|"分隔
                   比如"123|456|789"
                   如果没有找到任何窗口,返回空字符串
        
        示例:
            hwnds = dm.window.查找窗口Ex("Notepad", "无标题 - 记事本")
            if hwnds:
                for hwnd in hwnds.split("|"):
                    print(f"找到记事本窗口,句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找窗口Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindWindowEx(类名, 标题)
        except Exception as e:
            print(f"Error in 查找窗口Ex: {str(e)}")
            return ""

    def 获取窗口焦点(self) -> int:
        """
        函数简介:
            获取当前窗口的焦点。
        
        函数原型:
            long GetForegroundFocus()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 当前窗口焦点所在的窗口句柄
        
        示例:
            hwnd = dm.window.获取窗口焦点()
            print(f"当前焦点窗口句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口焦点: {msg}")
            return 0
            
        try:
            return self._dm.GetForegroundFocus()
        except Exception as e:
            print(f"Error in 获取窗口焦点: {str(e)}")
            return 0

    def 获取前台窗口(self) -> int:
        """
        函数简介:
            获取当前前台窗口。
        
        函数原型:
            long GetForegroundWindow()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 当前前台窗口句柄
        
        示例:
            hwnd = dm.window.获取前台窗口()
            print(f"当前前台窗口句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取前台窗口: {msg}")
            return 0
            
        try:
            return self._dm.GetForegroundWindow()
        except Exception as e:
            print(f"Error in 获取前台窗口: {str(e)}")
            return 0

    def 获取鼠标指向(self) -> int:
        """
        函数简介:
            获取鼠标指向的窗口句柄。
        
        函数原型:
            long GetPointWindow()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 鼠标指向的窗口句柄
        
        示例:
            hwnd = dm.window.获取鼠标指向()
            print(f"鼠标指向的窗口句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取鼠标指向: {msg}")
            return 0
            
        try:
            return self._dm.GetPointWindow()
        except Exception as e:
            print(f"Error in 获取鼠标指向: {str(e)}")
            return 0

    def 获取进程信息(self, 进程名: str) -> str:
        """
        函数简介:
            根据指定的进程名,获取进程详细信息。
        
        函数原型:
            string GetProcessInfo(process_name)
        
        参数定义:
            进程名 字符串: 进程名,比如"notepad.exe"
        
        返回值:
            字符串: 返回所有匹配的进程信息,格式"pid,进程路径"
                   并按"|"分隔
                   比如"1234,c:\\windows\\notepad.exe|5678,d:\\tools\\notepad.exe"
                   如果没有找到任何进程,返回空字符串
        
        示例:
            info = dm.window.获取进程信息("notepad.exe")
            if info:
                for proc in info.split("|"):
                    pid, path = proc.split(",")
                    print(f"找到记事本进程,PID:{pid} 路径:{path}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取进程信息: {msg}")
            return ""
            
        try:
            return self._dm.GetProcessInfo(进程名)
        except Exception as e:
            print(f"Error in 获取进程信息: {str(e)}")
            return ""

    def 获取特殊窗口(self, 窗口类型: int) -> int:
        """
        函数简介:
            获取一些特殊的窗口句柄。
        
        函数原型:
            long GetSpecialWindow(flag)
        
        参数定义:
            窗口类型 整形数: 取值定义如下:
                           0 : 获取桌面窗口
                           1 : 获取任务栏窗口
        
        返回值:
            整形数: 返回要查找的窗口句柄
        
        示例:
            # 获取桌面窗口句柄
            hwnd = dm.window.获取特殊窗口(0)
            print(f"桌面窗口句柄:{hwnd}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取特殊窗口: {msg}")
            return 0
            
        try:
            return self._dm.GetSpecialWindow(窗口类型)
        except Exception as e:
            print(f"Error in 获取特殊窗口: {str(e)}")
            return 0

    def 获取窗口(self, 窗口句柄: int, 标题: str) -> int:
        """
        函数简介:
            获取指定窗口相关的窗口句柄。
            可以获取到父窗口,子窗口,兄弟窗口等。
        
        函数原型:
            long GetWindow(hwnd,flag)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            标题 字符串: 取值定义如下:
                       "父窗口" : 返回父窗口句柄
                       "子窗口" : 返回第一个子窗口句柄
                       "兄弟窗口" : 返回下一个兄弟窗口句柄
                       "前一个" : 返回前一个兄弟窗口句柄
        
        返回值:
            整形数: 返回要查找的窗口句柄
        
        示例:
            # 获取父窗口句柄
            parent = dm.window.获取窗口(hwnd, "父窗口")
            print(f"父窗口句柄:{parent}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口: {msg}")
            return 0
            
        try:
            return self._dm.GetWindow(窗口句柄, 标题)
        except Exception as e:
            print(f"Error in 获取窗口: {str(e)}")
            return 0

    def 获取窗口类名(self, 窗口句柄: int) -> str:
        """
        函数简介:
            获取指定窗口的类名。
        
        函数原型:
            string GetWindowClass(hwnd)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
        
        返回值:
            字符串: 窗口的类名
        
        示例:
            class_name = dm.window.获取窗口类名(hwnd)
            print(f"窗口类名:{class_name}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口类名: {msg}")
            return ""
            
        try:
            return self._dm.GetWindowClass(窗口句柄)
        except Exception as e:
            print(f"Error in 获取窗口类名: {str(e)}")
            return ""

    def 获取窗口进程ID(self, 窗口句柄: int) -> int:
        """
        函数简介:
            获取指定窗口所在的进程ID。
        
        函数原型:
            long GetWindowProcessId(hwnd)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
        
        返回值:
            整形数: 返回窗口所在的进程ID
        
        示例:
            pid = dm.window.获取窗口进程ID(hwnd)
            print(f"窗口所在进程ID:{pid}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口进程ID: {msg}")
            return 0
            
        try:
            return self._dm.GetWindowProcessId(窗口句柄)
        except Exception as e:
            print(f"Error in 获取窗口进程ID: {str(e)}")
            return 0

    def 获取窗口进程路径(self, 窗口句柄: int) -> str:
        """
        函数简介:
            获取指定窗口所在的进程的exe文件全路径。
        
        函数原型:
            string GetWindowProcessPath(hwnd)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
        
        返回值:
            字符串: 返回窗口所在的进程的exe文件路径
        
        示例:
            path = dm.window.获取窗口进程路径(hwnd)
            print(f"窗口进程路径:{path}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口进程路径: {msg}")
            return ""
            
        try:
            return self._dm.GetWindowProcessPath(窗口句柄)
        except Exception as e:
            print(f"Error in 获取窗口进程路径: {str(e)}")
            return ""

    def 获取窗口矩形(self, 窗口句柄: int) -> tuple:
        """
        函数简介:
            获取指定窗口的区域。
        
        函数原型:
            long GetWindowRect(hwnd,x1,y1,x2,y2)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: 窗口左上角X坐标, 整形数: 窗口左上角Y坐标, 
                  整形数: 窗口右下角X坐标, 整形数: 窗口右下角Y坐标)
        
        示例:
            ret, x1, y1, x2, y2 = dm.window.获取窗口矩形(hwnd)
            if ret == 1:
                print(f"窗口区域:({x1},{y1},{x2},{y2})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口矩形: {msg}")
            return 0, 0, 0, 0, 0
            
        try:
            return self._dm.GetWindowRect(窗口句柄)
        except Exception as e:
            print(f"Error in 获取窗口矩形: {str(e)}")
            return 0, 0, 0, 0, 0

    def 获取窗口状态(self, 窗口句柄: int, 标志: int) -> int:
        """
        函数简介:
            获取指定窗口的一些属性。
        
        函数原型:
            long GetWindowState(hwnd,flag)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            标志 整形数: 取值定义如下:
                       0 : 判断窗口是否存在
                       1 : 判断窗口是否处于激活
                       2 : 判断窗口是否可见
                       3 : 判断窗口是否最小化
                       4 : 判断窗口是否最大化
                       5 : 判断窗口是否置顶
                       6 : 判断窗口是否无响应
                       7 : 判断窗口是否可用(灰色为不可用)
                       8 : 判断窗口是否可见2(不同方式判断)
                       9 : 判断窗口所在进程是否挂起
                       10 : 判断窗口是否有标题栏
                       11 : 判断窗口是否有工具条
                       12 : 判断窗口是否有滚动条
                       13 : 判断窗口是否有菜单条
                       14 : 判断窗口是否有纵向滚动条
                       15 : 判断窗口是否有横向滚动条
                       16 : 判断窗口是否有系统菜单
                       17 : 判断窗口是否有可见边框
                       18 : 判断窗口是否可以改变大小
                       19 : 判断窗口是否有标题栏按钮
                       20 : 判断窗口是否有最大化按钮
                       21 : 判断窗口是否有最小化按钮
                       22 : 判断窗口是否有帮助按钮
                       23 : 判断窗口是否有关闭按钮
        
        返回值:
            整形数: 0: 不满足条件 1: 满足条件
        
        示例:
            # 判断窗口是否存在
            ret = dm.window.获取窗口状态(hwnd, 0)
            if ret == 1:
                print("窗口存在")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口状态: {msg}")
            return 0
            
        try:
            return self._dm.GetWindowState(窗口句柄, 标志)
        except Exception as e:
            print(f"Error in 获取窗口状态: {str(e)}")
            return 0

    def 获取窗口标题(self, 窗口句柄: int) -> str:
        """
        函数简介:
            获取指定窗口的标题。
        
        函数原型:
            string GetWindowTitle(hwnd)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
        
        返回值:
            字符串: 窗口的标题
        
        示例:
            title = dm.window.获取窗口标题(hwnd)
            print(f"窗口标题:{title}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取窗口标题: {msg}")
            return ""
            
        try:
            return self._dm.GetWindowTitle(窗口句柄)
        except Exception as e:
            print(f"Error in 获取窗口标题: {str(e)}")
            return ""

    def 移动窗口(self, 窗口句柄: int, x: int, y: int) -> int:
        """
        函数简介:
            移动指定窗口到指定位置。
        
        函数原型:
            long MoveWindow(hwnd,x,y)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            x 整形数: 窗口左上角X坐标
            y 整形数: 窗口左上角Y坐标
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.移动窗口(hwnd, 100, 100)
            if ret == 1:
                print("窗口移动成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 移动窗口: {msg}")
            return 0
            
        try:
            return self._dm.MoveWindow(窗口句柄, x, y)
        except Exception as e:
            print(f"Error in 移动窗口: {str(e)}")
            return 0

    def 屏幕坐标到窗口(self, 窗口句柄: int, x: int, y: int) -> tuple:
        """
        函数简介:
            把屏幕坐标转换为窗口坐标。
        
        函数原型:
            long ScreenToClient(hwnd,x,y,rx,ry)
        
        参数定义:
            窗口句柄 整形数: 指定的窗口句柄
            x 整形数: 屏幕X坐标
            y 整形数: 屏幕Y坐标
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: 窗口X坐标, 整形数: 窗口Y坐标)
        
        示例:
            ret, rx, ry = dm.window.屏幕坐标到窗口(hwnd, 100, 100)
            if ret == 1:
                print(f"窗口坐标为:({rx}, {ry})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 屏幕坐标到窗口: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.ScreenToClient(窗口句柄, x, y)
        except Exception as e:
            print(f"Error in 屏幕坐标到窗口: {str(e)}")
            return 0, 0, 0

    def 发送粘贴(self, 窗口句柄: int) -> int:
        """
        函数简介:
            向指定窗口发送粘贴命令。
            同按键操作Ctrl+V。
        
        函数原型:
            long SendPaste(hwnd)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.发送粘贴(hwnd)
            if ret == 1:
                print("粘贴成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 发送粘贴: {msg}")
            return 0
            
        try:
            return self._dm.SendPaste(窗口句柄)
        except Exception as e:
            print(f"Error in 发送粘贴: {str(e)}")
            return 0

    def 发送文本(self, 窗口句柄: int, 内容: str) -> int:
        """
        函数简介:
            向指定窗口发送文本数据。
            相当于在窗口中输入文本。
        
        函数原型:
            long SendString(hwnd,str)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            内容 字符串: 要发送的文本数据
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.发送文本(hwnd, "测试文本")
            if ret == 1:
                print("发送成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 发送文本: {msg}")
            return 0
            
        try:
            return self._dm.SendString(窗口句柄, 内容)
        except Exception as e:
            print(f"Error in 发送文本: {str(e)}")
            return 0

    def 发送文本2(self, 窗口句柄: int, 内容: str) -> int:
        """
        函数简介:
            向指定窗口发送文本数据。
            此接口为老的SendString，如果新的SendString不能输入，可以尝试此接口。
        
        函数原型:
            long SendString2(hwnd,str)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            内容 字符串: 要发送的文本数据
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.发送文本2(hwnd, "测试文本")
            if ret == 1:
                print("发送成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 发送文本2: {msg}")
            return 0
            
        try:
            return self._dm.SendString2(窗口句柄, 内容)
        except Exception as e:
            print(f"Error in 发送文本2: {str(e)}")
            return 0

    def 设置窗口大小(self, 窗口句柄: int, 宽度: int, 高度: int) -> int:
        """
        函数简介:
            设置窗口的大小。
        
        函数原型:
            long SetClientSize(hwnd,width,height)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            宽度 整形数: 窗口宽度
            高度 整形数: 窗口高度
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.设置窗口大小(hwnd, 800, 600)
            if ret == 1:
                print("设置窗口大小成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置窗口大小: {msg}")
            return 0
            
        try:
            return self._dm.SetClientSize(窗口句柄, 宽度, 高度)
        except Exception as e:
            print(f"Error in 设置窗口大小: {str(e)}")
            return 0

    def 设置窗口状态(self, 窗口句柄: int, 状态: int) -> int:
        """
        函数简介:
            设置窗口的状态。
        
        函数原型:
            long SetWindowState(hwnd,flag)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            状态 整形数: 取值定义如下:
                       0 : 关闭指定窗口
                       1 : 激活指定窗口
                       2 : 最小化指定窗口,但不激活
                       3 : 最小化指定窗口,并释放内存,但同时也会激活窗口
                       4 : 最大化指定窗口,同时激活窗口
                       5 : 恢复指定窗口 ,但不激活
                       6 : 隐藏指定窗口
                       7 : 显示指定窗口
                       8 : 置顶指定窗口
                       9 : 取消置顶指定窗口
                       10 : 禁止指定窗口
                       11 : 取消禁止指定窗口
                       12 : 恢复并激活指定窗口
                       13 : 强制结束窗口所在进程
                       14 : 闪烁指定的窗口
                       15 : 使指定的窗口获取输入焦点
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            # 最大化窗口
            ret = dm.window.设置窗口状态(hwnd, 4)
            if ret == 1:
                print("窗口最大化成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置窗口状态: {msg}")
            return 0
            
        try:
            return self._dm.SetWindowState(窗口句柄, 状态)
        except Exception as e:
            print(f"Error in 设置窗口状态: {str(e)}")
            return 0

    def 设置窗口标题(self, 窗口句柄: int, 标题: str) -> int:
        """
        函数简介:
            设置窗口的标题。
        
        函数原型:
            long SetWindowText(hwnd,title)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            标题 字符串: 新的窗口标题
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.设置窗口标题(hwnd, "新标题")
            if ret == 1:
                print("设置窗口标题成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置窗口标题: {msg}")
            return 0
            
        try:
            return self._dm.SetWindowText(窗口句柄, 标题)
        except Exception as e:
            print(f"Error in 设置窗口标题: {str(e)}")
            return 0

    def 设置窗口透明(self, 窗口句柄: int, 透明度: int) -> int:
        """
        函数简介:
            设置窗口的透明度。
        
        函数原型:
            long SetWindowTransparent(hwnd,trans)
        
        参数定义:
            窗口句柄 整形数: 窗口句柄
            透明度 整形数: 透明度取值(0-255) 越小透明度越大
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.设置窗口透明(hwnd, 200)
            if ret == 1:
                print("设置窗口透明度成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置窗口透明: {msg}")
            return 0
            
        try:
            return self._dm.SetWindowTransparent(窗口句柄, 透明度)
        except Exception as e:
            print(f"Error in 设置窗口透明: {str(e)}")
            return 0

    def 设置发送文本延迟(self, 延迟: int) -> int:
        """
        函数简介:
            设置发送文本的延迟。
            影响SendString和SendString2接口的发送延迟。
        
        函数原型:
            long SetSendStringDelay(delay)
        
        参数定义:
            延迟 整形数: 延迟值，单位是毫秒
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.window.设置发送文本延迟(100)  # 设置发送延迟为100毫秒
            if ret == 1:
                print("设置发送延迟成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置发送文本延迟: {msg}")
            return 0
            
        try:
            return self._dm.SetSendStringDelay(延迟)
        except Exception as e:
            print(f"Error in 设置发送文本延迟: {str(e)}")
            return 0

    def SetSendStringDelay(self, *args, **kwargs):
        """英文别名，调用设置发送文本延迟"""
        return self.设置发送文本延迟(*args, **kwargs)

    # 添加英文别名
    def ClientToScreen(self, *args, **kwargs):
        """英文别名，调用客户区转屏幕"""
        return self.客户区转屏幕(*args, **kwargs)

    def EnumProcess(self, *args, **kwargs):
        """英文别名，调用枚举进程"""
        return self.枚举进程(*args, **kwargs)

    def EnumWindow(self, *args, **kwargs):
        """英文别名，调用枚举窗口"""
        return self.枚举窗口(*args, **kwargs)

    def EnumWindowByProcess(self, *args, **kwargs):
        """英文别名，调用枚举窗口按进程"""
        return self.枚举窗口按进程(*args, **kwargs)

    def FindWindow(self, *args, **kwargs):
        """英文别名，调用查找窗口"""
        return self.查找窗口(*args, **kwargs)

    def FindWindowByProcess(self, *args, **kwargs):
        """英文别名，调用查找窗口按进程"""
        return self.查找窗口按进程(*args, **kwargs)

    def FindWindowByProcessId(self, *args, **kwargs):
        """英文别名，调用查找窗口按进程ID"""
        return self.查找窗口按进程ID(*args, **kwargs)

    def FindWindowEx(self, *args, **kwargs):
        """英文别名，调用查找窗口Ex"""
        return self.查找窗口Ex(*args, **kwargs)

    def GetForegroundFocus(self, *args, **kwargs):
        """英文别名，调用获取窗口焦点"""
        return self.获取窗口焦点(*args, **kwargs)

    def GetForegroundWindow(self, *args, **kwargs):
        """英文别名，调用获取前台窗口"""
        return self.获取前台窗口(*args, **kwargs)

    def GetPointWindow(self, *args, **kwargs):
        """英文别名，调用获取鼠标指向"""
        return self.获取鼠标指向(*args, **kwargs)

    def GetProcessInfo(self, *args, **kwargs):
        """英文别名，调用获取进程信息"""
        return self.获取进程信息(*args, **kwargs)

    def GetSpecialWindow(self, *args, **kwargs):
        """英文别名，调用获取特殊窗口"""
        return self.获取特殊窗口(*args, **kwargs)

    def GetWindow(self, *args, **kwargs):
        """英文别名，调用获取窗口"""
        return self.获取窗口(*args, **kwargs)

    def GetWindowClass(self, *args, **kwargs):
        """英文别名，调用获取窗口类名"""
        return self.获取窗口类名(*args, **kwargs)

    def GetWindowProcessId(self, *args, **kwargs):
        """英文别名，调用获取窗口进程ID"""
        return self.获取窗口进程ID(*args, **kwargs)

    def GetWindowProcessPath(self, *args, **kwargs):
        """英文别名，调用获取窗口进程路径"""
        return self.获取窗口进程路径(*args, **kwargs)

    def GetWindowRect(self, *args, **kwargs):
        """英文别名，调用获取窗口矩形"""
        return self.获取窗口矩形(*args, **kwargs)

    def GetWindowState(self, *args, **kwargs):
        """英文别名，调用获取窗口状态"""
        return self.获取窗口状态(*args, **kwargs)

    def GetWindowTitle(self, *args, **kwargs):
        """英文别名，调用获取窗口标题"""
        return self.获取窗口标题(*args, **kwargs)

    def MoveWindow(self, *args, **kwargs):
        """英文别名，调用移动窗口"""
        return self.移动窗口(*args, **kwargs)

    def ScreenToClient(self, *args, **kwargs):
        """英文别名，调用屏幕坐标到窗口"""
        return self.屏幕坐标到窗口(*args, **kwargs)

    def SendPaste(self, *args, **kwargs):
        """英文别名，调用发送粘贴"""
        return self.发送粘贴(*args, **kwargs)

    def SendString(self, *args, **kwargs):
        """英文别名，调用发送文本"""
        return self.发送文本(*args, **kwargs)

    def SendString2(self, *args, **kwargs):
        """英文别名，调用发送文本2"""
        return self.发送文本2(*args, **kwargs)

    def SetClientSize(self, *args, **kwargs):
        """英文别名，调用设置窗口大小"""
        return self.设置窗口大小(*args, **kwargs)

    def SetWindowState(self, *args, **kwargs):
        """英文别名，调用设置窗口状态"""
        return self.设置窗口状态(*args, **kwargs)

    def SetWindowText(self, *args, **kwargs):
        """英文别名，调用设置窗口标题"""
        return self.设置窗口标题(*args, **kwargs)

    def SetWindowTransparent(self, *args, **kwargs):
        """英文别名，调用设置窗口透明"""
        return self.设置窗口透明(*args, **kwargs)

