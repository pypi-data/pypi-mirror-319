import win32com.client

class DmSystem:
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
        
    def Beep(self, f, duration):
        """函数简介:
        蜂鸣器.
        
        函数原型:
        long Beep(f,duration)
        
        参数定义:
        f 整形数: 频率
        duration 整形数: 时长(ms).
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.Beep 1000,1000
        """
        return self._dm.Beep(f, duration)
        
    def CheckFontSmooth(self):
        """函数简介:
        检测当前系统是否有开启屏幕字体平滑.
        
        函数原型:
        long CheckFontSmooth()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 系统没开启平滑字体.
        1 : 系统有开启平滑字体.
        
        示例:
        if dm.CheckFontSmooth() = 1 then
            TracePrint "当前系统有开启平滑字体"
        end if
        """
        return self._dm.CheckFontSmooth()
        
    def CheckUAC(self):
        """函数简介:
        检测当前系统是否有开启UAC(用户账户控制).
        
        函数原型:
        long CheckUAC()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 没开启UAC
        1 : 开启了UAC
        
        示例:
        if dm.CheckUAC() = 1 then
            TracePrint "当前系统开启了用户账户控制"
        end if
        
        注: 只有WIN7 WIN8 VISTA WIN2008以及以上系统才有UAC设置
        """
        return self._dm.CheckUAC()
        
    def Delay(self, mis):
        """函数简介:
        延时指定的毫秒,过程中不阻塞UI操作. 一般高级语言使用.按键用不到.
        
        函数原型:
        long Delay(mis)
        
        参数定义:
        mis整形数: 毫秒数. 必须大于0.
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.Delay 1000
        
        注: 由于是com组件,调用此函数必须保证调用线程的模型为MTA.否则此函数可能会失效.
        """
        return self._dm.Delay(mis)
        
    def Delays(self, mis_min, mis_max):
        """函数简介:
        延时指定范围内随机毫秒,过程中不阻塞UI操作. 一般高级语言使用.按键用不到.
        
        函数原型:
        long Delays(mis_min,mis_max)
        
        参数定义:
        mis_min整形数: 最小毫秒数. 必须大于0
        mis_max整形数: 最大毫秒数. 必须大于0
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.Delays 200,1000
        
        注: 由于是com组件,调用此函数必须保证调用线程的模型为MTA.否则此函数可能会失效.
        """
        return self._dm.Delays(mis_min, mis_max)
        
    def DisableCloseDisplayAndSleep(self):
        """函数简介:
        设置当前的电源设置，禁止关闭显示器，禁止关闭硬盘，禁止睡眠，禁止待机. 不支持XP.
        
        函数原型:
        long DisableCloseDisplayAndSleep()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.DisableCloseDisplayAndSleep
        """
        return self._dm.DisableCloseDisplayAndSleep()
        
    def DisableFontSmooth(self):
        """函数简介:
        关闭当前系统屏幕字体平滑.同时关闭系统的ClearType功能.
        
        函数原型:
        long DisableFontSmooth()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        if dm.CheckFontSmooth() = 1 then
            if dm.DisableFontSmooth() = 1 then
                MessageBox "关闭了当前系统平滑字体,重启生效"
                dm.ExitOs 2
                Delay 2000
                EndScript
            end if
        end if
        
        注: 关闭之后要让系统生效，必须重启系统才有效.
        """
        return self._dm.DisableFontSmooth()
        
    def DisablePowerSave(self):
        """函数简介:
        关闭电源管理，不会进入睡眠.
        
        函数原型:
        long DisablePowerSave()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.DisablePowerSave
        
        注: 此函数调用以后，并不会更改系统电源设置. 
        此函数经常用在后台操作过程中. 避免被系统干扰.
        """
        return self._dm.DisablePowerSave()
        
    def DisableScreenSave(self):
        """函数简介:
        关闭屏幕保护.
        
        函数原型:
        long DisableScreenSave()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.DisableScreenSave
        
        注: 调用此函数后，可能在系统中还是看到屏保是开启状态。但实际上屏保已经失效了.
        系统重启后，会失效。必须再重新调用一次.
        此函数经常用在后台操作过程中. 避免被系统干扰.
        """
        return self._dm.DisableScreenSave()
        
    def EnableFontSmooth(self):
        """函数简介:
        开启当前系统屏幕字体平滑.同时开启系统的ClearType功能.
        
        函数原型:
        long EnableFontSmooth()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        if dm.CheckFontSmooth() = 0 then
            if dm.EnableFontSmooth() = 1 then
                MessageBox "开启了当前系统平滑字体,重启生效"
                dm.ExitOs 2
                Delay 2000
                EndScript
            end if
        end if
        
        注: 开启之后要让系统生效，必须重启系统才有效.
        """
        return self._dm.EnableFontSmooth()
        
    def ExitOs(self, type):
        """函数简介:
        退出系统(注销 重启 关机)
        
        函数原型:
        long ExitOs(type)
        
        参数定义:
        type 整形数: 取值为以下类型
        0 : 注销系统
        1 : 关机
        2 : 重新启动
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm_ret = dm.ExitOs(1)
        """
        return self._dm.ExitOs(type)
        
    def GetClipboard(self):
        """函数简介:
        获取剪贴板的内容
        
        函数原型:
        string GetClipboard()
        
        参数定义:
        
        返回值:
        字符串:
        以字符串表示的剪贴板内容
        
        示例:
        TracePrint dm.GetClipboard()
        """
        return self._dm.GetClipboard()
        
    def GetCpuType(self):
        """函数简介:
        获取当前CPU类型(intel或者amd).
        
        函数原型:
        long GetCpuType()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 未知
        1 : Intel cpu
        2 : AMD cpu
        
        示例:
        if dm.GetCpuType() <> 1 then
            MessageBox "当前系统CPU不是intel cpu,不支持!"
            EndScript
        end if
        """
        return self._dm.GetCpuType()
        
    def GetCpuUsage(self):
        """函数简介:
        获取当前CPU的使用率. 用百分比返回.
        
        函数原型:
        long GetCpuUsage()
        
        参数定义:
        
        返回值:
        整形数:
        0-100表示的百分比
        
        示例:
        TracePrint dm.GetCpuUsage()
        """
        return self._dm.GetCpuUsage()
        
    def GetMemoryUsage(self):
        """函数简介:
        获取当前内存的使用率. 用百分比返回.
        
        函数原型:
        long GetMemoryUsage()
        
        参数定义:
        
        返回值:
        整形数:
        0-100表示的百分比
        
        示例:
        TracePrint dm.GetMemoryUsage()
        """
        return self._dm.GetMemoryUsage()
        
    def GetDir(self, type):
        """函数简介:
        得到系统的路径
        
        函数原型:
        string GetDir(type)
        
        参数定义:
        type 整形数: 取值为以下类型
        0 : 获取当前路径
        1 : 获取系统路径(system32路径)
        2 : 获取windows路径(windows所在路径)
        3 : 获取临时目录路径(temp)
        4 : 获取当前进程(exe)所在的路径
        
        返回值:
        字符串:
        返回路径
        
        示例:
        path = dm.GetDir(2)
        """
        return self._dm.GetDir(type)
        
    def GetDiskModel(self, index):
        """函数简介:
        获取本机的指定硬盘的厂商信息. 要求调用进程必须有管理员权限. 否则返回空串.
        
        函数原型:
        string GetDiskModel(index)
        
        参数定义:
        index整形数: 硬盘序号. 表示是第几块硬盘. 从0开始编号,最小为0,最大为5,也就是最多支持6块硬盘的厂商信息获取.
        
        返回值:
        字符串:
        字符串表达的硬盘厂商信息
        
        示例:
        // 获取第一块硬盘的厂商信息
        model = dm.GetDiskModel(0)
        """
        return self._dm.GetDiskModel(index)
        
    def GetDiskReversion(self, index):
        """函数简介:
        获取本机的指定硬盘的修正版本信息. 要求调用进程必须有管理员权限. 否则返回空串.
        
        函数原型:
        string GetDiskReversion(index)
        
        参数定义:
        index整形数: 硬盘序号. 表示是第几块硬盘. 从0开始编号,最小为0,最大为5,也就是最多支持6块硬盘的修正版本信息获取.
        
        返回值:
        字符串:
        字符串表达的修正版本信息
        
        示例:
        // 获取第一块硬盘的修正版本信息
        reversion = dm.GetDiskReversion(0)
        """
        return self._dm.GetDiskReversion(index)
        
    def GetDiskSerial(self, index):
        """函数简介:
        获取本机的指定硬盘的序列号. 要求调用进程必须有管理员权限. 否则返回空串.
        
        函数原型:
        string GetDiskSerial(index)
        
        参数定义:
        index整形数: 硬盘序号. 表示是第几块硬盘. 从0开始编号,最小为0,最大为5,也就是最多支持6块硬盘的序列号获取.
        
        返回值:
        字符串:
        字符串表达的硬盘序列号
        
        示例:
        // 获取第一块硬盘的序列号
        sirial = dm.GetDiskSerial(0)
        """
        return self._dm.GetDiskSerial(index)
        
    def GetDisplayInfo(self):
        """函数简介:
        获取本机的显卡信息.
        
        函数原型:
        string GetDisplayInfo()
        
        参数定义:
        
        返回值:
        字符串:
        字符串表达的显卡描述信息. 如果有多个显卡,用"|"连接
        
        示例:
        TracePrint dm.GetDisplayInfo()
        """
        return self._dm.GetDisplayInfo()
        
    def GetDPI(self):
        """函数简介:
        判断当前系统的DPI(文字缩放)是不是100%缩放.
        
        函数原型:
        long GetDPI()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 不是
        1 : 是
        
        示例:
        if dm.GetDPI() = 0 then
            MessageBox "当前系统文字缩放不是100%,请设置为100%"
            EndScript
        end if
        """
        return self._dm.GetDPI()
        
    def GetLocale(self):
        """函数简介:
        判断当前系统使用的非UNICODE字符集是否是GB2312(简体中文)(由于设计插件时偷懒了,使用的是非UNICODE字符集，导致插件必须运行在GB2312字符集环境下).
        
        函数原型:
        long GetLocale()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 不是GB2312(简体中文)
        1 : 是GB2312(简体中文)
        
        示例:
        if dm.GetLocale() = 0 then
            dm.SetLocale()
            dm.ExitOs(2)
        end if
        """
        return self._dm.GetLocale()
        
    def GetMachineCode(self):
        """函数简介:
        获取本机的机器码.(带网卡). 此机器码用于插件网站后台. 要求调用进程必须有管理员权限. 否则返回空串.
        
        函数原型:
        string GetMachineCode()
        
        参数定义:
        
        返回值:
        字符串:
        字符串表达的机器机器码
        
        示例:
        machine_code = dm.GetMachineCode()
        
        注: 此机器码包含的硬件设备有硬盘,显卡,网卡等. 其它不便透露. 重装系统不会改变此值.
        另要注意,插拔任何USB设备,(U盘，U盾,USB移动硬盘,USB键鼠等),以及安装任何网卡驱动程序,(开启或者关闭无线网卡等)都会导致机器码改变.
        """
        return self._dm.GetMachineCode()
        
    def GetMachineCodeNoMac(self):
        """函数简介:
        获取本机的机器码.(不带网卡) 要求调用进程必须有管理员权限. 否则返回空串.
        
        函数原型:
        string GetMachineCodeNoMac()
        
        参数定义:
        
        返回值:
        字符串:
        字符串表达的机器机器码
        
        示例:
        machine_code = dm.GetMachineCodeNoMac()
        
        注: 此机器码包含的硬件设备有硬盘,显卡,等. 其它不便透露. 重装系统不会改变此值.
        另要注意,插拔任何USB设备,(U盘，U盾,USB移动硬盘,USB键鼠等),都会导致机器码改变.
        """
        return self._dm.GetMachineCodeNoMac()
        
    def GetNetTime(self):
        """函数简介:
        从网络获取当前北京时间.
        
        函数原型:
        string GetNetTime()
        
        参数定义:
        
        返回值:
        字符串:
        时间格式. 和now返回一致. 比如"2001-11-01 23:14:08"
        
        示例:
        t = dm.GetNetTime()
        TracePrint "当前北京时间是:"&t
        
        注: 如果程序无法访问时间服务器，那么返回"0000-00-00 00:00:00"
        """
        return self._dm.GetNetTime()
        
    def GetNetTimeByIp(self, ip):
        """函数简介:
        根据指定时间服务器IP,从网络获取当前北京时间.
        
        函数原型:
        string GetNetTimeByIp(ip)
        
        参数定义:
        ip 字符串: IP或者域名,并且支持多个IP或者域名连接
        
        返回值:
        字符串:
        时间格式. 和now返回一致. 比如"2001-11-01 23:14:08"
        
        示例:
        t = dm.GetNetTimeByIp("210.72.145.44|ntp.sjtu.edu.cn")
        TracePrint "当前北京时间是:"&t
        
        注: 如果程序无法访问时间服务器，那么返回"0000-00-00 00:00:00"
        时间服务器的IP可以从网上查找NTP服务器.
        """
        return self._dm.GetNetTimeByIp(ip)
        
    def GetOsBuildNumber(self):
        """函数简介:
        得到操作系统的build版本号.
        
        函数原型:
        long GetOsBuildNumber()
        
        参数定义:
        
        返回值:
        整形数:
        build版本号,失败返回0
        
        示例:
        build = dm.GetOsBuildNumber()
        """
        return self._dm.GetOsBuildNumber()
        
    def GetOsType(self):
        """函数简介:
        得到操作系统的类型.
        
        函数原型:
        long GetOsType()
        
        参数定义:
        
        返回值:
        整形数:
        0 : win95/98/me/nt4.0
        1 : xp/2000
        2 : 2003/2003 R2/xp-64
        3 : vista/2008
        4 : win7/2008 R2
        5 : win8/2012
        6 : win8.1/2012 R2
        7 : win10/2016 TP/win11
        
        示例:
        os_type = dm.GetOsType()
        """
        return self._dm.GetOsType()
        
    def GetScreenDepth(self):
        """函数简介:
        获取屏幕的色深.
        
        函数原型:
        long GetScreenDepth()
        
        参数定义:
        
        返回值:
        整形数:
        返回系统颜色深度.(16或者32等)
        
        示例:
        depth = dm.GetScreenDepth()
        """
        return self._dm.GetScreenDepth()
        
    def GetScreenHeight(self):
        """函数简介:
        获取屏幕的高度.
        
        函数原型:
        long GetScreenHeight()
        
        参数定义:
        
        返回值:
        整形数:
        返回屏幕的高度
        
        示例:
        height = dm.GetScreenHeight()
        """
        return self._dm.GetScreenHeight()
        
    def GetScreenWidth(self):
        """函数简介:
        获取屏幕的宽度.
        
        函数原型:
        long GetScreenWidth()
        
        参数定义:
        
        返回值:
        整形数:
        返回屏幕的宽度
        
        示例:
        width = dm.GetScreenWidth()
        """
        return self._dm.GetScreenWidth()
        
    def GetTime(self):
        """函数简介:
        获取当前系统从开机到现在所经历过的时间，单位是毫秒.
        
        函数原型:
        long GetTime()
        
        参数定义:
        
        返回值:
        整形数:
        时间(单位毫秒)
        
        示例:
        time = dm.GetTime()
        """
        return self._dm.GetTime()
        
    def Is64Bit(self):
        """函数简介:
        判断当前系统是否是64位操作系统.
        
        函数原型:
        long Is64Bit()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 不是64位系统
        1 : 是64位系统
        
        示例:
        if dm.Is64Bit() = 1 then
            TracePrint "当前系统是64位系统"
        end if
        """
        return self._dm.Is64Bit()
        
    def IsSupportVt(self):
        """函数简介:
        判断当前CPU是否支持vt,并且是否在bios中开启了vt.
        
        函数原型:
        long IsSupportVt()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 当前cpu不是intel的cpu,或者当前cpu不支持vt,或者bios中没打开vt
        1 : 支持
        
        示例:
        if dm.IsSupportVt() = 1 then
            TracePrint "当前系统支持vt"
        end if
        """
        return self._dm.IsSupportVt()
        
    def Play(self, media_file):
        """函数简介:
        播放指定的MP3或者wav文件.
        
        函数原型:
        long Play(media_file)
        
        参数定义:
        media_file 字符串: 指定的音乐文件，可以采用文件名或者绝对路径的形式.
        
        返回值:
        整形数:
        0 : 失败
        非0表示当前播放的ID。可以用Stop来控制播放结束.
        
        示例:
        id = dm.Play("e:\\1.mp3")
        delay 3000
        dm.Stop id
        """
        return self._dm.Play(media_file)
        
    def RunApp(self, app_path, mode):
        """函数简介:
        运行指定的应用程序.
        
        函数原型:
        long RunApp(app_path,mode)
        
        参数定义:
        app_path 字符串: 指定的可执行程序全路径.
        mode 整形数: 取值如下
        0 : 普通模式
        1 : 加强模式
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.RunApp "c:\\windows\\notepad.exe",0
        """
        return self._dm.RunApp(app_path, mode)
        
    def SetClipboard(self, value):
        """函数简介:
        设置剪贴板的内容.
        
        函数原型:
        long SetClipboard(value)
        
        参数定义:
        value 字符串: 要设置的内容.
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.SetClipboard "123"
        """
        return self._dm.SetClipboard(value)
        
    def SetScreen(self, width, height, depth):
        """函数简介:
        设置系统的分辨率和色深.
        
        函数原型:
        long SetScreen(width,height,depth)
        
        参数定义:
        width 整形数: 屏幕宽度.
        height 整形数: 屏幕高度.
        depth 整形数: 系统色深.
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.SetScreen 1024,768,32
        """
        return self._dm.SetScreen(width, height, depth)
        
    def SetUAC(self, enable):
        """函数简介:
        设置当前系统的UAC(用户账户控制).
        
        函数原型:
        long SetUAC(enable)
        
        参数定义:
        enable 整形数: 取值为以下类型
        0 : 关闭UAC
        1 : 开启UAC
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.SetUAC 0
        
        注: 只有WIN7 WIN8 VISTA WIN2008以及以上系统才有UAC设置
        """
        return self._dm.SetUAC(enable)
        
    def ShowTaskBarIcon(self, hwnd, is_show):
        """函数简介:
        显示或者隐藏指定窗口在任务栏的图标.
        
        函数原型:
        long ShowTaskBarIcon(hwnd,is_show)
        
        参数定义:
        hwnd 整形数: 指定的窗口句柄
        is_show 整形数: 取值为以下类型
        0 : 隐藏
        1 : 显示
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.ShowTaskBarIcon hwnd,0
        """
        return self._dm.ShowTaskBarIcon(hwnd, is_show)
        
    def Stop(self, id):
        """函数简介:
        停止指定的音乐.
        
        函数原型:
        long Stop(id)
        
        参数定义:
        id 整形数: Play返回的播放id.
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        id = dm.Play("e:\\1.mp3")
        delay 3000
        dm.Stop id
        """
        return self._dm.Stop(id)
        
    def ActiveInputMethod(self, hwnd, input_method):
        """函数简介:
        激活指定窗口所在进程的输入法.
        
        函数原型:
        long ActiveInputMethod(hwnd,input_method)
        
        参数定义:
        hwnd 整形数: 窗口句柄
        input_method 字符串: 输入法名字。具体输入法名字对应表查看注册表中以下位置:
                           HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts
                           下面的每一项下的Layout Text的值就是输入法名字
                           比如 "中文 - QQ拼音输入法"
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm_ret = dm.ActiveInputMethod(hwnd,"中文 - QQ拼音输入法")
        if dm_ret = 1 then
            msgbox "QQ输入法开启成功"
        end if
        """
        return self._dm.ActiveInputMethod(hwnd, input_method)
        
    def CheckInputMethod(self, hwnd, input_method):
        """函数简介:
        检测指定窗口所在线程输入法是否开启.
        
        函数原型:
        long CheckInputMethod(hwnd,input_method)
        
        参数定义:
        hwnd 整形数: 窗口句柄
        input_method 字符串: 输入法名字。具体输入法名字对应表查看注册表中以下位置:
                           HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts
                           下面的每一项下的Layout Text的值就是输入法名字
                           比如 "中文 - QQ拼音输入法"
        
        返回值:
        整形数:
        0 : 未开启
        1 : 开启
        
        示例:
        dm_ret = dm.CheckInputMethod(hwnd,"中文 - QQ拼音输入法")
        if dm_ret = 1 then
            msgbox "QQ输入法开启拉"
        end if
        """
        return self._dm.CheckInputMethod(hwnd, input_method)
        
    def enter_cri(self):
        """函数简介:
        检测是否可以进入临界区.
        
        函数原型:
        long EnterCri()
        
        参数定义:
        无参数
        
        返回值:
        整形数:
        0 : 不可以进入
        1 : 已经进入临界区
        
        示例:
        do
            if dm.EnterCri() = 1 then
                exit do
            end if
            delay 100
        loop
        
        注: 此函数如果返回1，则调用对象就会占用此互斥信号量,直到此对象调用LeaveCri,否则不会释放.
        注意:如果调用对象在释放时，会自动把本对象占用的互斥信号量释放.
        """
        return self._dm.EnterCri()
        
    def execute_cmd(self, cmd, current_dir):
        """函数简介:
        运行指定的cmd指令.
        
        函数原型:
        string ExecuteCmd(cmd,current_dir)
        
        参数定义:
        cmd 字符串: 指令,比如"dir"
        current_dir 字符串: 运行的目录，比如"c:\windows"
        
        返回值:
        字符串: 运行指令的输出结果
        
        示例:
        ret = dm.ExecuteCmd("dir","c:\windows")
        """
        return self._dm.ExecuteCmd(cmd, current_dir)
        
    def find_input_method(self, input_method):
        """函数简介:
        根据指定的输入法名字，查找系统中对应的输入法.
        
        函数原型:
        string FindInputMethod(input_method)
        
        参数定义:
        input_method 字符串: 输入法名字。具体输入法名字对应表查看注册表中以下位置:
                           HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts
                           下面的每一项下的Layout Text的值就是输入法名字
                           比如 "中文 - QQ拼音输入法"
        
        返回值:
        字符串: 返回找到的输入法的键盘布局字符串，如果失败，返回空串
        
        示例:
        dm_ret = dm.FindInputMethod("中文 - QQ拼音输入法")
        if len(dm_ret) > 0 then
            msgbox "找到了QQ输入法"
        end if
        """
        return self._dm.FindInputMethod(input_method)
        
    def init_cri(self):
        """函数简介:
        初始化临界区,必须在脚本开头调用此接口.
        
        函数原型:
        long InitCri()
        
        参数定义:
        无参数
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.InitCri()
        """
        return self._dm.InitCri()
        
    def leave_cri(self):
        """函数简介:
        离开临界区.
        
        函数原型:
        long LeaveCri()
        
        参数定义:
        无参数
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.LeaveCri()
        """
        return self._dm.LeaveCri()
        
    def release_ref(self):
        """函数简介:
        释放引用.
        
        函数原型:
        long ReleaseRef()
        
        参数定义:
        无参数
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.ReleaseRef()
        """
        return self._dm.ReleaseRef()
        
    def set_exit_thread(self, enable):
        """函数简介:
        设置是否允许脚本调用此对象的退出线程.
        
        函数原型:
        long SetExitThread(enable)
        
        参数定义:
        enable 整形数: 取值为以下类型
        0 : 不允许
        1 : 允许
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        dm.SetExitThread 0
        """
        return self._dm.SetExitThread(enable)
        
    def exclude_pos(self, all_pos, type, x1, y1, x2, y2):
        """函数简介:
        根据部分Ex接口的返回值，然后在此基础上排除指定范围内的坐标.
        
        函数原型:
        string ExcludePos(all_pos,type,x1,y1,x2,y2)
        
        参数定义:
        all_pos 字符串: 坐标描述串。一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx, FindMultiColorEx,和FindPicEx的返回值.
        type 整形数: 取值为0或者1
                    如果all_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0
                    如果all_pos的内容是由FindColorEx, FindMultiColorEx返回，那么取值为1
                    如果all_pos的内容是由OcrEx返回，那么取值为2
                    如果all_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3
        x1 整形数: 左上角X坐标
        y1 整形数: 左上角Y坐标
        x2 整形数: 右下角X坐标
        y2 整形数: 右下角Y坐标
        
        返回值:
        字符串: 返回的格式和type指定的格式一致
        
        示例:
        ret = dm.FindColorEx(0,0,2000,2000,"aaaaaa-000000",1.0,0)
        ret = dm.ExcludePos(ret,1,100,100,500,500)
        TracePrint ret
        """
        return self._dm.ExcludePos(all_pos, type, x1, y1, x2, y2)
        
    def find_nearest_pos(self, all_pos, type, x, y):
        """函数简介:
        根据部分Ex接口的返回值，然后在此基础上查找最近指定坐标的坐标.
        
        函数原型:
        string FindNearestPos(all_pos,type,x,y)
        
        参数定义:
        all_pos 字符串: 坐标描述串。一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx, FindMultiColorEx,和FindPicEx的返回值.
        type 整形数: 取值为0或者1
                    如果all_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0
                    如果all_pos的内容是由FindColorEx, FindMultiColorEx返回，那么取值为1
                    如果all_pos的内容是由OcrEx返回，那么取值为2
                    如果all_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3
        x 整形数: X坐标
        y 整形数: Y坐标
        
        返回值:
        字符串: 返回的格式和type指定的格式一致
        
        示例:
        ret = dm.FindColorEx(0,0,2000,2000,"aaaaaa-000000",1.0,0)
        ret = dm.FindNearestPos(ret,1,100,100)
        TracePrint ret
        """
        return self._dm.FindNearestPos(all_pos, type, x, y)
        
    def sort_pos_distance(self, all_pos, type, x, y):
        """函数简介:
        根据部分Ex接口的返回值，然后对所有坐标根据对指定坐标的距离进行从小到大的排序.
        
        函数原型:
        string SortPosDistance(all_pos,type,x,y)
        
        参数定义:
        all_pos 字符串: 坐标描述串。一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx, FindMultiColorEx,和FindPicEx的返回值.
        type 整形数: 取值为0或者1
                    如果all_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0
                    如果all_pos的内容是由FindColorEx, FindMultiColorEx返回，那么取值为1
                    如果all_pos的内容是由OcrEx返回，那么取值为2
                    如果all_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3
        x 整形数: X坐标
        y 整形数: Y坐标
                 注意:如果x为65535并且y为0时，那么排序的结果是仅仅对x坐标进行排序
                 如果y为65535并且x为0时，那么排序的结果是仅仅对y坐标进行排序
        
        返回值:
        字符串: 返回的格式和type指定的格式一致
        
        示例:
        ret = dm.FindColorEx(0,0,2000,2000,"aaaaaa-000000",1.0,0)
        ret = dm.SortPosDistance(ret,1,100,100)
        TracePrint ret
        """
        return self._dm.SortPosDistance(all_pos, type, x, y)
        
    def GetSystemInfo(self, type, method):
        """函数简介:
        获取指定的系统信息.
        
        函数原型:
        string GetSystemInfo(type,method)
        
        参数定义:
        type 字符串: 取值如下
        "cpuid" : 表示获取cpu序列号. method可取0和1
        "disk_volume_serial id" : 表示获取分区序列号. id表示分区序号. 0表示C盘.1表示D盘.以此类推. 最高取到5. 也就是6个分区. method可取0
        "bios_vendor" : 表示获取bios厂商信息. method可取0和1
        "bios_version" : 表示获取bios版本信息. method可取0和1
        "bios_release_date" : 表示获取bios发布日期. method可取0和1
        "bios_oem" : 表示获取bios里的oem信息. method可取0
        "board_vendor" : 表示获取主板制造厂商信息. method可取0和1
        "board_product" : 表示获取主板产品信息. method可取0和1
        "board_version" : 表示获取主板版本信息. method可取0和1
        "board_serial" : 表示获取主板序列号. method可取0
        "board_location" : 表示获取主板位置信息. method可取0
        "system_manufacturer" : 表示获取系统制造商信息. method可取0和1
        "system_product" : 表示获取系统产品信息. method可取0和1
        "system_serial" : 表示获取bios序列号. method可取0
        "system_uuid" : 表示获取bios uuid. method可取0
        "system_version" : 表示获取系统版本信息. method可取0和1
        "system_sku" : 表示获取系统sku序列号. method可取0和1
        "system_family" : 表示获取系统家族信息. method可取0和1
        "product_id" : 表示获取系统产品id. method可取0
        "system_identifier" : 表示获取系统标识. method可取0
        "system_bios_version" : 表示获取系统BIOS版本号. method可取0. 多个结果用"|"连接.
        "system_bios_date" : 表示获取系统BIOS日期. method可取0
        method整形数: 获取方法. 一般从0开始取值.
        
        返回值:
        字符串:
        字符串表达的系统信息.
        
        示例:
        // 获取系统所有特征信息
        TracePrint dm.GetSystemInfo("cpuid",0)
        TracePrint dm.GetSystemInfo("cpuid",1)
        """
        return self._dm.GetSystemInfo(type, method)
        
    def SetDisplayAcceler(self, level):
        """函数简介:
        设置当前系统的硬件加速级别.
        
        函数原型:
        long SetDisplayAcceler(level)
        
        参数定义:
        level整形数: 取值范围为0-5. 0表示关闭硬件加速。5表示完全打开硬件加速.
        
        返回值:
        整形数:
        0 : 失败.
        1 : 成功.
        
        示例:
        // 关闭硬件加速
        TracePrint SetDisplayAcceler(0)
        
        注: 此函数只在XP 2003系统有效.
        """
        return self._dm.SetDisplayAcceler(level)
        
    def SetLocale(self):
        """函数简介:
        设置当前系统的非UNICOD字符集. 会弹出一个字符集选择列表,用户自己选择到简体中文即可.
        
        函数原型:
        long SetLocale()
        
        参数定义:
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        示例:
        if dm.GetLocale() = 0 then
            dm.SetLocale()
            dm.ExitOs(2)
        end if
        """
        return self._dm.SetLocale()
        
    # 中文别名
    蜂鸣 = Beep
    检查字体平滑 = CheckFontSmooth
    检查UAC = CheckUAC
    延时 = Delay
    随机延时 = Delays
    禁止关闭显示器和睡眠 = DisableCloseDisplayAndSleep
    禁用字体平滑 = DisableFontSmooth
    禁用电源管理 = DisablePowerSave
    禁用屏幕保护 = DisableScreenSave
    启用字体平滑 = EnableFontSmooth
    退出系统 = ExitOs
    获取剪贴板 = GetClipboard
    获取CPU类型 = GetCpuType
    获取CPU使用率 = GetCpuUsage
    获取目录 = GetDir
    获取硬盘型号 = GetDiskModel
    获取硬盘版本 = GetDiskReversion
    获取硬盘序列号 = GetDiskSerial
    获取显卡信息 = GetDisplayInfo
    获取DPI = GetDPI
    获取区域设置 = GetLocale
    获取机器码 = GetMachineCode
    获取机器码NoMac = GetMachineCodeNoMac
    获取内存使用率 = GetMemoryUsage
    获取网络时间 = GetNetTime
    获取网络时间ByIP = GetNetTimeByIp
    获取系统版本号 = GetOsBuildNumber
    获取系统类型 = GetOsType
    获取屏幕色深 = GetScreenDepth
    获取屏幕高度 = GetScreenHeight
    获取屏幕宽度 = GetScreenWidth
    获取时间 = GetTime
    是否64位 = Is64Bit
    是否支持VT = IsSupportVt
    播放 = Play
    运行程序 = RunApp
    设置剪贴板 = SetClipboard
    设置屏幕 = SetScreen
    设置UAC = SetUAC
    显示任务栏图标 = ShowTaskBarIcon
    停止 = Stop
    激活输入法 = ActiveInputMethod
    检查输入法 = CheckInputMethod
    进入临界区 = enter_cri
    执行CMD指令 = execute_cmd
    查找输入法 = find_input_method
    初始化临界区 = init_cri
    离开临界区 = leave_cri
    释放引用 = release_ref
    设置退出线程 = set_exit_thread
    排除坐标 = exclude_pos
    查找最近坐标 = find_nearest_pos
    坐标距离排序 = sort_pos_distance
    获取系统信息 = GetSystemInfo
    设置显示加速 = SetDisplayAcceler
    设置区域 = SetLocale 