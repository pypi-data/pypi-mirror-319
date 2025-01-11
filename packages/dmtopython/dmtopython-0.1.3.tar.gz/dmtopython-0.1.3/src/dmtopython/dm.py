#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件API完整封装
'''

import win32com.client
from .dm_ai import DmAi
from .dm_mouse import DmMouse
from .dm_keyboard import DmKeyboard
from .dm_window import DmWindow
from .dm_foobar import DmFoobar
from .dm_memory import DmMemory
from .dm_system import DmSystem
from .dm_ocr import DmOcr
from .dm_file import DmFile
from .dm_find import DmFind
from .dm_bg import DmBg
from .dm_faq import DmFaq
from .dm_dmg import DmDmg
from .dm_asm import DmAsm

class DmSoft:
    def __init__(self,code:str,key:str):
        self.code = code
        self.key = key
        """创建大漠对象"""
        try:
            self._dm = win32com.client.Dispatch('dm.dmsoft')
            # 注册
            self.regstats = self._dm.Reg(self.code, self.key)
            if self.regstats == 1:
                            # 初始化所有模块
                self.ai = DmAi(self._dm)
                self.asm = DmAsm(self._dm)
                self.bg = DmBg(self._dm)
                self.dmg = DmDmg(self._dm)
                self.faq = DmFaq(self._dm)
                self.file = DmFile(self._dm)
                self.find = DmFind(self._dm)
                self.footbar = DmFoobar(self._dm)
                self.keyboard = DmKeyboard(self._dm)
                self.memory = DmMemory(self._dm)
                self.mouse = DmMouse(self._dm)
                self.ocr = DmOcr(self._dm)
                self.system = DmSystem(self._dm)
                self.window = DmWindow(self._dm)
                print("大漠注册成功")
            else:
                self._dm = None
                raise Exception("注册失败，错误码："+str(self.regstats))
        except Exception as e:
            raise Exception("创建大漠对象失败，错误提示："+str(e))

    def get_dm_count(self):
        """获取大漠对象个数"""
        try:
            self._check_dm()
            return self._dm.GetDmCount()
        except Exception as e:
            print(f"Error in get_dm_count: {str(e)}")
            return 0 
    def close(self):
        """关闭大漠对象"""
        try:
            self._check_dm()
            self._dm.UnBindWindow()
        except Exception as e:
            print(f"Error in close: {str(e)}")

    def EnablePicCache(self, enable: int) -> int:
        """
        函数简介:
            设置是否开启或者关闭插件内部的图片缓存机制. (默认是打开)
        函数原型:
            long EnablePicCache(enable)
        参数定义:
            enable 整形数: 
                0 : 关闭
                1 : 打开
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            有些时候，系统内存比较吃紧，这时候再打开内部缓存，可能会导致缓存分配
            在虚拟内存，这样频繁换页，反而导致图色效率下降.这时候就建议关闭图色缓存.
            所有图色缓存机制都是对本对象的，也就是说，调用图色缓存机制的函数仅仅对本
            对象生效. 每个对象都有一个图色缓存队列.
        """
        return self._dm.EnablePicCache(enable)

    def GetBasePath(self) -> str:
        """
        函数简介:
            获取注册在系统中的dm.dll的路径
        函数原型:
            string GetBasePath()
        返回值:
            字符串: 返回dm.dll所在路径
        """
        return self._dm.GetBasePath()

    def GetDmCount(self) -> int:
        """
        函数简介:
            返回当前进程已经创建的dm对象个数
        函数原型:
            long GetDmCount()
        返回值:
            整形数: 个数
        """
        return self._dm.GetDmCount()

    def GetID(self) -> int:
        """
        函数简介:
            返回当前大漠对象的ID值，这个值对于每个对象是唯一存在的。可以用来判定两个大漠对象是否一致
        函数原型:
            long GetID()
        返回值:
            整形数: 当前对象的ID值
        """
        return self._dm.GetID()

    def GetLastError(self) -> int:
        """
        函数简介:
            获取插件命令的最后错误
        函数原型:
            long GetLastError()
        返回值:
            整形数: 返回值表示错误值。 0表示无错误
            -1 : 表示你使用了绑定里的收费功能，但是没注册，无法使用
            -2 : 使用模式0 2 时出现，因为目标窗口有保护
            ... (更多错误码说明请参考文档)
        注: 
            此函数必须紧跟上一句函数调用，中间任何的语句调用都会改变这个值
        """
        return self._dm.GetLastError()

    def GetPath(self) -> str:
        """
        函数简介:
            获取全局路径.(可用于调试)
        函数原型:
            string GetPath()
        返回值:
            字符串: 以字符串的形式返回当前设置的全局路径
        """
        return self._dm.GetPath()

    def SetDisplayInput(self, mode: str) -> int:
        """
        函数简介:
            设定图色的获取方式，默认是显示器或者后台窗口(具体参考BindWindow)
        函数原型:
            long SetDisplayInput(mode)
        参数定义:
            mode 字符串: 图色输入模式取值有以下几种
                1. "screen" 这个是默认的模式，表示使用显示器或者后台窗口
                2. "pic:file" 指定输入模式为指定的图片
                3. "mem:addr,size" 指定输入模式为指定的图片,此图片在内存当中
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetDisplayInput(mode)

    def SetEnumWindowDelay(self, delay: int) -> int:
        """
        函数简介:
            设置EnumWindow EnumWindowByProcess EnumWindowSuper FindWindow以及FindWindowEx的最长延时
        函数原型:
            long SetEnumWindowDelay(delay)
        参数定义:
            delay 整形数: 单位毫秒
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetEnumWindowDelay(delay)

    def SetPath(self, path: str) -> int:
        """
        函数简介:
            设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径
        函数原型:
            long SetPath(path)
        参数定义:
            path 字符串: 路径,可以是相对路径,也可以是绝对路径
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetPath(path)

    def SpeedNormalGraphic(self, enable: int) -> int:
        """
        函数简介:
            设置是否对前台图色进行加速. (默认是关闭). (对于不绑定，或者绑定图色为normal生效)( 仅对WIN8以上系统有效)
        函数原型:
            long SpeedNormalGraphic(enable)
        参数定义:
            enable 整形数:
                0 : 关闭
                1 : 打开
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SpeedNormalGraphic(enable)

    def Ver(self) -> str:
        """
        函数简介:
            返回当前插件版本号
        函数原型:
            string Ver()
        返回值:
            字符串: 当前插件的版本描述字符串
        """
        return self._dm.Ver()

    def Reg(self, reg_code: str, ver_info: str) -> int:
        """
        函数简介:
            调用此函数来注册，从而使用插件的高级功能
        函数原型:
            long Reg(reg_code,ver_info)
        参数定义:
            reg_code 字符串: 注册码
            ver_info 字符串: 版本附加信息（附加码）
        返回值:
            整形数:
            -1 : 无法连接网络
            -2 : 进程没有以管理员方式运行
            0 : 失败
            1 : 成功
            2 : 余额不足
            3 : 绑定了本机器，但是账户余额不足50元
            4 : 注册码错误
            5 : 你的机器或者IP在黑名单列表中或者不在白名单列表中
            6 : 非法使用插件
            7 : 你的帐号因为非法使用被封禁
            8 : ver_info不在你设置的附加白名单中
            77 : 机器码或者IP因为非法使用被封禁
            777 : 同一个机器码注册次数超过了服务器限制
        注:
            必须保证此函数在创建完对象以后立即调用，尤其必须在绑定窗口之前调用
        """
        return self._dm.Reg(reg_code, ver_info)

    # 中文别名
    开启图片缓存 = EnablePicCache
    获取基础路径 = GetBasePath
    获取对象数量 = GetDmCount
    获取对象ID = GetID
    获取最后错误 = GetLastError
    获取全局路径 = GetPath
    设置显示输入 = SetDisplayInput
    设置枚举延时 = SetEnumWindowDelay
    设置全局路径 = SetPath
    加速前台图色 = SpeedNormalGraphic
    获取版本号 = Ver
    注册 = Reg
