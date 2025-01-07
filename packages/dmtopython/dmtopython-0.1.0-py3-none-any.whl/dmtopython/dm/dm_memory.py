#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件内存模块API封装
用于内存操作相关的功能
'''

class DmMemory:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 双精度数据(self, 值: float) -> str:
        """
        函数简介:
            把双精度浮点数转换成二进制形式.

        函数原型:
            string DoubleToData(value)

        参数定义:
            值 双精度浮点数: 需要转化的双精度浮点数

        返回值:
            字符串: 字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

        示例:
            double_data = 双精度数据(1.24)
            dm_ret = 查找数据(hwnd,"00000000-7fffffff",double_data)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 双精度数据: {msg}")
            return ""
            
        try:
            return self._dm.DoubleToData(值)
        except Exception as e:
            print(f"Error in 双精度数据: {str(e)}")
            return ""

    def 查找数据(self, 窗口句柄: int, 地址范围: str, 数据: str) -> int:
        """
        函数简介:
            在指定的地址范围内查找数据,如果要查找的数据是字符串，可以用StringToData先转换成二进制形式

        函数原型:
            long FindData(hwnd,addr_range,data)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            数据 字符串: 要查找的数据 以字符串形式描述比如"123456",如果要查找的数据是字符串，可以用StringToData先转换成二进制形式

        返回值:
            整形数: 搜索到的地址

        示例:
            hwnd = 查找窗口("","记事本")
            查找数据(hwnd,"00400000-7FFFFFFF","123456")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找数据: {msg}")
            return 0
            
        try:
            return self._dm.FindData(窗口句柄, 地址范围, 数据)
        except Exception as e:
            print(f"Error in 查找数据: {str(e)}")
            return 0

    # 继续添加其他函数...
    def 查找数据Ex(self, 窗口句柄: int, 地址范围: str, 数据: str) -> str:
        """
        函数简介:
            在指定的地址范围内查找数据,如果要查找的数据是字符串，可以用StringToData先转换成二进制形式.这个函数可以查找到重复的地址.

        函数原型:
            string FindDataEx(hwnd,addr_range,data)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            数据 字符串: 要查找的数据 以字符串形式描述比如"123456",如果要查找的数据是字符串，可以用StringToData先转换成二进制形式

        返回值:
            字符串: 找到的地址集合，以|分割

        示例:
            hwnd = 查找窗口("","记事本")
            addrs = 查找数据Ex(hwnd,"00400000-7FFFFFFF","123456")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找数据Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindDataEx(窗口句柄, 地址范围, 数据)
        except Exception as e:
            print(f"Error in 查找数据Ex: {str(e)}")
            return ""

    def 查找双精度(self, 窗口句柄: int, 地址范围: str, 双精度: float) -> int:
        """
        函数简介:
            在指定的地址范围内查找双精度浮点数.

        函数原型:
            long FindDouble(hwnd,addr_range,double_value_min,double_value_max)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            双精度 双精度浮点数: 要查找的双精度浮点数

        返回值:
            整形数: 搜索到的地址

        示例:
            hwnd = 查找窗口("","记事本")
            addr = 查找双精度(hwnd,"00400000-7FFFFFFF",1.24)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找双精度: {msg}")
            return 0
            
        try:
            return self._dm.FindDouble(窗口句柄, 地址范围, 双精度)
        except Exception as e:
            print(f"Error in 查找双精度: {str(e)}")
            return 0

    def 查找双精度Ex(self, 窗口句柄: int, 地址范围: str, 双精度: float) -> str:
        """
        函数简介:
            在指定的地址范围内查找双精度浮点数,可以查找到重复的地址.

        函数原型:
            string FindDoubleEx(hwnd,addr_range,double_value_min,double_value_max)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            双精度 双精度浮点数: 要查找的双精度浮点数

        返回值:
            字符串: 找到的地址集合，以|分割

        示例:
            hwnd = 查找窗口("","记事本")
            addrs = 查找双精度Ex(hwnd,"00400000-7FFFFFFF",1.24)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找双精度Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindDoubleEx(窗口句柄, 地址范围, 双精度)
        except Exception as e:
            print(f"Error in 查找双精度Ex: {str(e)}")
            return ""

    def 查找浮点数(self, 窗口句柄: int, 地址范围: str, 浮点数: float) -> int:
        """
        函数简介:
            在指定的地址范围内查找单精度浮点数.

        函数原型:
            long FindFloat(hwnd,addr_range,float_value_min,float_value_max)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            浮点数 单精度浮点数: 要查找的单精度浮点数

        返回值:
            整形数: 搜索到的地址

        示例:
            hwnd = 查找窗口("","记事本")
            addr = 查找浮点数(hwnd,"00400000-7FFFFFFF",1.24)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找浮点数: {msg}")
            return 0
            
        try:
            return self._dm.FindFloat(窗口句柄, 地址范围, 浮点数)
        except Exception as e:
            print(f"Error in 查找浮点数: {str(e)}")
            return 0

    def 查找浮点数Ex(self, 窗口句柄: int, 地址范围: str, 浮点数: float) -> str:
        """
        函数简介:
            在指定的地址范围内查找单精度浮点数,可以查找到重复的地址.

        函数原型:
            string FindFloatEx(hwnd,addr_range,float_value_min,float_value_max)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            浮点数 单精度浮点数: 要查找的单精度浮点数

        返回值:
            字符串: 找到的地址集合，以|分割

        示例:
            hwnd = 查找窗口("","记事本")
            addrs = 查找浮点数Ex(hwnd,"00400000-7FFFFFFF",1.24)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找浮点数Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindFloatEx(窗口句柄, 地址范围, 浮点数)
        except Exception as e:
            print(f"Error in 查找浮点数Ex: {str(e)}")
            return ""

    def 查找整数(self, 窗口句柄: int, 地址范围: str, 整数: int) -> int:
        """
        函数简介:
            在指定的地址范围内查找整数.

        函数原型:
            long FindInt(hwnd,addr_range,int_value_min,int_value_max)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            整数 整形数: 要查找的整数

        返回值:
            整形数: 搜索到的地址

        示例:
            hwnd = 查找窗口("","记事本")
            addr = 查找整数(hwnd,"00400000-7FFFFFFF",100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找整数: {msg}")
            return 0
            
        try:
            return self._dm.FindInt(窗口句柄, 地址范围, 整数)
        except Exception as e:
            print(f"Error in 查找整数: {str(e)}")
            return 0

    def 查找整数Ex(self, 窗口句柄: int, 地址范围: str, 整数: int) -> str:
        """
        函数简介:
            在指定的地址范围内查找整数,可以查找到重复的地址.

        函数原型:
            string FindIntEx(hwnd,addr_range,int_value_min,int_value_max)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            整数 整形数: 要查找的整数

        返回值:
            字符串: 找到的地址集合，以|分割

        示例:
            hwnd = 查找窗口("","记事本")
            addrs = 查找整数Ex(hwnd,"00400000-7FFFFFFF",100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找整数Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindIntEx(窗口句柄, 地址范围, 整数)
        except Exception as e:
            print(f"Error in 查找整数Ex: {str(e)}")
            return ""

    def 查找字符串(self, 窗口句柄: int, 地址范围: str, 字符串: str) -> int:
        """
        函数简介:
            在指定的地址范围内查找字符串.

        函数原型:
            long FindString(hwnd,addr_range,string_value,type)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            字符串 字符串: 要查找的字符串

        返回值:
            整形数: 搜索到的地址

        示例:
            hwnd = 查找窗口("","记事本")
            addr = 查找字符串(hwnd,"00400000-7FFFFFFF","hello")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串: {msg}")
            return 0
            
        try:
            return self._dm.FindString(窗口句柄, 地址范围, 字符串)
        except Exception as e:
            print(f"Error in 查找字符串: {str(e)}")
            return 0

    def 查找字符串Ex(self, 窗口句柄: int, 地址范围: str, 字符串: str) -> str:
        """
        函数简介:
            在指定的地址范围内查找字符串,可以查找到重复的地址.

        函数原型:
            string FindStringEx(hwnd,addr_range,string_value,type)

        参数定义:
            窗口句柄 整形数: 指定搜索的窗口句柄
            地址范围 字符串: 比如"00400000-7FFFFFFF" 这样的地址范围
            字符串 字符串: 要查找的字符串

        返回值:
            字符串: 找到的地址集合，以|分割

        示例:
            hwnd = 查找窗口("","记事本")
            addrs = 查找字符串Ex(hwnd,"00400000-7FFFFFFF","hello")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindStringEx(窗口句柄, 地址范围, 字符串)
        except Exception as e:
            print(f"Error in 查找字符串Ex: {str(e)}")
            return ""

    def 浮点数转数据(self, 值: float) -> str:
        """
        函数简介:
            把单精度浮点数转换成二进制形式.

        函数原型:
            string FloatToData(value)

        参数定义:
            值 单精度浮点数: 需要转化的单精度浮点数

        返回值:
            字符串: 字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

        示例:
            float_data = 浮点数转数据(1.24)
            dm_ret = 查找数据(hwnd,"00400000-7FFFFFFF",float_data)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 浮点数转数据: {msg}")
            return ""
            
        try:
            return self._dm.FloatToData(值)
        except Exception as e:
            print(f"Error in 浮点数转数据: {str(e)}")
            return ""

    def FindStringEx(self, *args, **kwargs):
        """英文别名，调用查找字符串Ex"""
        return self.查找字符串Ex(*args, **kwargs)

    def FloatToData(self, *args, **kwargs):
        """英文别名，调用浮点数转数据"""
        return self.浮点数转数据(*args, **kwargs)

    # 添加英文别名
    def DoubleToData(self, *args, **kwargs):
        """英文别名，调用双精度数据"""
        return self.双精度数据(*args, **kwargs)

    def FindData(self, *args, **kwargs):
        """英文别名，调用查找数据"""
        return self.查找数据(*args, **kwargs)

    def FindDataEx(self, *args, **kwargs):
        """英文别名，调用查找数据Ex"""
        return self.查找数据Ex(*args, **kwargs)

    def FindDouble(self, *args, **kwargs):
        """英文别名，调用查找双精度"""
        return self.查找双精度(*args, **kwargs)

    def FindDoubleEx(self, *args, **kwargs):
        """英文别名，调用查找双精度Ex"""
        return self.查找双精度Ex(*args, **kwargs)

    def FindFloat(self, *args, **kwargs):
        """英文别名，调用查找浮点数"""
        return self.查找浮点数(*args, **kwargs)

    def FindFloatEx(self, *args, **kwargs):
        """英文别名，调用查找浮点数Ex"""
        return self.查找浮点数Ex(*args, **kwargs)

    def FindInt(self, *args, **kwargs):
        """英文别名，调用查找整数"""
        return self.查找整数(*args, **kwargs)

    def FindIntEx(self, *args, **kwargs):
        """英文别名，调用查找整数Ex"""
        return self.查找整数Ex(*args, **kwargs)

    def FindString(self, *args, **kwargs):
        """英文别名，调用查找字符串"""
        return self.查找字符串(*args, **kwargs)

    def 释放进程内存(self, 窗口句柄: int) -> int:
        """
        函数简介:
            释放指定进程的所有内存

        函数原型:
            long FreeProcessMemory(hwnd)

        参数定义:
            窗口句柄 整形数: 窗口句柄

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            释放进程内存(hwnd)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 释放进程内存: {msg}")
            return 0
            
        try:
            return self._dm.FreeProcessMemory(窗口句柄)
        except Exception as e:
            print(f"Error in 释放进程内存: {str(e)}")
            return 0

    def 获取命令行(self, 窗口句柄: int) -> str:
        """
        函数简介:
            获取指定进程的命令行

        函数原型:
            string GetCommandLine(hwnd)

        参数定义:
            窗口句柄 整形数: 窗口句柄

        返回值:
            字符串: 命令行字符串

        示例:
            cmd = 获取命令行(hwnd)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取命令行: {msg}")
            return ""
            
        try:
            return self._dm.GetCommandLine(窗口句柄)
        except Exception as e:
            print(f"Error in 获取命令行: {str(e)}")
            return ""

    def 获取模块基址(self, 窗口句柄: int, 模块名: str) -> int:
        """
        函数简介:
            获取指定进程的指定模块的基址

        函数原型:
            long GetModuleBaseAddr(hwnd,module)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            模块名 字符串: 模块名

        返回值:
            整形数: 模块的基址

        示例:
            base_addr = 获取模块基址(hwnd,"user32.dll")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取模块基址: {msg}")
            return 0
            
        try:
            return self._dm.GetModuleBaseAddr(窗口句柄, 模块名)
        except Exception as e:
            print(f"Error in 获取模块基址: {str(e)}")
            return 0

    def 获取远程地址(self, 窗口句柄: int, 地址: int) -> int:
        """
        函数简介:
            获取指定进程的指定地址的值

        函数原型:
            long GetRemoteApiAddress(hwnd,base_addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址

        返回值:
            整形数: 地址的值

        示例:
            value = 获取远程地址(hwnd,0x4010000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取远程地址: {msg}")
            return 0
            
        try:
            return self._dm.GetRemoteApiAddress(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 获取远程地址: {str(e)}")
            return 0

    def 整数转指针(self, 整数: int) -> int:
        """
        函数简介:
            把整数转换成地址

        函数原型:
            long Int64ToInt32(value)

        参数定义:
            整数 整形数: 需要转换的整数

        返回值:
            整形数: 转换后的地址

        示例:
            addr = 整数转指针(123456789)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 整数转指针: {msg}")
            return 0
            
        try:
            return self._dm.Int64ToInt32(整数)
        except Exception as e:
            print(f"Error in 整数转指针: {str(e)}")
            return 0

    # 添加新函数的英文别名
    def FreeProcessMemory(self, *args, **kwargs):
        """英文别名，调用释放进程内存"""
        return self.释放进程内存(*args, **kwargs)

    def GetCommandLine(self, *args, **kwargs):
        """英文别名，调用获取命令行"""
        return self.获取命令行(*args, **kwargs)

    def GetModuleBaseAddr(self, *args, **kwargs):
        """英文别名，调用获取模块基址"""
        return self.获取模块基址(*args, **kwargs)

    def GetRemoteApiAddress(self, *args, **kwargs):
        """英文别名，调用获取远程地址"""
        return self.获取远程地址(*args, **kwargs)

    def Int64ToInt32(self, *args, **kwargs):
        """英文别名，调用整数转指针"""
        return self.整数转指针(*args, **kwargs)

    def 打开进程(self, 进程ID: int) -> int:
        """
        函数简介:
            打开一个进程

        函数原型:
            long OpenProcess(pid)

        参数定义:
            进程ID 整形数: 进程ID

        返回值:
            整形数: 进程句柄,失败返回0

        示例:
            pid = 1234
            handle = 打开进程(pid)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 打开进程: {msg}")
            return 0
            
        try:
            return self._dm.OpenProcess(进程ID)
        except Exception as e:
            print(f"Error in 打开进程: {str(e)}")
            return 0

    def 读取数据(self, 窗口句柄: int, 地址: str, 长度: int) -> str:
        """
        函数简介:
            读取指定地址的二进制数据

        函数原型:
            string ReadData(hwnd,addr,len)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            长度 整形数: 要读取的长度

        返回值:
            字符串: 读取到的数据,以16进制表示

        示例:
            data = 读取数据(hwnd,"4A3B2C1D",10)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取数据: {msg}")
            return ""
            
        try:
            return self._dm.ReadData(窗口句柄, 地址, 长度)
        except Exception as e:
            print(f"Error in 读取数据: {str(e)}")
            return ""

    def 读取数据地址(self, 窗口句柄: int, 地址: int, 长度: int) -> str:
        """
        函数简介:
            读取指定地址的二进制数据

        函数原型:
            string ReadDataAddr(hwnd,addr,len)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            长度 整形数: 要读取的长度

        返回值:
            字符串: 读取到的数据,以16进制表示

        示例:
            data = 读取数据地址(hwnd,0x4010000,10)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取数据地址: {msg}")
            return ""
            
        try:
            return self._dm.ReadDataAddr(窗口句柄, 地址, 长度)
        except Exception as e:
            print(f"Error in 读取数据地址: {str(e)}")
            return ""

    def 读取数据二进制(self, 窗口句柄: int, 地址: str, 长度: int) -> str:
        """
        函数简介:
            读取指定地址的二进制数据

        函数原型:
            string ReadDataBin(hwnd,addr,len)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            长度 整形数: 要读取的长度

        返回值:
            字符串: 读取到的数据,以字符串形式表示

        示例:
            data = 读取数据二进制(hwnd,"4A3B2C1D",10)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取数据二进制: {msg}")
            return ""
            
        try:
            return self._dm.ReadDataBin(窗口句柄, 地址, 长度)
        except Exception as e:
            print(f"Error in 读取数据二进制: {str(e)}")
            return ""

    # 添加英文别名
    def OpenProcess(self, *args, **kwargs):
        """英文别名，调用打开进程"""
        return self.打开进程(*args, **kwargs)

    def ReadData(self, *args, **kwargs):
        """英文别名，调用读取数据"""
        return self.读取数据(*args, **kwargs)

    def ReadDataAddr(self, *args, **kwargs):
        """英文别名，调用读取数据地址"""
        return self.读取数据地址(*args, **kwargs)

    def ReadDataBin(self, *args, **kwargs):
        """英文别名，调用读取数据二进制"""
        return self.读取数据二进制(*args, **kwargs)

    def 读取数据地址二进制(self, 窗口句柄: int, 地址: int, 长度: int) -> str:
        """
        函数简介:
            读取指定地址的二进制数据

        函数原型:
            string ReadDataAddrFromBin(hwnd,addr,len)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            长度 整形数: 要读取的长度

        返回值:
            字符串: 读取到的数据,以字符串形式表示

        示例:
            data = 读取数据地址二进制(hwnd,0x4010000,10)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取数据地址二进制: {msg}")
            return ""
            
        try:
            return self._dm.ReadDataAddrFromBin(窗口句柄, 地址, 长度)
        except Exception as e:
            print(f"Error in 读取数据地址二进制: {str(e)}")
            return ""

    def 读取双精度(self, 窗口句柄: int, 地址: str) -> float:
        """
        函数简介:
            读取指定地址的双精度浮点数

        函数原型:
            double ReadDouble(hwnd,addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址

        返回值:
            双精度浮点数: 读取到的双精度浮点数

        示例:
            value = 读取双精度(hwnd,"4A3B2C1D")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取双精度: {msg}")
            return 0.0
            
        try:
            return self._dm.ReadDouble(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 读取双精度: {str(e)}")
            return 0.0

    def 读取双精度地址(self, 窗口句柄: int, 地址: int) -> float:
        """
        函数简介:
            读取指定地址的双精度浮点数

        函数原型:
            double ReadDoubleAddr(hwnd,addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址

        返回值:
            双精度浮点数: 读取到的双精度浮点数

        示例:
            value = 读取双精度地址(hwnd,0x4010000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取双精度地址: {msg}")
            return 0.0
            
        try:
            return self._dm.ReadDoubleAddr(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 读取双精度地址: {str(e)}")
            return 0.0

    # 添加英文别名
    def ReadDataAddrFromBin(self, *args, **kwargs):
        """英文别名，调用读取数据地址二进制"""
        return self.读取数据地址二进制(*args, **kwargs)

    def ReadDouble(self, *args, **kwargs):
        """英文别名，调用读取双精度"""
        return self.读取双精度(*args, **kwargs)

    def ReadDoubleAddr(self, *args, **kwargs):
        """英文别名，调用读取双精度地址"""
        return self.读取双精度地址(*args, **kwargs)

    def 读取浮点数(self, 窗口句柄: int, 地址: str) -> float:
        """
        函数简介:
            读取指定地址的单精度浮点数

        函数原型:
            float ReadFloat(hwnd,addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址

        返回值:
            单精度浮点数: 读取到的单精度浮点数

        示例:
            value = 读取浮点数(hwnd,"4A3B2C1D")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取浮点数: {msg}")
            return 0.0
            
        try:
            return self._dm.ReadFloat(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 读取浮点数: {str(e)}")
            return 0.0

    def 读取浮点数地址(self, 窗口句柄: int, 地址: int) -> float:
        """
        函数简介:
            读取指定地址的单精度浮点数

        函数原型:
            float ReadFloatAddr(hwnd,addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址

        返回值:
            单精度浮点数: 读取到的单精度浮点数

        示例:
            value = 读取浮点数地址(hwnd,0x4010000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取浮点数地址: {msg}")
            return 0.0
            
        try:
            return self._dm.ReadFloatAddr(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 读取浮点数地址: {str(e)}")
            return 0.0

    def 读取整数(self, 窗口句柄: int, 地址: str) -> int:
        """
        函数简介:
            读取指定地址的整数

        函数原型:
            long ReadInt(hwnd,addr,type)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址

        返回值:
            整形数: 读取到的整数

        示例:
            value = 读取整数(hwnd,"4A3B2C1D")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取整数: {msg}")
            return 0
            
        try:
            return self._dm.ReadInt(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 读取整数: {str(e)}")
            return 0

    # 添加英文别名
    def ReadFloat(self, *args, **kwargs):
        """英文别名，调用读取浮点数"""
        return self.读取浮点数(*args, **kwargs)

    def ReadFloatAddr(self, *args, **kwargs):
        """英文别名，调用读取浮点数地址"""
        return self.读取浮点数地址(*args, **kwargs)

    def ReadInt(self, *args, **kwargs):
        """英文别名，调用读取整数"""
        return self.读取整数(*args, **kwargs)

    def 读取整数地址(self, 窗口句柄: int, 地址: int) -> int:
        """
        函数简介:
            读取指定地址的整数

        函数原型:
            long ReadIntAddr(hwnd,addr,type)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址

        返回值:
            整形数: 读取到的整数

        示例:
            value = 读取整数地址(hwnd,0x4010000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取整数地址: {msg}")
            return 0
            
        try:
            return self._dm.ReadIntAddr(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 读取整数地址: {str(e)}")
            return 0

    def 读取字符串(self, 窗口句柄: int, 地址: str, 类型: int = 0) -> str:
        """
        函数简介:
            读取指定地址的字符串

        函数原型:
            string ReadString(hwnd,addr,type)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            类型 整形数: 字符串类型,取值如下:
                0: Ascii字符串
                1: Unicode字符串
                2: UTF8字符串

        返回值:
            字符串: 读取到的字符串

        示例:
            value = 读取字符串(hwnd,"4A3B2C1D",0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取字符串: {msg}")
            return ""
            
        try:
            return self._dm.ReadString(窗口句柄, 地址, 类型)
        except Exception as e:
            print(f"Error in 读取字符串: {str(e)}")
            return ""

    def 读取字符串地址(self, 窗口句柄: int, 地址: int, 类型: int = 0) -> str:
        """
        函数简介:
            读取指定地址的字符串

        函数原型:
            string ReadStringAddr(hwnd,addr,type)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            类型 整形数: 字符串类型,取值如下:
                0: Ascii字符串
                1: Unicode字符串
                2: UTF8字符串

        返回值:
            字符串: 读取到的字符串

        示例:
            value = 读取字符串地址(hwnd,0x4010000,0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取字符串地址: {msg}")
            return ""
            
        try:
            return self._dm.ReadStringAddr(窗口句柄, 地址, 类型)
        except Exception as e:
            print(f"Error in 读取字符串地址: {str(e)}")
            return ""

    # 添加英文别名
    def ReadIntAddr(self, *args, **kwargs):
        """英文别名，调用读取整数地址"""
        return self.读取整数地址(*args, **kwargs)

    def ReadString(self, *args, **kwargs):
        """英文别名，调用读取字符串"""
        return self.读取字符串(*args, **kwargs)

    def ReadStringAddr(self, *args, **kwargs):
        """英文别名，调用读取字符串地址"""
        return self.读取字符串地址(*args, **kwargs)

    def 设置内存查找结果到文件(self, 开关: int) -> int:
        """
        函数简介:
            设置是否把内存查找结果写入文件

        函数原型:
            long SetMemoryFindResultToFile(enable)

        参数定义:
            开关 整形数: 
                0: 关闭
                1: 开启

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            设置内存查找结果到文件(1)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置内存查找结果到文件: {msg}")
            return 0
            
        try:
            return self._dm.SetMemoryFindResultToFile(开关)
        except Exception as e:
            print(f"Error in 设置内存查找结果到文件: {str(e)}")
            return 0

    def 设置内存句柄为进程ID(self, 开关: int) -> int:
        """
        函数简介:
            设置是否使用进程ID来代替窗口句柄

        函数原型:
            long SetMemoryHwndAsProcessId(enable)

        参数定义:
            开关 整形数: 
                0: 关闭
                1: 开启

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            设置内存句柄为进程ID(1)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置内存句柄为进程ID: {msg}")
            return 0
            
        try:
            return self._dm.SetMemoryHwndAsProcessId(开关)
        except Exception as e:
            print(f"Error in 设置内存句柄为进程ID: {str(e)}")
            return 0

    def 字符串转数据(self, 字符串: str) -> str:
        """
        函数简介:
            把字符串转换成二进制形式

        函数原型:
            string StringToData(value,type)

        参数定义:
            字符串 字符串: 需要转化的字符串

        返回值:
            字符串: 字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

        示例:
            str_data = 字符串转数据("hello")
            dm_ret = 查找数据(hwnd,"00000000-7fffffff",str_data)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 字符串转数据: {msg}")
            return ""
            
        try:
            return self._dm.StringToData(字符串)
        except Exception as e:
            print(f"Error in 字符串转数据: {str(e)}")
            return ""

    # 添加英文别名
    def SetMemoryFindResultToFile(self, *args, **kwargs):
        """英文别名，调用设置内存查找结果到文件"""
        return self.设置内存查找结果到文件(*args, **kwargs)

    def SetMemoryHwndAsProcessId(self, *args, **kwargs):
        """英文别名，调用设置内存句柄为进程ID"""
        return self.设置内存句柄为进程ID(*args, **kwargs)

    def StringToData(self, *args, **kwargs):
        """英文别名，调用字符串转数据"""
        return self.字符串转数据(*args, **kwargs)

    def 终止进程(self, 进程ID: int) -> int:
        """
        函数简介:
            终止指定进程ID的进程

        函数原型:
            long TerminateProcess(pid)

        参数定义:
            进程ID 整形数: 进程ID

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            终止进程(1234)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 终止进程: {msg}")
            return 0
            
        try:
            return self._dm.TerminateProcess(进程ID)
        except Exception as e:
            print(f"Error in 终止进程: {str(e)}")
            return 0

    def 虚拟内存分配(self, 窗口句柄: int, 地址: int, 大小: int, 类型: int = 0) -> int:
        """
        函数简介:
            在指定进程分配内存

        函数原型:
            long VirtualAllocEx(hwnd,addr,size,type)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 要分配的地址
            大小 整形数: 要分配的大小
            类型 整形数: 分配的类型,取值如下:
                0: 保留内存
                1: 提交内存

        返回值:
            整形数: 分配的地址,失败返回0

        示例:
            addr = 虚拟内存分配(hwnd,0,1024,1)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 虚拟内存分配: {msg}")
            return 0
            
        try:
            return self._dm.VirtualAllocEx(窗口句柄, 地址, 大小, 类型)
        except Exception as e:
            print(f"Error in 虚拟内存分配: {str(e)}")
            return 0

    def 虚拟内存释放(self, 窗口句柄: int, 地址: int) -> int:
        """
        函数简介:
            释放指定进程的内存

        函数原型:
            long VirtualFreeEx(hwnd,addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 要释放的地址

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            虚拟内存释放(hwnd,0x4010000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 虚拟内存释放: {msg}")
            return 0
            
        try:
            return self._dm.VirtualFreeEx(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 虚拟内存释放: {str(e)}")
            return 0

    # 添加英文别名
    def TerminateProcess(self, *args, **kwargs):
        """英文别名，调用终止进程"""
        return self.终止进程(*args, **kwargs)

    def VirtualAllocEx(self, *args, **kwargs):
        """英文别名，调用虚拟内存分配"""
        return self.虚拟内存分配(*args, **kwargs)

    def VirtualFreeEx(self, *args, **kwargs):
        """英文别名，调用虚拟内存释放"""
        return self.虚拟内存释放(*args, **kwargs)

    def 虚拟内存保护(self, 窗口句柄: int, 地址: int, 大小: int, 属性: int) -> int:
        """
        函数简介:
            设置指定内存区域的保护属性

        函数原型:
            long VirtualProtectEx(hwnd,addr,size,type)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 要设置的地址
            大小 整形数: 要设置的大小
            属性 整形数: 要设置的属性,取值如下:
                0x1: 可执行
                0x2: 可写
                0x4: 可读
                0x8: 可写拷贝
                0x10: 可执行写
                0x20: 可执行读
                0x40: 可执行写读

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            虚拟内存保护(hwnd,0x4010000,1024,0x40)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 虚拟内存保护: {msg}")
            return 0
            
        try:
            return self._dm.VirtualProtectEx(窗口句柄, 地址, 大小, 属性)
        except Exception as e:
            print(f"Error in 虚拟内存保护: {str(e)}")
            return 0

    def 虚拟内存查询(self, 窗口句柄: int, 地址: int) -> str:
        """
        函数简介:
            查询指定地址的内存信息

        函数原型:
            string VirtualQueryEx(hwnd,addr)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 要查询的地址

        返回值:
            字符串: 内存信息,格式为"base_addr|size|protect|type"

        示例:
            info = 虚拟内存查询(hwnd,0x4010000)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 虚拟内存查询: {msg}")
            return ""
            
        try:
            return self._dm.VirtualQueryEx(窗口句柄, 地址)
        except Exception as e:
            print(f"Error in 虚拟内存查询: {str(e)}")
            return ""

    # 添加英文别名
    def VirtualProtectEx(self, *args, **kwargs):
        """英文别名，调用虚拟内存保护"""
        return self.虚拟内存保护(*args, **kwargs)

    def VirtualQueryEx(self, *args, **kwargs):
        """英文别名，调用虚拟内存查询"""
        return self.虚拟内存查询(*args, **kwargs)

    def 写入数据(self, 窗口句柄: int, 地址: str, 数据: str) -> int:
        """
        函数简介:
            在指定地址写入二进制数据

        函数原型:
            long WriteData(hwnd,addr,data)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            数据 字符串: 要写入的数据,以字符串形式描述

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入数据(hwnd,"4A3B2C1D","123456")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入数据: {msg}")
            return 0
            
        try:
            return self._dm.WriteData(窗口句柄, 地址, 数据)
        except Exception as e:
            print(f"Error in 写入数据: {str(e)}")
            return 0

    def 写入数据地址(self, 窗口句柄: int, 地址: int, 数据: str) -> int:
        """
        函数简介:
            在指定地址写入二进制数据

        函数原型:
            long WriteDataAddr(hwnd,addr,data)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            数据 字符串: 要写入的数据,以字符串形式描述

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入数据地址(hwnd,0x4010000,"123456")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入数据地址: {msg}")
            return 0
            
        try:
            return self._dm.WriteDataAddr(窗口句柄, 地址, 数据)
        except Exception as e:
            print(f"Error in 写入数据地址: {str(e)}")
            return 0

    def 写入数据地址二进制(self, 窗口句柄: int, 地址: int, 数据: str) -> int:
        """
        函数简介:
            在指定地址写入二进制数据

        函数原型:
            long WriteDataAddrFromBin(hwnd,addr,data)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            数据 字符串: 要写入的数据,以字符串形式描述

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入数据地址二进制(hwnd,0x4010000,"123456")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入数据地址二进制: {msg}")
            return 0
            
        try:
            return self._dm.WriteDataAddrFromBin(窗口句柄, 地址, 数据)
        except Exception as e:
            print(f"Error in 写入数据地址二进制: {str(e)}")
            return 0

    # 添加英文别名
    def WriteData(self, *args, **kwargs):
        """英文别名，调用写入数据"""
        return self.写入数据(*args, **kwargs)

    def WriteDataAddr(self, *args, **kwargs):
        """英文别名，调用写入数据地址"""
        return self.写入数据地址(*args, **kwargs)

    def WriteDataAddrFromBin(self, *args, **kwargs):
        """英文别名，调用写入数据地址二进制"""
        return self.写入数据地址二进制(*args, **kwargs)

    def 写入数据二进制(self, 窗口句柄: int, 地址: str, 数据: str) -> int:
        """
        函数简介:
            在指定地址写入二进制数据

        函数原型:
            long WriteDataFromBin(hwnd,addr,data)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            数据 字符串: 要写入的数据,以字符串形式描述

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入数据二进制(hwnd,"4A3B2C1D","123456")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入数据二进制: {msg}")
            return 0
            
        try:
            return self._dm.WriteDataFromBin(窗口句柄, 地址, 数据)
        except Exception as e:
            print(f"Error in 写入数据二进制: {str(e)}")
            return 0

    def 写入双精度(self, 窗口句柄: int, 地址: str, 值: float) -> int:
        """
        函数简介:
            在指定地址写入双精度浮点数

        函数原型:
            long WriteDouble(hwnd,addr,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            值 双精度浮点数: 要写入的双精度浮点数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入双精度(hwnd,"4A3B2C1D",1.23)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入双精度: {msg}")
            return 0
            
        try:
            return self._dm.WriteDouble(窗口句柄, 地址, 值)
        except Exception as e:
            print(f"Error in 写入双精度: {str(e)}")
            return 0

    def 写入双精度地址(self, 窗口句柄: int, 地址: int, 值: float) -> int:
        """
        函数简介:
            在指定地址写入双精度浮点数

        函数原型:
            long WriteDoubleAddr(hwnd,addr,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            值 双精度浮点数: 要写入的双精度浮点数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入双精度地址(hwnd,0x4010000,1.23)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入双精度地址: {msg}")
            return 0
            
        try:
            return self._dm.WriteDoubleAddr(窗口句柄, 地址, 值)
        except Exception as e:
            print(f"Error in 写入双精度地址: {str(e)}")
            return 0

    # 添加英文别名
    def WriteDataFromBin(self, *args, **kwargs):
        """英文别名，调用写入数据二进制"""
        return self.写入数据二进制(*args, **kwargs)

    def WriteDouble(self, *args, **kwargs):
        """英文别名，调用写入双精度"""
        return self.写入双精度(*args, **kwargs)

    def WriteDoubleAddr(self, *args, **kwargs):
        """英文别名，调用写入双精度地址"""
        return self.写入双精度地址(*args, **kwargs)

    def 写入浮点数(self, 窗口句柄: int, 地址: str, 值: float) -> int:
        """
        函数简介:
            在指定地址写入单精度浮点数

        函数原型:
            long WriteFloat(hwnd,addr,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            值 单精度浮点数: 要写入的单精度浮点数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入浮点数(hwnd,"4A3B2C1D",1.23)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入浮点数: {msg}")
            return 0
            
        try:
            return self._dm.WriteFloat(窗口句柄, 地址, 值)
        except Exception as e:
            print(f"Error in 写入浮点数: {str(e)}")
            return 0

    def 写入浮点数地址(self, 窗口句柄: int, 地址: int, 值: float) -> int:
        """
        函数简介:
            在指定地址写入单精度浮点数

        函数原型:
            long WriteFloatAddr(hwnd,addr,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            值 单精度浮点数: 要写入的单精度浮点数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入浮点数地址(hwnd,0x4010000,1.23)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入浮点数地址: {msg}")
            return 0
            
        try:
            return self._dm.WriteFloatAddr(窗口句柄, 地址, 值)
        except Exception as e:
            print(f"Error in 写入浮点数地址: {str(e)}")
            return 0

    def 写入整数(self, 窗口句柄: int, 地址: str, 值: int) -> int:
        """
        函数简介:
            在指定地址写入整数

        函数原型:
            long WriteInt(hwnd,addr,type,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            值 整形数: 要写入的整数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入整数(hwnd,"4A3B2C1D",100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入整数: {msg}")
            return 0
            
        try:
            return self._dm.WriteInt(窗口句柄, 地址, 值)
        except Exception as e:
            print(f"Error in 写入整数: {str(e)}")
            return 0

    # 添加英文别名
    def WriteFloat(self, *args, **kwargs):
        """英文别名，调用写入浮点数"""
        return self.写入浮点数(*args, **kwargs)

    def WriteFloatAddr(self, *args, **kwargs):
        """英文别名，调用写入浮点数地址"""
        return self.写入浮点数地址(*args, **kwargs)

    def WriteInt(self, *args, **kwargs):
        """英文别名，调用写入整数"""
        return self.写入整数(*args, **kwargs)

    def 写入整数地址(self, 窗口句柄: int, 地址: int, 值: int) -> int:
        """
        函数简介:
            在指定地址写入整数

        函数原型:
            long WriteIntAddr(hwnd,addr,type,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            值 整形数: 要写入的整数

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入整数地址(hwnd,0x4010000,100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入整数地址: {msg}")
            return 0
            
        try:
            return self._dm.WriteIntAddr(窗口句柄, 地址, 值)
        except Exception as e:
            print(f"Error in 写入整数地址: {str(e)}")
            return 0

    def 写入字符串(self, 窗口句柄: int, 地址: str, 字符串: str, 类型: int = 0) -> int:
        """
        函数简介:
            在指定地址写入字符串

        函数原型:
            long WriteString(hwnd,addr,type,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 字符串: 地址
            字符串 字符串: 要写入的字符串
            类型 整形数: 字符串类型,取值如下:
                0: Ascii字符串
                1: Unicode字符串
                2: UTF8字符串

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入字符串(hwnd,"4A3B2C1D","hello",0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入字符串: {msg}")
            return 0
            
        try:
            return self._dm.WriteString(窗口句柄, 地址, 类型, 字符串)
        except Exception as e:
            print(f"Error in 写入字符串: {str(e)}")
            return 0

    def 写入字符串地址(self, 窗口句柄: int, 地址: int, 字符串: str, 类型: int = 0) -> int:
        """
        函数简介:
            在指定地址写入字符串

        函数原型:
            long WriteStringAddr(hwnd,addr,type,v)

        参数定义:
            窗口句柄 整形数: 窗口句柄
            地址 整形数: 地址
            字符串 字符串: 要写入的字符串
            类型 整形数: 字符串类型,取值如下:
                0: Ascii字符串
                1: Unicode字符串
                2: UTF8字符串

        返回值:
            整形数: 
                0: 失败
                1: 成功

        示例:
            写入字符串地址(hwnd,0x4010000,"hello",0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入字符串地址: {msg}")
            return 0
            
        try:
            return self._dm.WriteStringAddr(窗口句柄, 地址, 类型, 字符串)
        except Exception as e:
            print(f"Error in 写入字符串地址: {str(e)}")
            return 0

    # 添加英文别名
    def WriteIntAddr(self, *args, **kwargs):
        """英文别名，调用写入整数地址"""
        return self.写入整数地址(*args, **kwargs)

    def WriteString(self, *args, **kwargs):
        """英文别名，调用写入字符串"""
        return self.写入字符串(*args, **kwargs)

    def WriteStringAddr(self, *args, **kwargs):
        """英文别名，调用写入字符串地址"""
        return self.写入字符串地址(*args, **kwargs) 