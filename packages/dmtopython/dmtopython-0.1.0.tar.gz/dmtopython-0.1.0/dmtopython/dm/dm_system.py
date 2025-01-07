#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件系统模块API封装
用于系统相关的功能
'''

class DmSystem:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    # 1. 基础操作函数
    def 蜂鸣(self) -> int:
        """
        函数简介:
            发出蜂鸣声。

        函数原型:
            long Beep()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 蜂鸣: {msg}")
            return 0
            
        try:
            return self._dm.Beep()
        except Exception as e:
            print(f"Error in 蜂鸣: {str(e)}")
            return 0

    def 睡眠(self, 毫秒: int) -> int:
        """
        函数简介:
            休眠指定的毫秒数。

        函数原型:
            long Sleep(ms)

        参数定义:
            毫秒 整形数: 要休眠的毫秒数

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 睡眠: {msg}")
            return 0
            
        try:
            return self._dm.Sleep(毫秒)
        except Exception as e:
            print(f"Error in 睡眠: {str(e)}")
            return 0

    def 延时(self, 毫秒: int) -> int:
        """
        函数简介:
            延迟指定的毫秒数。

        函数原型:
            long Delay(ms)

        参数定义:
            毫秒 整形数: 要延迟的毫秒数

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 延时: {msg}")
            return 0
            
        try:
            return self._dm.Delay(毫秒)
        except Exception as e:
            print(f"Error in 延时: {str(e)}")
            return 0

    def 延时精确(self, 毫秒: int) -> int:
        """
        函数简介:
            延迟指定的毫秒数，精确度较高。

        函数原型:
            long Delays(ms)

        参数定义:
            毫秒 整形数: 要延迟的毫秒数

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 延时精确: {msg}")
            return 0
            
        try:
            return self._dm.Delays(毫秒)
        except Exception as e:
            print(f"Error in 延时精确: {str(e)}")
            return 0

    def 停止(self) -> int:
        """
        函数简介:
            停止脚本。

        函数原型:
            long Stop()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 停止: {msg}")
            return 0
            
        try:
            return self._dm.Stop()
        except Exception as e:
            print(f"Error in 停止: {str(e)}")
            return 0

    # 2. 系统信息获取函数
    def 获取DPI(self) -> int:
        """
        函数简介:
            获取系统DPI。

        函数原型:
            long GetDPI()

        参数定义:
            无

        返回值:
            整形数: DPI数值
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取DPI: {msg}")
            return 0
            
        try:
            return self._dm.GetDPI()
        except Exception as e:
            print(f"Error in 获取DPI: {str(e)}")
            return 0

    def 获取显示信息(self) -> str:
        """
        函数简介:
            获取显示信息。

        函数原型:
            string GetDisplayInfo()

        参数定义:
            无

        返回值:
            字符串: 显示信息
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取显示信息: {msg}")
            return ""
            
        try:
            return self._dm.GetDisplayInfo()
        except Exception as e:
            print(f"Error in 获取显示信息: {str(e)}")
            return ""

    def 获取CPU类型(self) -> str:
        """
        函数简介:
            获取CPU类型。

        函数原型:
            string GetCpuType()

        参数定义:
            无

        返回值:
            字符串: CPU类型
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取CPU类型: {msg}")
            return ""
            
        try:
            return self._dm.GetCpuType()
        except Exception as e:
            print(f"Error in 获取CPU类型: {str(e)}")
            return ""

    def 获取CPU使用率(self) -> int:
        """
        函数简介:
            获取CPU使用率。

        函数原型:
            long GetCpuUsage()

        参数定义:
            无

        返回值:
            整形数: CPU使用率(0-100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取CPU使用率: {msg}")
            return 0
            
        try:
            return self._dm.GetCpuUsage()
        except Exception as e:
            print(f"Error in 获取CPU使用率: {str(e)}")
            return 0

    def 获取内存使用率(self) -> int:
        """
        函数简介:
            获取内存使用率。

        函数原型:
            long GetMemoryUsage()

        参数定义:
            无

        返回值:
            整形数: 内存使用率(0-100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取内存使用率: {msg}")
            return 0
            
        try:
            return self._dm.GetMemoryUsage()
        except Exception as e:
            print(f"Error in 获取内存使用率: {str(e)}")
            return 0

    def 获取磁盘序列号(self, 索引: int) -> str:
        """
        函数简介:
            获取指定序号的磁盘序列号。

        函数原型:
            string GetDiskReversion(index)

        参数定义:
            索引 整形数: 磁盘序号

        返回值:
            字符串: 磁盘序列号
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取磁盘序列号: {msg}")
            return ""
            
        try:
            return self._dm.GetDiskReversion(索引)
        except Exception as e:
            print(f"Error in 获取磁盘序列号: {str(e)}")
            return ""

    # 3. 系统设置函数
    def 检查字体平滑(self) -> int:
        """
        函数简介:
            检查系统是否开启了字体平滑。

        函数原型:
            long CheckFontSmooth()

        参数定义:
            无

        返回值:
            整形数: 0: 未开启 1: 已开启
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 检查字体平滑: {msg}")
            return 0
            
        try:
            return self._dm.CheckFontSmooth()
        except Exception as e:
            print(f"Error in 检查字体平滑: {str(e)}")
            return 0

    def 检查UAC(self) -> int:
        """
        函数简介:
            检查当前系统是否开启了UAC。

        函数原型:
            long CheckUAC()

        参数定义:
            无

        返回值:
            整形数: 0: 未开启 1: 已开启
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 检查UAC: {msg}")
            return 0
            
        try:
            return self._dm.CheckUAC()
        except Exception as e:
            print(f"Error in 检查UAC: {str(e)}")
            return 0

    def 禁用关闭显示器和睡眠(self) -> int:
        """
        函数简介:
            禁止系统关闭显示器和睡眠。

        函数原型:
            long DisableCloseDisplayAndSleep()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 禁用关闭显示器和睡眠: {msg}")
            return 0
            
        try:
            return self._dm.DisableCloseDisplayAndSleep()
        except Exception as e:
            print(f"Error in 禁用关闭显示器和睡眠: {str(e)}")
            return 0

    def 禁用字体平滑(self) -> int:
        """
        函数简介:
            禁用系统字体平滑。

        函数原型:
            long DisableFontSmooth()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 禁用字体平滑: {msg}")
            return 0
            
        try:
            return self._dm.DisableFontSmooth()
        except Exception as e:
            print(f"Error in 禁用字体平滑: {str(e)}")
            return 0

    def 禁用电源保护(self) -> int:
        """
        函数简介:
            禁用系统电源保护。

        函数原型:
            long DisablePowerSave()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 禁用电源保护: {msg}")
            return 0
            
        try:
            return self._dm.DisablePowerSave()
        except Exception as e:
            print(f"Error in 禁用电源保护: {str(e)}")
            return 0

    def 禁用屏幕保护(self) -> int:
        """
        函数简介:
            禁用系统屏幕保护。

        函数原型:
            long DisableScreenSave()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 禁用屏幕保护: {msg}")
            return 0
            
        try:
            return self._dm.DisableScreenSave()
        except Exception as e:
            print(f"Error in 禁用屏幕保护: {str(e)}")
            return 0

    def 启用字体平滑(self) -> int:
        """
        函数简介:
            启用系统字体平滑。

        函数原型:
            long EnableFontSmooth()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用字体平滑: {msg}")
            return 0
            
        try:
            return self._dm.EnableFontSmooth()
        except Exception as e:
            print(f"Error in 启用字体平滑: {str(e)}")
            return 0

    # 4. 显示相关函数
    def 获取屏幕宽度(self) -> int:
        """
        函数简介:
            获取屏幕宽度。

        函数原型:
            long GetScreenWidth()

        参数定义:
            无

        返回值:
            整形数: 屏幕宽度
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取屏幕宽度: {msg}")
            return 0
            
        try:
            return self._dm.GetScreenWidth()
        except Exception as e:
            print(f"Error in 获取屏幕宽度: {str(e)}")
            return 0

    def 获取屏幕高度(self) -> int:
        """
        函数简介:
            获取屏幕高度。

        函数原型:
            long GetScreenHeight()

        参数定义:
            无

        返回值:
            整形数: 屏幕高度
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取屏幕高度: {msg}")
            return 0
            
        try:
            return self._dm.GetScreenHeight()
        except Exception as e:
            print(f"Error in 获取屏幕高度: {str(e)}")
            return 0

    def 获取屏幕色深(self) -> int:
        """
        函数简介:
            获取屏幕色深。

        函数原型:
            long GetScreenDepth()

        参数定义:
            无

        返回值:
            整形数: 屏幕色深
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取屏幕色深: {msg}")
            return 0
            
        try:
            return self._dm.GetScreenDepth()
        except Exception as e:
            print(f"Error in 获取屏幕色深: {str(e)}")
            return 0

    def 设置屏幕(self, 宽度: int, 高度: int, 颜色深度: int) -> int:
        """
        函数简介:
            设置屏幕分辨率。

        函数原型:
            long SetScreen(width,height,depth)

        参数定义:
            宽度 整形数: 屏幕宽度
            高度 整形数: 屏幕高度
            颜色深度 整形数: 颜色深度

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置屏幕: {msg}")
            return 0
            
        try:
            return self._dm.SetScreen(宽度, 高度, 颜色深度)
        except Exception as e:
            print(f"Error in 设置屏幕: {str(e)}")
            return 0

    def 设置显示加速(self, 启用: int) -> int:
        """
        函数简介:
            设置是否启用显示加速。

        函数原型:
            long SetDisplayAcceler(enable)

        参数定义:
            启用 整形数: 0: 禁用 1: 启用

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置显示加速: {msg}")
            return 0
            
        try:
            return self._dm.SetDisplayAcceler(启用)
        except Exception as e:
            print(f"Error in 设置显示加速: {str(e)}")
            return 0

    # 5. 其他功能函数
    def 获取剪贴板(self) -> str:
        """
        函数简介:
            获取剪贴板的内容。

        函数原型:
            string GetClipboard()

        参数定义:
            无

        返回值:
            字符串: 剪贴板内容
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取剪贴板: {msg}")
            return ""
            
        try:
            return self._dm.GetClipboard()
        except Exception as e:
            print(f"Error in 获取剪贴板: {str(e)}")
            return ""

    def 设置剪贴板(self, 内容: str) -> int:
        """
        函数简介:
            设置剪贴板的内容。

        函数原型:
            long SetClipboard(value)

        参数定义:
            内容 字符串: 要设置的内容

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置剪贴板: {msg}")
            return 0
            
        try:
            return self._dm.SetClipboard(内容)
        except Exception as e:
            print(f"Error in 设置剪贴板: {str(e)}")
            return 0

    def 播放声音(self, 文件: str) -> int:
        """
        函数简介:
            播放指定的声音文件。

        函数原型:
            long Play(file)

        参数定义:
            文件 字符串: 声音文件名

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 播放声音: {msg}")
            return 0
            
        try:
            return self._dm.Play(文件)
        except Exception as e:
            print(f"Error in 播放声音: {str(e)}")
            return 0

    def 获取时间(self) -> str:
        """
        函数简介:
            获取当前系统时间。

        函数原型:
            string GetTime()

        参数定义:
            无

        返回值:
            字符串: 当前系统时间
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取时间: {msg}")
            return ""
            
        try:
            return self._dm.GetTime()
        except Exception as e:
            print(f"Error in 获取时间: {str(e)}")
            return ""

    def 获取网络时间(self) -> str:
        """
        函数简介:
            获取网络时间。

        函数原型:
            string GetNetTime()

        参数定义:
            无

        返回值:
            字符串: 网络时间
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取网络时间: {msg}")
            return ""
            
        try:
            return self._dm.GetNetTime()
        except Exception as e:
            print(f"Error in 获取网络时间: {str(e)}")
            return ""

    def 获取磁盘型号(self, 索引: int) -> str:
        """
        函数简介:
            获取指定序号的磁盘型号。

        函数原型:
            string GetDiskModel(index)

        参数定义:
            索引 整形数: 磁盘序号

        返回值:
            字符串: 磁盘型号
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取磁盘型号: {msg}")
            return ""
            
        try:
            return self._dm.GetDiskModel(索引)
        except Exception as e:
            print(f"Error in 获取磁盘型号: {str(e)}")
            return ""

    def 获取区域(self) -> int:
        """
        函数简介:
            获取系统区域。

        函数原型:
            long GetLocale()

        参数定义:
            无

        返回值:
            整形数: 系统区域标识
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取区域: {msg}")
            return 0
            
        try:
            return self._dm.GetLocale()
        except Exception as e:
            print(f"Error in 获取区域: {str(e)}")
            return 0

    def 获取机器码(self) -> str:
        """
        函数简介:
            获取本机机器码。

        函数原型:
            string GetMachineCode()

        参数定义:
            无

        返回值:
            字符串: 机器码
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取机器码: {msg}")
            return ""
            
        try:
            return self._dm.GetMachineCode()
        except Exception as e:
            print(f"Error in 获取机器码: {str(e)}")
            return ""

    def 获取机器码NoMac(self) -> str:
        """
        函数简介:
            获取本机机器码(不包含MAC地址)。

        函数原型:
            string GetMachineCodeNoMac()

        参数定义:
            无

        返回值:
            字符串: 机器码
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取机器码NoMac: {msg}")
            return ""
            
        try:
            return self._dm.GetMachineCodeNoMac()
        except Exception as e:
            print(f"Error in 获取机器码NoMac: {str(e)}")
            return ""

    def 获取网络时间ByIp(self, IP地址: str) -> str:
        """
        函数简介:
            获取指定IP的网络时间。

        函数原型:
            string GetNetTimeByIp(ip)

        参数定义:
            IP地址 字符串: IP地址

        返回值:
            字符串: 网络时间
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取网络时间ByIp: {msg}")
            return ""
            
        try:
            return self._dm.GetNetTimeByIp(IP地址)
        except Exception as e:
            print(f"Error in 获取网络时间ByIp: {str(e)}")
            return ""

    def 获取网络时间Safe(self) -> str:
        """
        函数简介:
            安全方式获取网络时间。

        函数原型:
            string GetNetTimeSafe()

        参数定义:
            无

        返回值:
            字符串: 网络时间
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取网络时间Safe: {msg}")
            return ""
            
        try:
            return self._dm.GetNetTimeSafe()
        except Exception as e:
            print(f"Error in 获取网络时间Safe: {str(e)}")
            return ""

    def 获取系统版本号(self) -> str:
        """
        函数简介:
            获取操作系统版本号。

        函数原型:
            string GetOsBuildNumber()

        参数定义:
            无

        返回值:
            字符串: 系统版本号
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取系统版本号: {msg}")
            return ""
            
        try:
            return self._dm.GetOsBuildNumber()
        except Exception as e:
            print(f"Error in 获取系统版本号: {str(e)}")
            return ""

    def 获取系统信息(self) -> str:
        """
        函数简介:
            获取系统信息。

        函数原型:
            string GetSystemInfo()

        参数定义:
            无

        返回值:
            字符串: 系统信息
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取系统信息: {msg}")
            return ""
            
        try:
            return self._dm.GetSystemInfo()
        except Exception as e:
            print(f"Error in 获取系统信息: {str(e)}")
            return ""

    def 获取64位(self) -> int:
        """
        函数简介:
            判断系统是否是64位。

        函数原型:
            long Is64Bit()

        参数定义:
            无

        返回值:
            整形数: 0: 32位 1: 64位
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取64位: {msg}")
            return 0
            
        try:
            return self._dm.Is64Bit()
        except Exception as e:
            print(f"Error in 获取64位: {str(e)}")
            return 0

    def 运行程序(self, 路径: str, 模式: int = 1) -> int:
        """
        函数简介:
            运行指定的程序。

        函数原型:
            long RunApp(path,mode)

        参数定义:
            路径 字符串: 程序路径
            模式 整形数: 运行模式 默认为1

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 运行程序: {msg}")
            return 0
            
        try:
            return self._dm.RunApp(路径, 模式)
        except Exception as e:
            print(f"Error in 运行程序: {str(e)}")
            return 0

    def 显示任务栏图标(self, 显示: int) -> int:
        """
        函数简介:
            显示或隐藏任务栏图标。

        函数原型:
            long ShowTaskBarIcon(show)

        参数定义:
            显示 整形数: 0: 隐藏 1: 显示

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 显示任务栏图标: {msg}")
            return 0
            
        try:
            return self._dm.ShowTaskBarIcon(显示)
        except Exception as e:
            print(f"Error in 显示任务栏图标: {str(e)}")
            return 0

    def 获取目录(self) -> str:
        """
        函数简介:
            获取当前程序的目录。

        函数原型:
            string GetDir(type)

        参数定义:
            无

        返回值:
            字符串: 当前目录
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取目录: {msg}")
            return ""
            
        try:
            return self._dm.GetDir(0)
        except Exception as e:
            print(f"Error in 获取目录: {str(e)}")
            return ""

    def 退出系统(self, 类型: int = 1) -> int:
        """
        函数简介:
            退出系统。

        函数原型:
            long ExitOs(type)

        参数定义:
            类型 整形数: 退出类型 0: 注销 1: 关机 2: 重启

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 退出系统: {msg}")
            return 0
            
        try:
            return self._dm.ExitOs(类型)
        except Exception as e:
            print(f"Error in 退出系统: {str(e)}")
            return 0

    # 添加对应的英文别名
    def GetDiskModel(self, *args, **kwargs):
        """英文别名，调用获取磁盘型号"""
        return self.获取磁盘型号(*args, **kwargs)

    def GetLocale(self, *args, **kwargs):
        """英文别名，调用获取区域"""
        return self.获取区域(*args, **kwargs)

    def GetMachineCode(self, *args, **kwargs):
        """英文别名，调用获取机器码"""
        return self.获取机器码(*args, **kwargs)

    def GetMachineCodeNoMac(self, *args, **kwargs):
        """英文别名，调用获取机器码NoMac"""
        return self.获取机器码NoMac(*args, **kwargs)

    def GetNetTimeByIp(self, *args, **kwargs):
        """英文别名，调用获取网络时间ByIp"""
        return self.获取网络时间ByIp(*args, **kwargs)

    def GetNetTimeSafe(self, *args, **kwargs):
        """英文别名，调用获取网络时间Safe"""
        return self.获取网络时间Safe(*args, **kwargs)

    def GetOsBuildNumber(self, *args, **kwargs):
        """英文别名，调用获取系统版本号"""
        return self.获取系统版本号(*args, **kwargs)

    def GetSystemInfo(self, *args, **kwargs):
        """英文别名，调用获取系统信息"""
        return self.获取系统信息(*args, **kwargs)

    def Is64Bit(self, *args, **kwargs):
        """英文别名，调用获取64位"""
        return self.获取64位(*args, **kwargs)

    def RunApp(self, *args, **kwargs):
        """英文别名，调用运行程序"""
        return self.运行程序(*args, **kwargs)

    def ShowTaskBarIcon(self, *args, **kwargs):
        """英文别名，调用显示任务栏图标"""
        return self.显示任务栏图标(*args, **kwargs)

    def GetDir(self, *args, **kwargs):
        """英文别名，调用获取目录"""
        return self.获取目录(*args, **kwargs)

    def ExitOs(self, *args, **kwargs):
        """英文别名，调用退出系统"""
        return self.退出系统(*args, **kwargs)

    def 获取输入法方法(self) -> str:
        """
        函数简介:
            获取当前输入法的输入方法。

        函数原型:
            string ActiveInputMethod()

        参数定义:
            无

        返回值:
            字符串: 当前输入法的输入方法
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取输入法方法: {msg}")
            return ""
            
        try:
            return self._dm.ActiveInputMethod()
        except Exception as e:
            print(f"Error in 获取输入法方法: {str(e)}")
            return ""

    def 检查输入法(self, 输入法: str) -> int:
        """
        函数简介:
            检查指定输入法是否活动。

        函数原型:
            long CheckInputMethod(input_method)

        参数定义:
            输入法 字符串: 输入法名称

        返回值:
            整形数: 0: 不活动 1: 活动
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 检查输入法: {msg}")
            return 0
            
        try:
            return self._dm.CheckInputMethod(输入法)
        except Exception as e:
            print(f"Error in 检查输入法: {str(e)}")
            return 0

    def 按回车(self) -> int:
        """
        函数简介:
            模拟按下回车键。

        函数原型:
            long EnterCri()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 按回车: {msg}")
            return 0
            
        try:
            return self._dm.EnterCri()
        except Exception as e:
            print(f"Error in 按回车: {str(e)}")
            return 0

    def 执行命令(self, 命令: str) -> int:
        """
        函数简介:
            执行指定的系统命令。

        函数原型:
            long ExecuteCmd(cmd)

        参数定义:
            命令 字符串: 要执行的命令

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 执行命令: {msg}")
            return 0
            
        try:
            return self._dm.ExecuteCmd(命令)
        except Exception as e:
            print(f"Error in 执行命令: {str(e)}")
            return 0

    def 查找输入法(self, 输入法: str) -> int:
        """
        函数简介:
            查找指定的输入法。

        函数原型:
            long FindInputMethod(input_method)

        参数定义:
            输入法 字符串: 输入法名称

        返回值:
            整形数: 0: 未找到 1: 找到
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找输入法: {msg}")
            return 0
            
        try:
            return self._dm.FindInputMethod(输入法)
        except Exception as e:
            print(f"Error in 查找输入法: {str(e)}")
            return 0

    def 初始化(self) -> int:
        """
        函数简介:
            初始化系统。

        函数原型:
            long InitCri()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 初始化: {msg}")
            return 0
            
        try:
            return self._dm.InitCri()
        except Exception as e:
            print(f"Error in 初始化: {str(e)}")
            return 0

    def 离开输入法(self) -> int:
        """
        函数简介:
            离开当前输入法。

        函数原型:
            long LeaveCri()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 离开输入法: {msg}")
            return 0
            
        try:
            return self._dm.LeaveCri()
        except Exception as e:
            print(f"Error in 离开输入法: {str(e)}")
            return 0

    def 释放引用(self) -> int:
        """
        函数简介:
            释放系统资源。

        函数原型:
            long ReleaseRef()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 释放引用: {msg}")
            return 0
            
        try:
            return self._dm.ReleaseRef()
        except Exception as e:
            print(f"Error in 释放引用: {str(e)}")
            return 0

    def 设置输入法(self, 输入法: str) -> int:
        """
        函数简介:
            设置系统输入法。

        函数原型:
            long SetSimMode(mode)

        参数定义:
            输入法 字符串: 输入法名称

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置输入法: {msg}")
            return 0
            
        try:
            return self._dm.SetSimMode(输入法)
        except Exception as e:
            print(f"Error in 设置输入法: {str(e)}")
            return 0

    # 添加对应的英文别名
    def ActiveInputMethod(self, *args, **kwargs):
        """英文别名，调用获取输入法方法"""
        return self.获取输入法方法(*args, **kwargs)

    def CheckInputMethod(self, *args, **kwargs):
        """英文别名，调用检查输入法"""
        return self.检查输入法(*args, **kwargs)

    def EnterCri(self, *args, **kwargs):
        """英文别名，调用按回车"""
        return self.按回车(*args, **kwargs)

    def ExecuteCmd(self, *args, **kwargs):
        """英文别名，调用执行命令"""
        return self.执行命令(*args, **kwargs)

    def FindInputMethod(self, *args, **kwargs):
        """英文别名，调用查找输入法"""
        return self.查找输入法(*args, **kwargs)

    def InitCri(self, *args, **kwargs):
        """英文别名，调用初始化"""
        return self.初始化(*args, **kwargs)

    def LeaveCri(self, *args, **kwargs):
        """英文别名，调用离开输入法"""
        return self.离开输入法(*args, **kwargs)

    def ReleaseRef(self, *args, **kwargs):
        """英文别名，调用释放引用"""
        return self.释放引用(*args, **kwargs)

    def SetSimMode(self, *args, **kwargs):
        """英文别名，调用设置输入法"""
        return self.设置输入法(*args, **kwargs)

    def 排除窗口(self, 窗口句柄: int) -> int:
        """
        函数简介:
            排除指定的窗口,以便后台键鼠操作。

        函数原型:
            long ExcludePos(hwnd)

        参数定义:
            窗口句柄 整形数: 要排除的窗口句柄

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 排除窗口: {msg}")
            return 0
            
        try:
            return self._dm.ExcludePos(窗口句柄)
        except Exception as e:
            print(f"Error in 排除窗口: {str(e)}")
            return 0

    def 排除区域(self, 左边: int, 顶边: int, 右边: int, 底边: int) -> int:
        """
        函数简介:
            排除指定的区域,以便后台键鼠操作。

        函数原型:
            long ExcludePos(left, top, right, bottom)

        参数定义:
            左边 整形数: 区域的左边坐标
            顶边 整形数: 区域的顶边坐标
            右边 整形数: 区域的右边坐标
            底边 整形数: 区域的底边坐标

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 排除区域: {msg}")
            return 0
            
        try:
            return self._dm.ExcludePos(左边, 顶边, 右边, 底边)
        except Exception as e:
            print(f"Error in 排除区域: {str(e)}")
            return 0

    def 设置排除距离(self, 距离: int) -> int:
        """
        函数简介:
            设置排除区域的大小。

        函数原型:
            long SetPosDistance(distance)

        参数定义:
            距离 整形数: 排除区域的大小

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置排除距离: {msg}")
            return 0
            
        try:
            return self._dm.SetPosDistance(距离)
        except Exception as e:
            print(f"Error in 设置排除距离: {str(e)}")
            return 0

    # 添加对应的英文别名
    def ExcludePos(self, *args, **kwargs):
        """英文别名，调用排除窗口或排除区域"""
        if len(args) == 1:
            return self.排除窗口(*args, **kwargs)
        else:
            return self.排除区域(*args, **kwargs)

    def SetPosDistance(self, *args, **kwargs):
        """英文别名，调用设置排除距离"""
        return self.设置排除距离(*args, **kwargs)

    def 添加汇编(self, 汇编指令: str) -> int:
        """
        函数简介:
            添加汇编指令。

        函数原型:
            long AsmAdd(asm_ins)

        参数定义:
            汇编指令 字符串: 汇编指令

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 添加汇编: {msg}")
            return 0
            
        try:
            return self._dm.AsmAdd(汇编指令)
        except Exception as e:
            print(f"Error in 添加汇编: {str(e)}")
            return 0

    def 调用汇编(self) -> int:
        """
        函数简介:
            调用已添加的汇编指令。

        函数原型:
            long AsmCall(mode)

        参数定义:
            无

        返回值:
            整形数: 调用结果
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 调用汇编: {msg}")
            return 0
            
        try:
            return self._dm.AsmCall(0)
        except Exception as e:
            print(f"Error in 调用汇编: {str(e)}")
            return 0

    def 清除汇编(self) -> int:
        """
        函数简介:
            清除已添加的汇编指令。

        函数原型:
            long AsmClear()

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 清除汇编: {msg}")
            return 0
            
        try:
            return self._dm.AsmClear()
        except Exception as e:
            print(f"Error in 清除汇编: {str(e)}")
            return 0

    def 设置汇编超时(self, 毫秒: int) -> int:
        """
        函数简介:
            设置汇编指令执行的超时时间。

        函数原型:
            long AsmSetTimeout(time_out)

        参数定义:
            毫秒 整形数: 超时时间(毫秒)

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置汇编超时: {msg}")
            return 0
            
        try:
            return self._dm.AsmSetTimeout(毫秒)
        except Exception as e:
            print(f"Error in 设置汇编超时: {str(e)}")
            return 0

    def 汇编(self, 汇编指令: str) -> int:
        """
        函数简介:
            执行汇编指令。

        函数原型:
            long Assemble(base_addr,is_64bit)

        参数定义:
            汇编指令 字符串: 汇编指令

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 汇编: {msg}")
            return 0
            
        try:
            return self._dm.Assemble(汇编指令, 0)
        except Exception as e:
            print(f"Error in 汇编: {str(e)}")
            return 0

    def 反汇编(self, 地址: int, 是否64位: int = 0) -> str:
        """
        函数简介:
            将指定地址的机器码反汇编。

        函数原型:
            string DisAssemble(asm_code,base_addr,is_64bit)

        参数定义:
            地址 整形数: 内存地址
            是否64位 整形数: 0: 32位 1: 64位

        返回值:
            字符串: 反汇编结果
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 反汇编: {msg}")
            return ""
            
        try:
            return self._dm.DisAssemble(地址, 是否64位)
        except Exception as e:
            print(f"Error in 反汇编: {str(e)}")
            return ""

    def 设置显示错误信息(self, 显示: int) -> int:
        """
        函数简介:
            设置是否显示错误信息。

        函数原型:
            long SetShowAsmErrorMsg(show)

        参数定义:
            显示 整形数: 0: 不显示 1: 显示

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置显示错误信息: {msg}")
            return 0
            
        try:
            return self._dm.SetShowAsmErrorMsg(显示)
        except Exception as e:
            print(f"Error in 设置显示错误信息: {str(e)}")
            return 0

    # 添加对应的英文别名
    def AsmAdd(self, *args, **kwargs):
        """英文别名，调用添加汇编"""
        return self.添加汇编(*args, **kwargs)

    def AsmCall(self, *args, **kwargs):
        """英文别名，调用调用汇编"""
        return self.调用汇编(*args, **kwargs)

    def AsmClear(self, *args, **kwargs):
        """英文别名，调用清除汇编"""
        return self.清除汇编(*args, **kwargs)

    def AsmSetTimeout(self, *args, **kwargs):
        """英文别名，调用设置汇编超时"""
        return self.设置汇编超时(*args, **kwargs)

    def Assemble(self, *args, **kwargs):
        """英文别名，调用汇编"""
        return self.汇编(*args, **kwargs)

    def DisAssemble(self, *args, **kwargs):
        """英文别名，调用反汇编"""
        return self.反汇编(*args, **kwargs)

    def SetShowAsmErrorMsg(self, *args, **kwargs):
        """英文别名，调用设置显示错误信息"""
        return self.设置显示错误信息(*args, **kwargs)

    def 启用图片缓存(self) -> int:
        """
        函数简介:
            启用图片缓存。

        函数原型:
            long EnablePicCache(enable)

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用图片缓存: {msg}")
            return 0
            
        try:
            return self._dm.EnablePicCache(1)
        except Exception as e:
            print(f"Error in 启用图片缓存: {str(e)}")
            return 0

    def 获取基础路径(self) -> str:
        """
        函数简介:
            获取系统基础路径。

        函数原型:
            string GetBasePath()

        参数定义:
            无

        返回值:
            字符串: 基础路径
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取基础路径: {msg}")
            return ""
            
        try:
            return self._dm.GetBasePath()
        except Exception as e:
            print(f"Error in 获取基础路径: {str(e)}")
            return ""

    def 获取实例数量(self) -> int:
        """
        函数简介:
            获取dm实例数量

        函数原型:
            long GetDmCount()

        参数定义:
            无

        返回值:
            整形数: 实例数量
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取文档数量: {msg}")
            return 0
            
        try:
            return self._dm.GetDmCount()
        except Exception as e:
            print(f"Error in 获取文档数量: {str(e)}")
            return 0

    def 获取ID(self) -> int:
        """
        函数简介:
            获取对象ID。

        函数原型:
            long GetID()

        参数定义:
            无

        返回值:
            整形数: 对象ID
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取ID: {msg}")
            return 0
            
        try:
            return self._dm.GetID()
        except Exception as e:
            print(f"Error in 获取ID: {str(e)}")
            return 0

    def 获取最后错误(self) -> int:
        """
        函数简介:
            获取插件命令的最后错误。

        函数原型:
            long GetLastError()

        参数定义:
            无

        返回值:
            整形数: 错误代码
                0: 无错误
                -1: 使用了绑定里的收费功能，但是没注册，无法使用
                -2: 使用模式0 2时出现，因为目标窗口有保护。常见于win7以上系统或者有安全软件拦截插件。解决办法: 关闭所有安全软件，然后再重新尝试。如果还不行就可以肯定是目标窗口有特殊保护
                -3: 使用模式0 2时出现，可能目标窗口有保护，也可能是异常错误。可以尝试换绑定模式或许可以解决
                -4: 使用模式101 103时出现，这是异常错误
                -5: 使用模式101 103时出现，这个错误的解决办法就是关闭目标窗口，重新打开再绑定即可。也可能是运行脚本的进程没有管理员权限
                -6: 被安全软件拦截。典型的是金山、360等。如果是360关闭即可。如果是金山，必须卸载，关闭是没用的
                -7,-9: 使用模式101 103时出现，异常错误。还有可能是安全软件的问题，比如360等。尝试卸载360
                -8,-10: 使用模式101 103时出现，目标进程可能有保护，也可能是插件版本过老，试试新的或许可以解决。-8可以尝试使用DmGuard中的np2盾配合
                -11,-12,-37: 使用模式101 103时出现，目标进程有保护
                -13: 使用模式101 103时出现，目标进程有保护。或者是因为上次的绑定没有解绑导致。尝试在绑定前调用ForceUnBindWindow
                -14: 可能系统缺少部分DLL，尝试安装d3d。或者是鼠标或者键盘使用了dx.mouse.api或者dx.keypad.api，但实际系统没有插鼠标和键盘。也有可能是图色中有dx.graphic.3d之类的，但相应的图色被占用，比如全屏D3D程序
                -16: 可能使用了绑定模式 0 和 101，然后可能指定了一个子窗口导致不支持。可以换模式2或者103来尝试。另外也可以考虑使用父窗口或者顶级窗口来避免这个错误。还有可能是目标窗口没有正常解绑然后再次绑定的时候
                -17: 模式101 103时出现的异常错误
                -18: 句柄无效
                -19: 使用模式0 11 101时出现的异常错误
                -20: 使用模式101 103时出现，说明目标进程里没有解绑，并且子绑定达到了最大。尝试在返回这个错误时，调用ForceUnBindWindow来强制解除绑定
                -21: 使用任何模式时出现，说明目标进程已经存在了绑定(没有正确解绑就退出了?被其它软件绑定?或者多个线程同时进行了绑定?)。尝试在返回这个错误时，调用ForceUnBindWindow来强制解除绑定或者检查自己的代码
                -22: 使用模式0 2，绑定64位进程窗口时出现，因为安全软件拦截插件释放的EXE文件导致
                -23: 使用模式0 2，绑定64位进程窗口时出现，因为安全软件拦截插件释放的DLL文件导致
                -24,-25: 使用模式0 2，绑定64位进程窗口时出现，因为安全软件拦截插件运行释放的EXE
                -26: 使用模式0 2，绑定64位进程窗口时出现，因为目标窗口有保护。常见于win7以上系统或者有安全软件拦截插件。解决办法: 关闭所有安全软件，然后再重新尝试。如果还不行就可以肯定是目标窗口有特殊保护
                -27: 绑定64位进程窗口时出现，因为使用了不支持的模式，目前暂时只支持模式0 2 11 13 101 103
                -28: 绑定32位进程窗口时出现，因为使用了不支持的模式，目前暂时只支持模式0 2 11 13 101 103
                -38: 使用了大于2的绑定模式，并且使用了dx.public.inject.c时，分配内存失败。可以考虑开启memory系列盾来尝试
                -39,-41: 使用了大于2的绑定模式，并且使用了dx.public.inject.c时的异常错误
                -40: 使用了大于2的绑定模式，并且使用了dx.public.inject.c时，写入内存失败。可以考虑开启memory系列盾来尝试
                -42: 绑定时，创建映射内存失败。这是个异常错误。一般不会出现。如果出现了，检查下代码是不是有同个对象同时绑定的情况。还有可能是你的进程有句柄泄露导致无法创建句柄会出这个错误
                -43: 绑定时，映射内存失败。这是个异常错误。一般不会出现。如果出现了，一般是你的进程内存不足，检查下你的进程是不是内存泄漏了
                -44: 无效的参数，通常是传递了不支持的参数
                -45: 绑定时，创建互斥信号失败。这个是异常错误。一般不会出现。如果出现了检查进程是否有句柄泄漏的情况
                -100: 调用读写内存函数后，发现无效的窗口句柄
                -101: 读写内存函数失败
                -200: AsmCall失败
                -202: AsmCall平台兼容问题，联系我解决

        注意:
            此函数必须紧跟上一句函数调用，中间任何的语句调用都会改变这个值。

        示例:
            TracePrint dm.GetLastError()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取最后错误: {msg}")
            return 0
            
        try:
            return self._dm.GetLastError()
        except Exception as e:
            print(f"Error in 获取最后错误: {str(e)}")
            return 0

    def GetLastError(self, *args, **kwargs):
        """英文别名，调用获取最后错误"""
        return self.获取最后错误(*args, **kwargs)

    def 获取路径(self) -> str:
        """
        函数简介:
            获取当前路径。

        函数原型:
            string GetPath()

        参数定义:
            无

        返回值:
            字符串: 当前路径

        示例:
            path = dm.GetPath()
            TracePrint path
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取路径: {msg}")
            return ""
            
        try:
            return self._dm.GetPath()
        except Exception as e:
            print(f"Error in 获取路径: {str(e)}")
            return ""

    # 添加对应的英文别名
    def EnablePicCache(self, *args, **kwargs):
        """英文别名，调用启用图片缓存"""
        return self.启用图片缓存(*args, **kwargs)

    def GetBasePath(self, *args, **kwargs):
        """英文别名，调用获取基础路径"""
        return self.获取基础路径(*args, **kwargs)

    def GetDocCount(self, *args, **kwargs):
        """英文别名，调用获取文档数量"""
        return self.获取文档数量(*args, **kwargs)

    def GetID(self, *args, **kwargs):
        """英文别名，调用获取ID"""
        return self.获取ID(*args, **kwargs)

    def GetLastError(self, *args, **kwargs):
        """英文别名，调用获取最后错误"""
        return self.获取最后错误(*args, **kwargs)

    def GetPath(self, *args, **kwargs):
        """英文别名，调用获取路径"""
        return self.获取路径(*args, **kwargs)

    def 设置显示输入(self, 显示: int) -> int:
        """
        函数简介:
            设置是否显示输入。

        函数原型:
            long SetDisplayInput(show)

        参数定义:
            显示 整形数: 
                0: 不显示 
                1: 显示

        返回值:
            整形数: 
                0: 失败 
                1: 成功

        示例:
            dm.SetDisplayInput(1)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置显示输入: {msg}")
            return 0
            
        try:
            return self._dm.SetDisplayInput(显示)
        except Exception as e:
            print(f"Error in 设置显示输入: {str(e)}")
            return 0

    def 设置枚举窗口延时(self, 延时: int) -> int:
        """
        函数简介:
            设置枚举窗口的超时时间。

        函数原型:
            long SetEnumWindowDelay(delay)

        参数定义:
            延时 整形数: 延时时间(毫秒)

        返回值:
            整形数: 
                0: 失败 
                1: 成功

        示例:
            dm.SetEnumWindowDelay(2000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置枚举窗口延时: {msg}")
            return 0
            
        try:
            return self._dm.SetEnumWindowDelay(延时)
        except Exception as e:
            print(f"Error in 设置枚举窗口延时: {str(e)}")
            return 0

    def 设置显示错误(self, 显示: int) -> int:
        """
        函数简介:
            设置是否显示错误信息。

        函数原型:
            long SetShowErrorMsg(show)

        参数定义:
            显示 整形数: 
                0: 不显示 
                1: 显示

        返回值:
            整形数: 
                0: 失败 
                1: 成功

        示例:
            dm.SetShowErrorMsg(1)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置显示错误: {msg}")
            return 0
            
        try:
            return self._dm.SetShowErrorMsg(显示)
        except Exception as e:
            print(f"Error in 设置显示错误: {str(e)}")
            return 0

    def 设置正常图色(self, 启用: int = 1) -> int:
        """
        函数简介:
            设置是否对前台图色进行加速(默认是关闭)。
            (对于不绑定，或者绑定图色为normal生效)(仅对WIN8以上系统有效)

        函数原型:
            long SpeedNormalGraphic(enable)

        参数定义:
            启用 整形数: 
                0: 关闭
                1: 打开

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            dm.SpeedNormalGraphic(1)

        注: 
            1. WIN8以上系统,由于AERO的开启,导致前台图色速度很慢,使用此接口可以显著提速
            2. WIN7系统无法使用,只能通过关闭aero来对前台图色提速
            3. 每个进程最多只能有一个对象开启此加速接口
            4. 如果要用开启别的对象的加速，那么要先关闭之前开启的
            5. 开启此接口后,仅能对主显示器的屏幕进行截图,分屏的显示器上的内容无法截图
            6. 开启此接口后，程序CPU会有一定上升，因为这个方法是以牺牲CPU性能来提升速度的
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置正常图色: {msg}")
            return 0
            
        try:
            return self._dm.SpeedNormalGraphic(启用)
        except Exception as e:
            print(f"Error in 设置正常图色: {str(e)}")
            return 0

    # 添加对应的英文别名
    def SetDisplayInput(self, *args, **kwargs):
        """英文别名，调用设置显示输入"""
        return self.设置显示输入(*args, **kwargs)

    def SetEnumWindowDelay(self, *args, **kwargs):
        """英文别名，调用设置枚举窗口延时"""
        return self.设置枚举窗口延时(*args, **kwargs)

    def SetShowErrorMsg(self, *args, **kwargs):
        """英文别名，调用设置显示错误"""
        return self.设置显示错误(*args, **kwargs)

    def SpeedNormalGraphic(self, *args, **kwargs):
        """英文别名，调用设置正常图色"""
        return self.设置正常图色(*args, **kwargs)

    def 防护盾(self, 启用: int, 类型: str) -> int:
        """
        函数简介:
            针对部分检测措施的保护盾。前面有五角星(★)的表示同时支持32位和64位,否则就仅支持64位。
            驱动功能支持的系统版本号为win7及以上系统的正式版本。
            新点的WIN10和WIN11必须要关闭内核隔离,否则会无法加载驱动,或者加载某些功能蓝屏。

        函数原型:
            long DmGuard(enable,type)

        参数定义:
            启用 整形数: 
                0: 关闭保护盾(仅对memory/memory2/memory3/memory4/b2/b3起作用)
                1: 打开保护盾
            类型 字符串: 保护盾类型,可以是以下任意一个:
                ★"np": 防止NP检测(已过时,不建议使用)
                ★"memory": 保护内存系列接口和汇编接口(需要加载驱动)
                ★"memory2": 保护内存系列接口和汇编接口(需要加载驱动)
                "memory3 pid addr_start addr_end": 保护指定进程的内存操作
                "memory4": 保护内存系列接口和汇编接口(需要加载驱动)
                "memory5": 保护内存系列接口(直接读写物理内存,需要加载驱动)
                "memory6": memory5的加强版本
                "phide [pid]": 隐藏指定进程(32位系统)
                "phide2 [pid]": 同phide但进程可见
                "phide3 [pid]": 仅隐藏进程
                ★"display2": 防止截图的极端模式
                ★"display3 <hwnd>": 保护指定窗口防截图
                "display4 <hwnd>": 保护指定窗口(需要加载驱动)
                ★"block [pid]": 保护进程不被非法访问
                ★"b2 [pid]": 另一种进程保护方式
                "b3 [pid]": 另一种进程保护方式
                "f1 [pid]": 进程伪装
                ★"d1 [cls][add dll_name exact]": 阻止DLL加载
                ★"f2 <target> <protect>": 进程伪装
                "hm module unlink": 防止模块被非法访问
                "inject mode pid <p1> <p2>": DLL注入
                "del <path>": 强制删除文件
                "cl pid type name": 关闭指定句柄
                "hl [pid]": 隐藏进程句柄
                "gr": 开启句柄操作
                "th": 开启线程操作

        返回值:
            整形数: 
                1: 成功
                0: 不支持的保护盾类型
                -1: 32位平台不支持
                -2: 驱动释放失败
                -3: 驱动加载失败
                -4到-6: 异常错误
                -7: 系统版本不支持
                -8: 驱动加载失败
                -9: 参数错误
                -10: 功能失败
                -11: 分配内存失败
                -14: 无效窗口句柄
                -16: 依赖驱动未启动
                -20: 功能不可重复加载
                其他负值: 其他错误

        示例:
            dm.防护盾(1, "memory")  # 开启内存保护
            dm.防护盾(1, "display2")  # 开启防截图
            dm.防护盾(1, "block")  # 保护当前进程
            dm.防护盾(1, "block 1044")  # 保护指定进程
            dm.防护盾(0, "b2")  # 关闭b2保护
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 防护盾: {msg}")
            return 0
            
        try:
            return self._dm.DmGuard(启用, 类型)
        except Exception as e:
            print(f"Error in 防护盾: {str(e)}")
            return 0

    def 防护盾解除(self) -> int:
        """
        函数简介:
            解除防护盾

        函数原型:
            long DmGuardExtract()

        参数定义:
            无参数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            防护盾解除()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 防护盾解除: {msg}")
            return 0
            
        try:
            return self._dm.DmGuardExtract()
        except Exception as e:
            print(f"Error in 防护盾解除: {str(e)}")
            return 0

    def 防护盾加载自定义(self, 自定义参数: str) -> int:
        """
        函数简介:
            加载自定义的防护盾参数

        函数原型:
            long DmGuardLoadCustom(custom_param)

        参数定义:
            自定义参数 字符串: 自定义的防护盾参数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            防护盾加载自定义("custom_param")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 防护盾加载自定义: {msg}")
            return 0
            
        try:
            return self._dm.DmGuardLoadCustom(自定义参数)
        except Exception as e:
            print(f"Error in 防护盾加载自定义: {str(e)}")
            return 0

    def 防护盾参数(self, 命令: str, 子命令: str, 参数: str) -> str:
        """
        函数简介:
            DmGuard的加强接口,用于获取一些额外信息。必须先用DmGuard开启对应的盾才能使用此接口。

        函数原型:
            string DmGuardParams(cmd,subcmd,param)

        参数定义:
            命令 字符串: 盾类型,可以是以下值:
                "gr": 句柄操作相关(需先调用 防护盾(1,"gr"))
                "th": 线程操作相关(需先调用 防护盾(1,"th"))
            子命令 字符串: 具体操作类型:
                当命令为"gr"时:
                    "enum": 枚举指定进程的所有句柄
                    "get": 获取指定句柄信息(类型,名字,权限值)
                    "set": 设置指定句柄的权限值
                    "close": 关闭指定句柄
                当命令为"th"时:
                    "enum": 枚举指定进程的所有线程
                    "get": 获取指定线程的详细信息
                    "resume": 恢复指定线程
                    "suspend": 挂起指定线程
                    "terminate": 结束指定线程
            参数 字符串: 根据命令和子命令不同而不同:
                当命令为"gr"时:
                    "enum": "pid" (进程ID,十进制)
                    "get": "pid handle" (进程ID和句柄值,十进制)
                    "set": "pid handle access" (进程ID,句柄值,权限值,十进制)
                    "close": "pid handle" (进程ID和句柄值,十进制)
                当命令为"th"时:
                    "enum": "pid" (进程ID,十进制)
                    "get": "tid" (线程ID,十进制)
                    "resume": "tid" (线程ID,十进制)
                    "suspend": "tid" (线程ID,十进制)
                    "terminate": "tid" (线程ID,十进制)

        返回值:
            字符串: 根据命令和子命令不同而不同:
                当命令为"gr"时:
                    "enum": "handle1|handle2|...|handlen" (句柄列表)
                    "get": "type|name|access" (句柄类型|名字|权限值)
                    "set": "ok"表示成功,空字符串表示失败
                    "close": "ok"表示成功,空字符串表示失败
                当命令为"th"时:
                    "enum": "tid1|tid2|...|tidn" (线程ID列表)
                    "get": "tid|priority|ethread|teb|win32StartAddress|module_name|switch_count|state|suspend_count"
                    "resume": "ok"表示成功,空字符串表示失败
                    "suspend": "ok"表示成功,空字符串表示失败
                    "terminate": "ok"表示成功,空字符串表示失败

        示例:
            # 枚举进程1024的所有句柄
            dm.防护盾(1, "gr")
            handles = dm.防护盾参数("gr", "enum", "1024")
            
            # 获取进程1024中句柄240的信息
            dm.防护盾(1, "gr")
            info = dm.防护盾参数("gr", "get", "1024 240")
            
            # 修改进程1024中句柄240的权限为12345
            dm.防护盾(1, "gr")
            dm.防护盾参数("gr", "set", "1024 240 12345")
            
            # 枚举进程1024的所有线程
            dm.防护盾(1, "th")
            threads = dm.防护盾参数("th", "enum", "1024")
            
            # 结束线程338
            dm.防护盾(1, "th")
            dm.防护盾参数("th", "terminate", "338")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 防护盾参数: {msg}")
            return ""
            
        try:
            return self._dm.DmGuardParams(命令, 子命令, 参数)
        except Exception as e:
            print(f"Error in 防护盾参数: {str(e)}")
            return ""

    # 添加英文别名
    def DmGuard(self, *args, **kwargs):
        """英文别名，调用防护盾"""
        return self.防护盾(*args, **kwargs)

    def DmGuardExtract(self, *args, **kwargs):
        """英文别名，调用防护盾解除"""
        return self.防护盾解除(*args, **kwargs)

    def DmGuardLoadCustom(self, *args, **kwargs):
        """英文别名，调用防护盾加载自定义"""
        return self.防护盾加载自定义(*args, **kwargs)

    def DmGuardParams(self, *args, **kwargs):
        """英文别名，调用防护盾参数"""
        return self.防护盾参数(*args, **kwargs)

    # ... 其他英文别名 ... 