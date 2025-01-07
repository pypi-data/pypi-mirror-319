#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件文件操作模块API封装
用于文件操作相关的功能
'''

class DmFile:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 复制文件(self, 源文件: str, 目标文件: str) -> int:
        """
        函数简介:
            复制文件。
        
        函数原型:
            long CopyFile(src_file,dst_file)
        
        参数定义:
            源文件 字符串: 要复制的文件名
            目标文件 字符串: 复制到的目标文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 复制文件: {msg}")
            return 0
            
        try:
            return self._dm.CopyFile(源文件, 目标文件)
        except Exception as e:
            print(f"Error in 复制文件: {str(e)}")
            return 0

    def 创建文件夹(self, 文件夹: str) -> int:
        """
        函数简介:
            创建指定的文件夹。
        
        函数原型:
            long CreateFolder(folder)
        
        参数定义:
            文件夹 字符串: 要创建的文件夹名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 创建文件夹: {msg}")
            return 0
            
        try:
            return self._dm.CreateFolder(文件夹)
        except Exception as e:
            print(f"Error in 创建文件夹: {str(e)}")
            return 0

    def 解密文件(self, 源文件: str, 目标文件: str, 密码: str) -> int:
        """
        函数简介:
            解密指定的文件。
        
        函数原型:
            long DecodeFile(src_file,dst_file,pwd)
        
        参数定义:
            源文件 字符串: 要解密的文件名
            目标文件 字符串: 解密后的目标文件名
            密码 字符串: 密码
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 解密文件: {msg}")
            return 0
            
        try:
            return self._dm.DecodeFile(源文件, 目标文件, 密码)
        except Exception as e:
            print(f"Error in 解密文件: {str(e)}")
            return 0

    def 删除文件(self, 文件: str) -> int:
        """
        函数简介:
            删除指定的文件。
        
        函数原型:
            long DeleteFile(file)
        
        参数定义:
            文件 字符串: 要删除的文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 删除文件: {msg}")
            return 0
            
        try:
            return self._dm.DeleteFile(文件)
        except Exception as e:
            print(f"Error in 删除文件: {str(e)}")
            return 0

    def 删除文件夹(self, 文件夹: str) -> int:
        """
        函数简介:
            删除指定的文件夹。
        
        函数原型:
            long DeleteFolder(folder)
        
        参数定义:
            文件夹 字符串: 要删除的文件夹名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 删除文件夹: {msg}")
            return 0
            
        try:
            return self._dm.DeleteFolder(文件夹)
        except Exception as e:
            print(f"Error in 删除文件夹: {str(e)}")
            return 0

    def 删除指定的ini节(self, 节名: str, 文件: str) -> int:
        """
        函数简介:
            删除指定的ini节。
        
        函数原型:
            long DeleteIni(section,key,file)
        
        参数定义:
            节名 字符串: 要删除的节名
            文件 字符串: ini文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 删除指定的ini节: {msg}")
            return 0
            
        try:
            return self._dm.DeleteIni(节名, "", 文件)
        except Exception as e:
            print(f"Error in 删除指定的ini节: {str(e)}")
            return 0

    def 删除指定的ini键值(self, 节名: str, 键名: str, 文件: str) -> int:
        """
        函数简介:
            删除指定的ini键值。
        
        函数原型:
            long DeleteIniPwd(section,key,file,pwd)
        
        参数定义:
            节名 字符串: 节名
            键名 字符串: 键名
            文件 字符串: ini文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 删除指定的ini键值: {msg}")
            return 0
            
        try:
            return self._dm.DeleteIniPwd(节名, 键名, 文件, "")
        except Exception as e:
            print(f"Error in 删除指定的ini键值: {str(e)}")
            return 0

    def 下载文件(self, 地址: str, 存储文件: str) -> int:
        """
        函数简介:
            从指定的网址下载文件。
        
        函数原型:
            long DownloadFile(url,save_file)
        
        参数定义:
            地址 字符串: 网址
            存储文件 字符串: 要存储的文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 下载文件: {msg}")
            return 0
            
        try:
            return self._dm.DownloadFile(地址, 存储文件)
        except Exception as e:
            print(f"Error in 下载文件: {str(e)}")
            return 0

    def 加密文件(self, 源文件: str, 目标文件: str, 密码: str) -> int:
        """
        函数简介:
            加密指定的文件。
        
        函数原型:
            long EncodeFile(src_file,dst_file,pwd)
        
        参数定义:
            源文件 字符串: 要加密的文件名
            目标文件 字符串: 加密后的目标文件名
            密码 字符串: 密码
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 加密文件: {msg}")
            return 0
            
        try:
            return self._dm.EncodeFile(源文件, 目标文件, 密码)
        except Exception as e:
            print(f"Error in 加密文件: {str(e)}")
            return 0

    def 枚举指定目录下的所有文件(self, 目录: str) -> str:
        """
        函数简介:
            枚举指定目录下的所有文件。
        
        函数原型:
            string EnumIniSection(file)
        
        参数定义:
            目录 字符串: 目录名
        
        返回值:
            字符串: 所有文件名,以|分割
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 枚举指定目录下的所有文件: {msg}")
            return ""
            
        try:
            return self._dm.EnumIniSection(目录)
        except Exception as e:
            print(f"Error in 枚举指定目录下的所有文件: {str(e)}")
            return ""

    def 枚举指定目录下的所有文件夹(self, 目录: str) -> str:
        """
        函数简介:
            枚举指定目录下的所有文件夹。
        
        函数原型:
            string EnumIniSectionPwd(file,pwd)
        
        参数定义:
            目录 字符串: 目录名
        
        返回值:
            字符串: 所有文件夹名,以|分割
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 枚举指定目录下的所有文件夹: {msg}")
            return ""
            
        try:
            return self._dm.EnumIniSectionPwd(目录, "")
        except Exception as e:
            print(f"Error in 枚举指定目录下的所有文件夹: {str(e)}")
            return ""

    def 获取文件长度(self, 文件: str) -> int:
        """
        函数简介:
            获取指定文件的长度。
        
        函数原型:
            long GetFileLength(file)
        
        参数定义:
            文件 字符串: 文件名
        
        返回值:
            整形数: 文件长度
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取文件长度: {msg}")
            return 0
            
        try:
            return self._dm.GetFileLength(文件)
        except Exception as e:
            print(f"Error in 获取文件长度: {str(e)}")
            return 0

    def 获取真实路径(self, 文件: str) -> str:
        """
        函数简介:
            获取指定文件的真实路径。
        
        函数原型:
            string GetRealPath(file)
        
        参数定义:
            文件 字符串: 文件名
        
        返回值:
            字符串: 文件的真实路径
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取真实路径: {msg}")
            return ""
            
        try:
            return self._dm.GetRealPath(文件)
        except Exception as e:
            print(f"Error in 获取真实路径: {str(e)}")
            return ""

    def 判断文件是否存在(self, 文件: str) -> int:
        """
        函数简介:
            判断指定文件是否存在。
        
        函数原型:
            long IsFileExist(file)
        
        参数定义:
            文件 字符串: 文件名
        
        返回值:
            整形数: 0: 不存在 1: 存在
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 判断文件是否存在: {msg}")
            return 0
            
        try:
            return self._dm.IsFileExist(文件)
        except Exception as e:
            print(f"Error in 判断文件是否存在: {str(e)}")
            return 0

    def 判断文件夹是否存在(self, 文件夹: str) -> int:
        """
        函数简介:
            判断指定文件夹是否存在。
        
        函数原型:
            long IsFolderExist(folder)
        
        参数定义:
            文件夹 字符串: 文件夹名
        
        返回值:
            整形数: 0: 不存在 1: 存在
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 判断文件夹是否存在: {msg}")
            return 0
            
        try:
            return self._dm.IsFolderExist(文件夹)
        except Exception as e:
            print(f"Error in 判断文件夹是否存在: {str(e)}")
            return 0

    def 读取文件(self, 文件: str) -> str:
        """
        函数简介:
            读取指定文件的内容。
        
        函数原型:
            string ReadFile(file)
        
        参数定义:
            文件 字符串: 文件名
        
        返回值:
            字符串: 文件内容
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取文件: {msg}")
            return ""
            
        try:
            return self._dm.ReadFile(文件)
        except Exception as e:
            print(f"Error in 读取文件: {str(e)}")
            return ""

    def 读取ini(self, 节名: str, 键名: str, 文件: str) -> str:
        """
        函数简介:
            读取指定的ini文件。
        
        函数原型:
            string ReadIni(section,key,file)
        
        参数定义:
            节名 字符串: 节名
            键名 字符串: 键名
            文件 字符串: ini文件名
        
        返回值:
            字符串: 读取到的内容
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取ini: {msg}")
            return ""
            
        try:
            return self._dm.ReadIni(节名, 键名, 文件)
        except Exception as e:
            print(f"Error in 读取ini: {str(e)}")
            return ""

    def 读取ini密码(self, 节名: str, 键名: str, 文件: str, 密码: str) -> str:
        """
        函数简介:
            读取加密的ini文件。
        
        函数原型:
            string ReadIniPwd(section,key,file,pwd)
        
        参数定义:
            节名 字符串: 节名
            键名 字符串: 键名
            文件 字符串: ini文件名
            密码 字符串: 密码
        
        返回值:
            字符串: 读取到的内容
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 读取ini2: {msg}")
            return ""
            
        try:
            return self._dm.ReadIniPwd(节名, 键名, 文件, 密码)
        except Exception as e:
            print(f"Error in 读取ini2: {str(e)}")
            return ""

    def 选择目录(self) -> str:
        """
        函数简介:
            弹出选择目录对话框。
        
        函数原型:
            string SelectDirectory()
        
        参数定义:
            无
        
        返回值:
            字符串: 选择的目录
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 选择目录: {msg}")
            return ""
            
        try:
            return self._dm.SelectDirectory()
        except Exception as e:
            print(f"Error in 选择目录: {str(e)}")
            return ""

    def 选择文件(self) -> str:
        """
        函数简介:
            弹出选择文件对话框。
        
        函数原型:
            string SelectFile()
        
        参数定义:
            无
        
        返回值:
            字符串: 选择的文件名
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 选择文件: {msg}")
            return ""
            
        try:
            return self._dm.SelectFile()
        except Exception as e:
            print(f"Error in 选择文件: {str(e)}")
            return ""

    def 写入文件(self, 文件: str, 内容: str) -> int:
        """
        函数简介:
            写入指定的文件。
        
        函数原型:
            long WriteFile(file,content)
        
        参数定义:
            文件 字符串: 文件名
            内容 字符串: 要写入的内容
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入文件: {msg}")
            return 0
            
        try:
            return self._dm.WriteFile(文件, 内容)
        except Exception as e:
            print(f"Error in 写入文件: {str(e)}")
            return 0

    def 写入ini(self, 节名: str, 键名: str, 值: str, 文件: str) -> int:
        """
        函数简介:
            写入指定的ini文件。
        
        函数原型:
            long WriteIni(section,key,value,file)
        
        参数定义:
            节名 字符串: 节名
            键名 字符串: 键名
            值 字符串: 要写入的值
            文件 字符串: ini文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入ini: {msg}")
            return 0
            
        try:
            return self._dm.WriteIni(节名, 键名, 值, 文件)
        except Exception as e:
            print(f"Error in 写入ini: {str(e)}")
            return 0

    def 写入ini2(self, 节名: str, 键名: str, 值: str, 文件: str, 密码: str) -> int:
        """
        函数简介:
            写入加密的ini文件。
        
        函数原型:
            long WriteIniPwd(section,key,value,file,pwd)
        
        参数定义:
            节名 字符串: 节名
            键名 字符串: 键名
            值 字符串: 要写入的值
            文件 字符串: ini文件名
            密码 字符串: 密码
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 写入ini2: {msg}")
            return 0
            
        try:
            return self._dm.WriteIniPwd(节名, 键名, 值, 文件, 密码)
        except Exception as e:
            print(f"Error in 写入ini2: {str(e)}")
            return 0

    # 添加英文别名
    def CopyFile(self, *args, **kwargs):
        """英文别名，调用复制文件"""
        return self.复制文件(*args, **kwargs)

    def CreateFolder(self, *args, **kwargs):
        """英文别名，调用创建文件夹"""
        return self.创建文件夹(*args, **kwargs)

    def DecodeFile(self, *args, **kwargs):
        """英文别名，调用解密文件"""
        return self.解密文件(*args, **kwargs)

    def DeleteFile(self, *args, **kwargs):
        """英文别名，调用删除文件"""
        return self.删除文件(*args, **kwargs)

    def DeleteFolder(self, *args, **kwargs):
        """英文别名，调用删除文件夹"""
        return self.删除文件夹(*args, **kwargs)

    def DeleteIni(self, *args, **kwargs):
        """英文别名，调用删除指定的ini节"""
        return self.删除指定的ini节(*args, **kwargs)

    def DeleteIniPwd(self, *args, **kwargs):
        """英文别名，调用删除指定的ini键值"""
        return self.删除指定的ini键值(*args, **kwargs)

    def DownloadFile(self, *args, **kwargs):
        """英文别名，调用下载文件"""
        return self.下载文件(*args, **kwargs)

    def EncodeFile(self, *args, **kwargs):
        """英文别名，调用加密文件"""
        return self.加密文件(*args, **kwargs)

    def EnumIniSection(self, *args, **kwargs):
        """英文别名，调用枚举指定目录下的所有文件"""
        return self.枚举指定目录下的所有文件(*args, **kwargs)

    def EnumIniSectionPwd(self, *args, **kwargs):
        """英文别名，调用枚举指定目录下的所有文件夹"""
        return self.枚举指定目录下的所有文件夹(*args, **kwargs)

    def GetFileLength(self, *args, **kwargs):
        """英文别名，调用获取文件长度"""
        return self.获取文件长度(*args, **kwargs)

    def GetRealPath(self, *args, **kwargs):
        """英文别名，调用获取真实路径"""
        return self.获取真实路径(*args, **kwargs)

    def IsFileExist(self, *args, **kwargs):
        """英文别名，调用判断文件是否存在"""
        return self.判断文件是否存在(*args, **kwargs)

    def IsFolderExist(self, *args, **kwargs):
        """英文别名，调用判断文件夹是否存在"""
        return self.判断文件夹是否存在(*args, **kwargs)

    def ReadFile(self, *args, **kwargs):
        """英文别名，调用读取文件"""
        return self.读取文件(*args, **kwargs)

    def ReadIni(self, *args, **kwargs):
        """英文别名，调用读取ini"""
        return self.读取ini(*args, **kwargs)

    def ReadIniPwd(self, *args, **kwargs):
        """英文别名，调用读取ini2"""
        return self.读取ini2(*args, **kwargs)

    def SelectDirectory(self, *args, **kwargs):
        """英文别名，调用选择目录"""
        return self.选择目录(*args, **kwargs)

    def SelectFile(self, *args, **kwargs):
        """英文别名，调用选择文件"""
        return self.选择文件(*args, **kwargs)

    def WriteFile(self, *args, **kwargs):
        """英文别名，调用写入文件"""
        return self.写入文件(*args, **kwargs)

    def WriteIni(self, *args, **kwargs):
        """英文别名，调用写入ini"""
        return self.写入ini(*args, **kwargs)

    def WriteIniPwd(self, *args, **kwargs):
        """英文别名，调用写入ini2"""
        return self.写入ini2(*args, **kwargs) 