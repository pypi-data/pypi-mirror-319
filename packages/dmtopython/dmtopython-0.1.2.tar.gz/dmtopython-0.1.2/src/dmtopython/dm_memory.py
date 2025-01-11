import win32com.client

class DmMemory:
    def __init__(self, dm=None, code=None, key=None):
        if dm:
            self._dm = dm
        else:
            self._dm = win32com.client.Dispatch('dm.dmsoft')
            if code and key:
                self._dm.Reg(code, key)
        
    def ReadData(self, hwnd, addr, length):
        """函数简介:
        读取指定地址的二进制数据
        
        函数原型:
        string ReadData(hwnd,addr,len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述，数值必须是16进制,里面可以用[ ] + -这些符号来描述一个地址。
        len 整形数: 二进制数据的长度
        
        返回值:
        字符串: 读取到的数值,以16进制表示的字符串 每个字节以空格相隔 比如"12 34 56 78 ab cd ef"
        """
        return self._dm.ReadData(hwnd, addr, length)
        
    def ReadDataAddr(self, hwnd, addr, length):
        """函数简介:
        读取指定地址的二进制数据
        
        函数原型:
        string ReadDataAddr(hwnd,addr,len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        len 整形数: 二进制数据的长度
        
        返回值:
        字符串: 读取到的数值,以16进制表示的字符串 每个字节以空格相隔
        """
        return self._dm.ReadDataAddr(hwnd, addr, length)
        
    def ReadDataToBin(self, hwnd, addr, length):
        """函数简介:
        读取指定地址的二进制数据,只不过返回的是内存地址,而不是字符串
        
        函数原型:
        long ReadDataToBin(hwnd,addr,len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 地址字符串
        len 整形数: 二进制数据的长度
        
        返回值:
        整形数: 读取到的数据指针. 返回0表示读取失败
        """
        return self._dm.ReadDataToBin(hwnd, addr, length)
        
    def ReadDataAddrToBin(self, hwnd, addr, length):
        """函数简介:
        读取指定地址的二进制数据,只不过返回的是内存地址,而不是字符串
        
        函数原型:
        long ReadDataAddrToBin(hwnd,addr,len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        len 整形数: 二进制数据的长度
        
        返回值:
        整形数: 读取到的数据指针. 返回0表示读取失败
        """
        return self._dm.ReadDataAddrToBin(hwnd, addr, length)
        
    def ReadDouble(self, hwnd, addr):
        """函数简介:
        读取指定地址的双精度浮点数
        
        函数原型:
        double ReadDouble(hwnd,addr)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 地址字符串
        
        返回值:
        双精度浮点数: 读取到的数值
        """
        return self._dm.ReadDouble(hwnd, addr)
        
    def ReadDoubleAddr(self, hwnd, addr):
        """函数简介:
        读取指定地址的双精度浮点数
        
        函数原型:
        double ReadDoubleAddr(hwnd,addr)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        
        返回值:
        双精度浮点数: 读取到的数值
        """
        return self._dm.ReadDoubleAddr(hwnd, addr)
        
    def ReadFloat(self, hwnd, addr):
        """函数简介:
        读取指定地址的单精度浮点数
        
        函数原型:
        float ReadFloat(hwnd,addr)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 地址字符串
        
        返回值:
        单精度浮点数: 读取到的数值
        """
        return self._dm.ReadFloat(hwnd, addr)
        
    def ReadFloatAddr(self, hwnd, addr):
        """函数简介:
        读取指定地址的单精度浮点数
        
        函数原型:
        float ReadFloatAddr(hwnd,addr)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        
        返回值:
        单精度浮点数: 读取到的数值
        """
        return self._dm.ReadFloatAddr(hwnd, addr)
        
    def FindDataEx(self, hwnd, addr_range, data, step, multi_thread, mode):
        """函数简介:
        搜索指定的二进制数据.
        
        函数原型:
        string FindDataEx(hwnd, addr_range, data, step, multi_thread, mode)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合，可以是上次FindXXX的返回地址集合或地址范围
        data 字符串: 要搜索的二进制数据,如"00 01 23 45 67 86 ab ce f1"
        step 整形数: 搜索步长
        multi_thread整形数: 是否开启多线程查找. 0不开启，1开启
        mode 整形数: 1表示开启快速扫描(略过只读内存) 0表示所有内存类型全部扫描
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindDataEx(hwnd, addr_range, data, step, multi_thread, mode)
        
    def FindDouble(self, hwnd, addr_range, double_value_min, double_value_max):
        """函数简介:
        搜索指定的双精度浮点数
        
        函数原型:
        string FindDouble(hwnd, addr_range, double_value_min, double_value_max)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        double_value_min 双精度浮点数: 搜索的双精度数值最小值
        double_value_max 双精度浮点数: 搜索的双精度数值最大值
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindDouble(hwnd, addr_range, double_value_min, double_value_max)
        
    def FindFloat(self, hwnd, addr_range, float_value_min, float_value_max):
        """函数简介:
        搜索指定的单精度浮点数
        
        函数原型:
        string FindFloat(hwnd, addr_range, float_value_min, float_value_max)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        float_value_min 单精度浮点数: 搜索的单精度数值最小值
        float_value_max 单精度浮点数: 搜索的单精度数值最大值
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindFloat(hwnd, addr_range, float_value_min, float_value_max)
        
    def FindInt(self, hwnd, addr_range, int_value_min, int_value_max, type):
        """函数简介:
        搜索指定的整数
        
        函数原型:
        string FindInt(hwnd, addr_range, int_value_min, int_value_max, type)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        int_value_min 长整形数: 搜索的整数最小值
        int_value_max 长整形数: 搜索的整数最大值
        type 整形数: 整数类型,0:32位 1:16位 2:8位 3:64位
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindInt(hwnd, addr_range, int_value_min, int_value_max, type)
        
    def FindString(self, hwnd, addr_range, string_value, type):
        """函数简介:
        搜索指定的字符串
        
        函数原型:
        string FindString(hwnd, addr_range, string_value, type)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        string_value 字符串: 搜索的字符串
        type 整形数: 字符串类型,0:Ascii 1:Unicode 2:UTF8
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindString(hwnd, addr_range, string_value, type)
        
    def WriteData(self, hwnd, addr, data):
        """函数简介:
        对指定地址写入二进制数据
        
        函数原型:
        long WriteData(hwnd,addr,data)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        data 字符串: 二进制数据，以字符串形式描述，如"12 34 56 78 90 ab cd"
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteData(hwnd, addr, data)
        
    def WriteDataAddr(self, hwnd, addr, data):
        """函数简介:
        对指定地址写入二进制数据
        
        函数原型:
        long WriteDataAddr(hwnd,addr,data)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        data 字符串: 二进制数据，以字符串形式描述，如"12 34 56 78 90 ab cd"
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteDataAddr(hwnd, addr, data)
        
    def WriteDouble(self, hwnd, addr, v):
        """函数简介:
        对指定地址写入双精度浮点数
        
        函数原型:
        long WriteDouble(hwnd,addr,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        v 双精度浮点数: 双精度浮点数
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteDouble(hwnd, addr, v)
        
    def WriteDoubleAddr(self, hwnd, addr, v):
        """函数简介:
        对指定地址写入双精度浮点数
        
        函数原型:
        long WriteDoubleAddr(hwnd,addr,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        v 双精度浮点数: 双精度浮点数
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteDoubleAddr(hwnd, addr, v)
        
    def WriteFloat(self, hwnd, addr, v):
        """函数简介:
        对指定地址写入单精度浮点数
        
        函数原型:
        long WriteFloat(hwnd,addr,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        v 单精度浮点数: 单精度浮点数
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteFloat(hwnd, addr, v)
        
    def WriteFloatAddr(self, hwnd, addr, v):
        """函数简介:
        对指定地址写入单精度浮点数
        
        函数原型:
        long WriteFloatAddr(hwnd,addr,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        v 单精度浮点数: 单精度浮点数
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteFloatAddr(hwnd, addr, v)
        
    def WriteString(self, hwnd, addr, type, v):
        """函数简介:
        对指定地址写入字符串
        
        函数原型:
        long WriteString(hwnd,addr,type,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        type 整形数: 字符串类型,0:Ascii 1:Unicode 2:UTF8
        v 字符串: 要写入的字符串
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteString(hwnd, addr, type, v)
        
    def WriteStringAddr(self, hwnd, addr, type, v):
        """函数简介:
        对指定地址写入字符串
        
        函数原型:
        long WriteStringAddr(hwnd,addr,type,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        type 整形数: 字符串类型,0:Ascii 1:Unicode 2:UTF8
        v 字符串: 要写入的字符串
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteStringAddr(hwnd, addr, type, v)
        
    def VirtualAllocEx(self, hwnd, addr, size, type):
        """函数简介:
        在指定的窗口所在进程分配一段内存
        
        函数原型:
        LONGLONG VirtualAllocEx(hwnd,addr,size,type)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 预期的分配地址。0表示自动分配
        size 整形数: 需要分配的内存大小
        type 整形数: 内存类型,0:可读可写可执行 1:可读可执行不可写 2:可读可写不可执行
        
        返回值:
        长整形数: 分配的内存地址，0表示分配失败
        """
        return self._dm.VirtualAllocEx(hwnd, addr, size, type)
        
    def VirtualFreeEx(self, hwnd, addr):
        """函数简介:
        释放用VirtualAllocEx分配的内存
        
        函数原型:
        long VirtualFreeEx(hwnd,addr)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: VirtualAllocEx返回的地址
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.VirtualFreeEx(hwnd, addr)
        
    def VirtualProtectEx(self, hwnd, addr, size, type, old_protect):
        """函数简介:
        修改指定的窗口所在进程的地址的读写属性
        
        函数原型:
        long VirtualProtectEx(hwnd,addr,size,type,old_protect)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 需要修改的地址
        size 整形数: 需要修改的地址大小
        type 整形数: 0:可读可写可执行 1:修改为old_protect指定的读写属性
        old_protect 整形数: 指定的读写属性
        
        返回值:
        整形数: 0:失败 其他:修改之前的读写属性
        """
        return self._dm.VirtualProtectEx(hwnd, addr, size, type, old_protect)
        
    def VirtualQueryEx(self, hwnd, addr, pmbi):
        """函数简介:
        获取指定窗口，指定地址的内存属性
        
        函数原型:
        string VirtualQueryEx(hwnd,addr,pmbi)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 需要查询的地址
        pmbi 整形数: MEMORY_BASIC_INFORMATION结构体地址,可为0
        
        返回值:
        字符串: 查询结果,格式为"BaseAddress,AllocationBase,AllocationProtect,RegionSize,State,Protect,Type"
        """
        return self._dm.VirtualQueryEx(hwnd, addr, pmbi)
        
    def SetMemoryHwndAsProcessId(self, en):
        """函数简介:
        设置是否把所有内存接口函数中的窗口句柄当作进程ID
        
        函数原型:
        long SetMemoryHwndAsProcessId(en)
        
        参数定义:
        en 整形数: 0:关闭 1:开启
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.SetMemoryHwndAsProcessId(en)
        
    def SetMemoryFindResultToFile(self, file):
        """函数简介:
        设置是否把所有内存查找接口的结果保存入指定文件
        
        函数原型:
        long SetMemoryFindResultToFile(file)
        
        参数定义:
        file 字符串: 要保存的搜索结果文件名,空字符串表示取消此功能
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.SetMemoryFindResultToFile(file)
        
    def OpenProcess(self, pid):
        """函数简介:
        根据指定pid打开进程，并返回进程句柄
        
        函数原型:
        long OpenProcess(pid)
        
        参数定义:
        pid 整形数: 进程pid
        
        返回值:
        整形数: 进程句柄,0表示失败
        """
        return self._dm.OpenProcess(pid)
        
    def TerminateProcess(self, pid):
        """函数简介:
        根据指定的PID，强制结束进程
        
        函数原型:
        long TerminateProcess(pid)
        
        参数定义:
        pid 整形数: 进程ID
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.TerminateProcess(pid)
        
    def TerminateProcessTree(self, pid):
        """函数简介:
        根据指定的PID，强制结束进程以及此进程创建的所有子进程
        
        函数原型:
        long TerminateProcessTree(pid)
        
        参数定义:
        pid 整形数: 进程ID
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.TerminateProcessTree(pid)
        
    def GetCommandLine(self, hwnd):
        """函数简介:
        获取指定窗口所在进程的启动命令行
        
        函数原型:
        string GetCommandLine(hwnd)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        
        返回值:
        字符串: 读取到的启动命令行
        """
        return self._dm.GetCommandLine(hwnd)
        
    def GetModuleBaseAddr(self, hwnd, module):
        """函数简介:
        根据指定的窗口句柄，来获取对应窗口句柄进程下的指定模块的基址
        
        函数原型:
        LONGLONG GetModuleBaseAddr(hwnd,module)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        module 字符串: 模块名
        
        返回值:
        长整形数: 模块的基址
        """
        return self._dm.GetModuleBaseAddr(hwnd, module)
        
    def GetModuleSize(self, hwnd, module):
        """函数简介:
        根据指定的窗口句柄，来获取对应窗口句柄进程下的指定模块的大小
        
        函数原型:
        long GetModuleSize(hwnd,module)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        module 字符串: 模块名
        
        返回值:
        整形数: 模块的大小
        """
        return self._dm.GetModuleSize(hwnd, module)
        
    def FreeProcessMemory(self, hwnd):
        """函数简介:
        释放指定进程的不常用内存
        
        函数原型:
        long FreeProcessMemory(hwnd)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.FreeProcessMemory(hwnd)
        
    def ReadInt(self, hwnd, addr, type):
        """函数简介:
        读取指定地址的整数数值
        
        函数原型:
        LONGLONG ReadInt(hwnd,addr,type)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        type 整形数: 整数类型,0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
        
        返回值:
        长整形数: 读取到的数值
        """
        return self._dm.ReadInt(hwnd, addr, type)
        
    def ReadIntAddr(self, hwnd, addr, type):
        """函数简介:
        读取指定地址的整数数值
        
        函数原型:
        LONGLONG ReadIntAddr(hwnd,addr,type)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        type 整形数: 整数类型,0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
        
        返回值:
        长整形数: 读取到的数值
        """
        return self._dm.ReadIntAddr(hwnd, addr, type)
        
    def WriteInt(self, hwnd, addr, type, v):
        """函数简介:
        对指定地址写入整数数值
        
        函数原型:
        long WriteInt(hwnd,addr,type,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        type 整形数: 整数类型,0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
        v 长整形数: 要写入的数值
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteInt(hwnd, addr, type, v)
        
    def WriteIntAddr(self, hwnd, addr, type, v):
        """函数简介:
        对指定地址写入整数数值
        
        函数原型:
        long WriteIntAddr(hwnd,addr,type,v)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        type 整形数: 整数类型,0:32位有符号 1:16位有符号 2:8位有符号 3:64位 4:32位无符号 5:16位无符号 6:8位无符号
        v 长整形数: 要写入的数值
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteIntAddr(hwnd, addr, type, v)
        
    def FloatToData(self, value):
        """函数简介:
        把单精度浮点数转换成二进制形式
        
        函数原型:
        string FloatToData(value)
        
        参数定义:
        value 单精度浮点数: 需要转化的单精度浮点数
        
        返回值:
        字符串: 字符串形式表达的二进制数据
        """
        return self._dm.FloatToData(value)
        
    def IntToData(self, value, type):
        """函数简介:
        把整数转换成二进制形式
        
        函数原型:
        string IntToData(value,type)
        
        参数定义:
        value 长整形数: 需要转化的整型数
        type 整形数: 0:4字节 1:2字节 2:1字节 3:8字节
        
        返回值:
        字符串: 字符串形式表达的二进制数据
        """
        return self._dm.IntToData(value, type)
        
    def StringToData(self, value, type):
        """函数简介:
        把字符串转换成二进制形式
        
        函数原型:
        string StringToData(value,type)
        
        参数定义:
        value 字符串: 需要转化的字符串
        type 整形数: 0:Ascii 1:Unicode
        
        返回值:
        字符串: 字符串形式表达的二进制数据
        """
        return self._dm.StringToData(value, type)
        
    def FindDoubleEx(self, hwnd, addr_range, double_value_min, double_value_max, step, multi_thread, mode):
        """函数简介:
        搜索指定的双精度浮点数
        
        函数原型:
        string FindDoubleEx(hwnd, addr_range, double_value_min, double_value_max, step, multi_thread, mode)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        double_value_min 双精度浮点数: 搜索的双精度数值最小值
        double_value_max 双精度浮点数: 搜索的双精度数值最大值
        step 整形数: 搜索步长
        multi_thread 整形数: 是否开启多线程,0不开启,1开启
        mode 整形数: 1表示开启快速扫描(略过只读内存) 0表示所有内存类型全部扫描
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindDoubleEx(hwnd, addr_range, double_value_min, double_value_max, step, multi_thread, mode)
        
    def FindFloatEx(self, hwnd, addr_range, float_value_min, float_value_max, step, multi_thread, mode):
        """函数简介:
        搜索指定的单精度浮点数
        
        函数原型:
        string FindFloatEx(hwnd, addr_range, float_value_min, float_value_max, step, multi_thread, mode)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        float_value_min 单精度浮点数: 搜索的单精度数值最小值
        float_value_max 单精度浮点数: 搜索的单精度数值最大值
        step 整形数: 搜索步长
        multi_thread 整形数: 是否开启多线程,0不开启,1开启
        mode 整形数: 1表示开启快速扫描(略过只读内存) 0表示所有内存类型全部扫描
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindFloatEx(hwnd, addr_range, float_value_min, float_value_max, step, multi_thread, mode)
        
    def FindIntEx(self, hwnd, addr_range, int_value_min, int_value_max, type, step, multi_thread, mode):
        """函数简介:
        搜索指定的整数
        
        函数原型:
        string FindIntEx(hwnd, addr_range, int_value_min, int_value_max, type, step, multi_thread, mode)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        int_value_min 长整形数: 搜索的整数最小值
        int_value_max 长整形数: 搜索的整数最大值
        type 整形数: 整数类型,0:32位 1:16位 2:8位 3:64位
        step 整形数: 搜索步长
        multi_thread 整形数: 是否开启多线程,0不开启,1开启
        mode 整形数: 1表示开启快速扫描(略过只读内存) 0表示所有内存类型全部扫描
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindIntEx(hwnd, addr_range, int_value_min, int_value_max, type, step, multi_thread, mode)
        
    def FindStringEx(self, hwnd, addr_range, string_value, type, step, multi_thread, mode):
        """函数简介:
        搜索指定的字符串
        
        函数原型:
        string FindStringEx(hwnd, addr_range, string_value, type, step, multi_thread, mode)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        string_value 字符串: 搜索的字符串
        type 整形数: 字符串类型,0:Ascii 1:Unicode 2:UTF8
        step 整形数: 搜索步长
        multi_thread 整形数: 是否开启多线程,0不开启,1开启
        mode 整形数: 1表示开启快速扫描(略过只读内存) 0表示所有内存类型全部扫描
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindStringEx(hwnd, addr_range, string_value, type, step, multi_thread, mode)
        
    def WriteDataAddrFromBin(self, hwnd, addr, data, length):
        """函数简介:
        对指定地址写入二进制数据,直接从数据指针获取数据写入
        
        函数原型:
        long WriteDataAddrFromBin(hwnd, addr, data, len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        data 整形数: 数据指针
        len 整形数: 数据长度
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteDataAddrFromBin(hwnd, addr, data, length)
        
    def SetParam64ToPointer(self):
        """函数简介:
        这个接口是给E语言设计的,用于兼容长整数的处理
        
        函数原型:
        long SetParam64ToPointer()
        
        参数定义:
        无
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.SetParam64ToPointer()
        
    def Int64ToInt32(self, value):
        """函数简介:
        强制转换64位整数为32位
        
        函数原型:
        long Int64ToInt32(value)
        
        参数定义:
        value 长整形数: 需要转换的64位整数
        
        返回值:
        整形数: 返回的32位整数
        """
        return self._dm.Int64ToInt32(value)
        
    def DoubleToData(self, value):
        """函数简介:
        把双精度浮点数转换成二进制形式
        
        函数原型:
        string DoubleToData(value)
        
        参数定义:
        value 双精度浮点数: 需要转化的双精度浮点数
        
        返回值:
        字符串: 字符串形式表达的二进制数据
        """
        return self._dm.DoubleToData(value)
        
    def FindData(self, hwnd, addr_range, data):
        """函数简介:
        搜索指定的二进制数据,默认步长是1
        
        函数原型:
        string FindData(hwnd, addr_range, data)
        
        参数定义:
        hwnd 整形数: 指定搜索的窗口句柄或者进程ID
        addr_range 字符串: 指定搜索的地址集合
        data 字符串: 要搜索的二进制数据,如"00 01 23 45 67 86 ab ce f1"
        
        返回值:
        字符串: 返回搜索到的地址集合，格式如"addr1|addr2|addr3"
        """
        return self._dm.FindData(hwnd, addr_range, data)
        
    def GetRemoteApiAddress(self, hwnd, base_addr, fun_name):
        """函数简介:
        根据指定的目标模块地址,获取目标窗口(进程)内的导出函数地址
        
        函数原型:
        LONGLONG GetRemoteApiAddress(hwnd,base_addr,fun_name)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        base_addr 长整形数: 目标模块地址
        fun_name 字符串: 需要获取的导出函数名
        
        返回值:
        长整形数: 获取的地址,0表示失败
        """
        return self._dm.GetRemoteApiAddress(hwnd, base_addr, fun_name)
        
    def WriteDataFromBin(self, hwnd, addr, data, length):
        """函数简介:
        对指定地址写入二进制数据,直接从数据指针获取数据写入
        
        函数原型:
        long WriteDataFromBin(hwnd, addr, data, len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        data 整形数: 数据指针
        len 整形数: 数据长度
        
        返回值:
        整形数: 0:失败 1:成功
        """
        return self._dm.WriteDataFromBin(hwnd, addr, data, length)
        
    def ReadString(self, hwnd, addr, type, length=0):
        """函数简介:
        读取指定地址的字符串
        
        函数原型:
        string ReadString(hwnd,addr,type,len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 字符串: 用字符串来描述地址，类似于CE的地址描述
        type 整形数: 字符串类型,0:GBK 1:Unicode 2:UTF8
        len 整形数: 需要读取的字节数目,0表示自动判定
        
        返回值:
        字符串: 读取到的字符串
        """
        return self._dm.ReadString(hwnd, addr, type, length)
        
    def ReadStringAddr(self, hwnd, addr, type, length=0):
        """函数简介:
        读取指定地址的字符串
        
        函数原型:
        string ReadStringAddr(hwnd,addr,type,len)
        
        参数定义:
        hwnd 整形数: 窗口句柄或者进程ID
        addr 长整形数: 地址
        type 整形数: 字符串类型,0:GBK 1:Unicode 2:UTF8
        len 整形数: 需要读取的字节数目,0表示自动判定
        
        返回值:
        字符串: 读取到的字符串
        """
        return self._dm.ReadStringAddr(hwnd, addr, type, length)
        
    # 添加中文别名
    读取数据 = ReadData
    读取数据_地址 = ReadDataAddr
    读取数据到指针 = ReadDataToBin
    读取数据到指针_地址 = ReadDataAddrToBin
    读取双精度浮点数 = ReadDouble
    读取双精度浮点数_地址 = ReadDoubleAddr
    读取单精度浮点数 = ReadFloat
    读取单精度浮点数_地址 = ReadFloatAddr
    读取整数 = ReadInt
    读取整数_地址 = ReadIntAddr
    查找数据Ex = FindDataEx
    查找双精度浮点数 = FindDouble
    查找单精度浮点数 = FindFloat
    查找整数 = FindInt
    查找字符串 = FindString
    写入数据 = WriteData
    写入数据_地址 = WriteDataAddr
    写入双精度浮点数 = WriteDouble
    写入双精度浮点数_地址 = WriteDoubleAddr
    写入单精度浮点数 = WriteFloat
    写入单精度浮点数_地址 = WriteFloatAddr
    写入整数 = WriteInt
    写入整数_地址 = WriteIntAddr
    写入字符串 = WriteString
    写入字符串_地址 = WriteStringAddr
    分配内存 = VirtualAllocEx
    释放内存 = VirtualFreeEx
    修改内存属性 = VirtualProtectEx
    查询内存属性 = VirtualQueryEx
    设置进程ID模式 = SetMemoryHwndAsProcessId
    设置查找结果保存 = SetMemoryFindResultToFile
    打开进程 = OpenProcess
    结束进程 = TerminateProcess
    结束进程树 = TerminateProcessTree
    获取命令行 = GetCommandLine
    获取模块基址 = GetModuleBaseAddr
    获取模块大小 = GetModuleSize
    释放进程内存 = FreeProcessMemory
    浮点数转数据 = FloatToData
    整数转数据 = IntToData
    字符串转数据 = StringToData
    查找双精度浮点数Ex = FindDoubleEx
    查找单精度浮点数Ex = FindFloatEx
    查找整数Ex = FindIntEx
    查找字符串Ex = FindStringEx
    写入数据从指针 = WriteDataAddrFromBin
    设置64位参数转指针 = SetParam64ToPointer
    转换64位到32位 = Int64ToInt32
    双精度浮点数转数据 = DoubleToData
    查找数据 = FindData
    获取远程API地址 = GetRemoteApiAddress
    写入数据从指针_地址 = WriteDataFromBin
    读取字符串 = ReadString
    读取字符串_地址 = ReadStringAddr 