#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件OCR模块API封装
用于文字识别相关的功能
'''

class DmOcr:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 添加字典(self, 字典: str) -> int:
        """
        函数简介:
            添加字库文件。

        函数原型:
            long AddDict(index,dict_info)

        参数定义:
            字典 字符串: 字库文件名

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 添加字典: {msg}")
            return 0
            
        try:
            return self._dm.AddDict(0, 字典)
        except Exception as e:
            print(f"Error in 添加字典: {str(e)}")
            return 0

    def 清空字典(self) -> int:
        """
        函数简介:
            清空字库。

        函数原型:
            long ClearDict(index)

        参数定义:
            无

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 清空字典: {msg}")
            return 0
            
        try:
            return self._dm.ClearDict(0)
        except Exception as e:
            print(f"Error in 清空字典: {str(e)}")
            return 0

    def 启用共享字库(self, 启用: int) -> int:
        """
        函数简介:
            设置是否启用共享字库。

        函数原型:
            long EnableShareDict(enable)

        参数定义:
            启用 整形数: 0: 关闭 1: 开启

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用共享字库: {msg}")
            return 0
            
        try:
            return self._dm.EnableShareDict(启用)
        except Exception as e:
            print(f"Error in 启用共享字库: {str(e)}")
            return 0

    def 获取字库数量(self) -> int:
        """
        函数简介:
            获取字库中的字符数量。

        函数原型:
            long GetDictCount(index)

        参数定义:
            无

        返回值:
            整形数: 字库中的字符数量
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取字库数量: {msg}")
            return 0
            
        try:
            return self._dm.GetDictCount(0)
        except Exception as e:
            print(f"Error in 获取字库数量: {str(e)}")
            return 0

    def 获取字库信息(self) -> str:
        """
        函数简介:
            获取字库信息。

        函数原型:
            string GetDictInfo(str,font_name,word_height,sim)

        参数定义:
            无

        返回值:
            字符串: 字库信息
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取字库信息: {msg}")
            return ""
            
        try:
            return self._dm.GetDictInfo("", "", 0, 0.0)
        except Exception as e:
            print(f"Error in 获取字库信息: {str(e)}")
            return ""

    def 获取结果数量(self) -> int:
        """
        函数简介:
            获取识别结果数量。

        函数原型:
            long GetResultCount(str)

        参数定义:
            无

        返回值:
            整形数: 识别到的结果数量
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取结果数量: {msg}")
            return 0
            
        try:
            return self._dm.GetResultCount("")
        except Exception as e:
            print(f"Error in 获取结果数量: {str(e)}")
            return 0

    def 获取结果坐标(self, 索引: int) -> str:
        """
        函数简介:
            获取第index个识别结果的坐标。

        函数原型:
            string GetResultPos(str,index,x,y)

        参数定义:
            索引 整形数: 第几个结果,从0开始

        返回值:
            字符串: 坐标信息,格式为"x,y"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取结果坐标: {msg}")
            return ""
            
        try:
            return self._dm.GetResultPos("", 索引, 0, 0)
        except Exception as e:
            print(f"Error in 获取结果坐标: {str(e)}")
            return ""

    def 获取词组数量(self) -> int:
        """
        函数简介:
            获取词组数量。

        函数原型:
            long GetWordResultCount(str)

        参数定义:
            无

        返回值:
            整形数: 词组数量
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取词组数量: {msg}")
            return 0
            
        try:
            return self._dm.GetWordResultCount("")
        except Exception as e:
            print(f"Error in 获取词组数量: {str(e)}")
            return 0

    def 获取词组坐标(self, 索引: int) -> str:
        """
        函数简介:
            获取第index个词组的坐标。

        函数原型:
            string GetWordResultPos(str,index,x,y)

        参数定义:
            索引 整形数: 第几个词组,从0开始

        返回值:
            字符串: 坐标信息,格式为"x,y"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取词组坐标: {msg}")
            return ""
            
        try:
            return self._dm.GetWordResultPos("", 索引, 0, 0)
        except Exception as e:
            print(f"Error in 获取词组坐标: {str(e)}")
            return ""

    def 获取词组(self, 索引: int) -> str:
        """
        函数简介:
            获取第index个词组。

        函数原型:
            string GetWords(str,index)

        参数定义:
            索引 整形数: 第几个词组,从0开始

        返回值:
            字符串: 词组内容
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取词组: {msg}")
            return ""
            
        try:
            return self._dm.GetWords("", 索引)
        except Exception as e:
            print(f"Error in 获取词组: {str(e)}")
            return ""

    def 识别文字(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内识别文字。

        函数原型:
            string Ocr(x1,y1,x2,y2,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 识别到的文字
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 识别文字: {msg}")
            return ""
            
        try:
            return self._dm.Ocr(x1, y1, x2, y2, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 识别文字: {str(e)}")
            return ""

    def 识别文字Ex(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内识别文字,返回文字和坐标。

        函数原型:
            string OcrEx(x1,y1,x2,y2,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 识别到的文字和坐标,格式为"识别到的文字|x,y"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 识别文字Ex: {msg}")
            return ""
            
        try:
            return self._dm.OcrEx(x1, y1, x2, y2, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 识别文字Ex: {str(e)}")
            return ""

    def 识别文字内存(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内识别文字,使用内存中的字库。

        函数原型:
            string OcrInFile(x1,y1,x2,y2,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 识别到的文字
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 识别文字内存: {msg}")
            return ""
            
        try:
            return self._dm.OcrInFile(x1, y1, x2, y2, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 识别文字内存: {str(e)}")
            return ""

    def 保存字库(self, 文件: str) -> int:
        """
        函数简介:
            保存字库到文件。

        函数原型:
            long SaveDict(index,file)

        参数定义:
            文件 字符串: 要保存的文件名

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 保存字库: {msg}")
            return 0
            
        try:
            return self._dm.SaveDict(0, 文件)
        except Exception as e:
            print(f"Error in 保存字库: {str(e)}")
            return 0

    def 设置字库(self, 字库: str) -> int:
        """
        函数简介:
            设置字库文件。

        函数原型:
            long SetDict(index,dict_info)

        参数定义:
            字库 字符串: 字库文件名

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字库: {msg}")
            return 0
            
        try:
            return self._dm.SetDict(0, 字库)
        except Exception as e:
            print(f"Error in 设置字库: {str(e)}")
            return 0

    def 设置字库内存(self, 字库: str) -> int:
        """
        函数简介:
            设置内存字库。

        函数原型:
            long SetDictMem(index,data,size)

        参数定义:
            字库 字符串: 字库数据

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字库内存: {msg}")
            return 0
            
        try:
            return self._dm.SetDictMem(0, 字库, len(字库))
        except Exception as e:
            print(f"Error in 设置字库内存: {str(e)}")
            return 0

    def 设置字库密码(self, 密码: str) -> int:
        """
        函数简介:
            设置字库密码。

        函数原型:
            long SetDictPwd(pwd)

        参数定义:
            密码 字符串: 字库密码

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字库密码: {msg}")
            return 0
            
        try:
            return self._dm.SetDictPwd(密码)
        except Exception as e:
            print(f"Error in 设置字库密码: {str(e)}")
            return 0

    def 设置最小行距(self, 行距: int) -> int:
        """
        函数简介:
            设置最小行距。

        函数原型:
            long SetMinColGap(min_gap)

        参数定义:
            行距 整形数: 最小行距

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置最小行距: {msg}")
            return 0
            
        try:
            return self._dm.SetMinColGap(行距)
        except Exception as e:
            print(f"Error in 设置最小行距: {str(e)}")
            return 0

    def 设置最小列宽(self, 列宽: int) -> int:
        """
        函数简介:
            设置最小列宽。

        函数原型:
            long SetMinRowGap(min_gap)

        参数定义:
            列宽 整形数: 最小列宽

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置最小列宽: {msg}")
            return 0
            
        try:
            return self._dm.SetMinRowGap(列宽)
        except Exception as e:
            print(f"Error in 设置最小列宽: {str(e)}")
            return 0

    def 设置行间距(self, 行间距: int) -> int:
        """
        函数简介:
            设置行间距。

        函数原型:
            long SetRowGapNoDict(row_gap)

        参数定义:
            行间距 整形数: 行间距

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置行间距: {msg}")
            return 0
            
        try:
            return self._dm.SetRowGapNoDict(行间距)
        except Exception as e:
            print(f"Error in 设置行间距: {str(e)}")
            return 0

    def 设置字间距(self, 字间距: int) -> int:
        """
        函数简介:
            设置字间距。

        函数原型:
            long SetWordGapNoDict(word_gap)

        参数定义:
            字间距 整形数: 字间距

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字间距: {msg}")
            return 0
            
        try:
            return self._dm.SetWordGapNoDict(字间距)
        except Exception as e:
            print(f"Error in 设置字间距: {str(e)}")
            return 0

    def 设置字库行高(self, 行高: int) -> int:
        """
        函数简介:
            设置字库的行高。

        函数原型:
            long SetWordLineHeight(line_height)

        参数定义:
            行高 整形数: 行高

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字库行高: {msg}")
            return 0
            
        try:
            return self._dm.SetWordLineHeight(行高)
        except Exception as e:
            print(f"Error in 设置字库行高: {str(e)}")
            return 0

    def 设置字库无字典(self, 启用: int) -> int:
        """
        函数简介:
            设置是否不使用字库进行识别。

        函数原型:
            long SetWordNoDict(enable)

        参数定义:
            启用 整形数: 0: 使用字库 1: 不使用字库

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字库无字典: {msg}")
            return 0
            
        try:
            return self._dm.SetWordNoDict(启用)
        except Exception as e:
            print(f"Error in 设置字库无字典: {str(e)}")
            return 0

    def 使用字库(self, 序号: int) -> int:
        """
        函数简介:
            使用指定的字库。

        函数原型:
            long UseDict(index)

        参数定义:
            序号 整形数: 字库序号

        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 使用字库: {msg}")
            return 0
            
        try:
            return self._dm.UseDict(序号)
        except Exception as e:
            print(f"Error in 使用字库: {str(e)}")
            return 0

    def 查找字符串(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定的字符串。

        函数原型:
            long FindStr(x1,y1,x2,y2,str,color,sim,intX,intY)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.FindStr(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串: {str(e)}")
            return 0, 0, 0

    def 查找字符串E(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找指定的字符串,并返回坐标。

        函数原型:
            string FindStrE(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回找到的字符串坐标,格式为"x,y"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串E: {msg}")
            return ""
            
        try:
            return self._dm.FindStrE(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串E: {str(e)}")
            return ""

    def 查找字符串Ex(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的字符串。

        函数原型:
            string FindStrEx(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回所有找到的坐标,格式为"x1,y1|x2,y2|x3,y3|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindStrEx(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串Ex: {str(e)}")
            return ""

    def 获取字典(self, 索引: int) -> str:
        """
        函数简介:
            获取指定的字库内容。

        函数原型:
            string GetDict(index)

        参数定义:
            索引 整形数: 字库索引

        返回值:
            字符串: 字库内容
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取字典: {msg}")
            return ""
            
        try:
            return self._dm.GetDict(索引)
        except Exception as e:
            print(f"Error in 获取字典: {str(e)}")
            return ""

    def 查找字符串ExS(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的字符串,返回坐标和字符串。

        函数原型:
            string FindStrExS(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回所有找到的坐标和字符串,格式为"x1,y1,str1|x2,y2,str2|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串ExS: {msg}")
            return ""
            
        try:
            return self._dm.FindStrExS(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串ExS: {str(e)}")
            return ""

    def 查找字符串Fast(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> tuple:
        """
        函数简介:
            在指定的区域内快速查找指定的字符串。

        函数原型:
            long FindStrFast(x1,y1,x2,y2,str,color,sim,intX,intY)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串Fast: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.FindStrFast(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串Fast: {str(e)}")
            return 0, 0, 0

    def 查找字符串FastE(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内快速查找指定的字符串,并返回坐标。

        函数原型:
            string FindStrFastE(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回找到的字符串坐标,格式为"x,y"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串FastE: {msg}")
            return ""
            
        try:
            return self._dm.FindStrFastE(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串FastE: {str(e)}")
            return ""

    def 查找字符串FastEx(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内快速查找所有符合条件的字符串。

        函数原型:
            string FindStrFastEx(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回所有找到的坐标,格式为"x1,y1|x2,y2|x3,y3|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串FastEx: {msg}")
            return ""
            
        try:
            return self._dm.FindStrFastEx(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串FastEx: {str(e)}")
            return ""

    def 查找字符串FastExS(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内快速查找所有符合条件的字符串,返回坐标和字符串。

        函数原型:
            string FindStrFastExS(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回所有找到的坐标和字符串,格式为"x1,y1,str1|x2,y2,str2|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串FastExS: {msg}")
            return ""
            
        try:
            return self._dm.FindStrFastExS(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串FastExS: {str(e)}")
            return ""

    def 查找字符串FastS(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内快速查找指定的字符串,返回坐标和字符串。

        函数原型:
            string FindStrFastS(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回找到的坐标和字符串,格式为"x,y,str"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串FastS: {msg}")
            return ""
            
        try:
            return self._dm.FindStrFastS(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串FastS: {str(e)}")
            return ""

    def 查找字符串S(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找指定的字符串,返回坐标和字符串。

        函数原型:
            string FindStrS(x1,y1,x2,y2,str,color,sim)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0

        返回值:
            字符串: 返回找到的坐标和字符串,格式为"x,y,str"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串S: {msg}")
            return ""
            
        try:
            return self._dm.FindStrS(x1, y1, x2, y2, 字符串, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找字符串S: {str(e)}")
            return ""

    def 查找字符串带字体(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float, 字体: str, 字号: int, 标志: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定字体的字符串。

        函数原型:
            long FindStrWithFont(x1,y1,x2,y2,str,color,sim,font_name,font_size,flag,intX,intY)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
            字体 字符串: 字体名称
            字号 整形数: 字体大小
            标志 整形数: 字体标志,比如粗体,斜体等

        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串带字体: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.FindStrWithFont(x1, y1, x2, y2, 字符串, 颜色, 相似度, 字体, 字号, 标志)
        except Exception as e:
            print(f"Error in 查找字符串带字体: {str(e)}")
            return 0, 0, 0

    def 查找字符串带字体E(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float, 字体: str, 字号: int, 标志: int) -> str:
        """
        函数简介:
            在指定的区域内查找指定字体的字符串,并返回坐标。

        函数原型:
            string FindStrWithFontE(x1,y1,x2,y2,str,color,sim,font_name,font_size,flag)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
            字体 字符串: 字体名称
            字号 整形数: 字体大小
            标志 整形数: 字体标志,比如粗体,斜体等

        返回值:
            字符串: 返回找到的字符串坐标,格式为"x,y"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串带字体E: {msg}")
            return ""
            
        try:
            return self._dm.FindStrWithFontE(x1, y1, x2, y2, 字符串, 颜色, 相似度, 字体, 字号, 标志)
        except Exception as e:
            print(f"Error in 查找字符串带字体E: {str(e)}")
            return ""

    def 查找字符串带字体Ex(self, x1: int, y1: int, x2: int, y2: int, 字符串: str, 颜色: str, 相似度: float, 字体: str, 字号: int, 标志: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的指定字体的字符串。

        函数原型:
            string FindStrWithFontEx(x1,y1,x2,y2,str,color,sim,font_name,font_size,flag)

        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            字符串 字符串: 要查找的字符串
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
            字体 字符串: 字体名称
            字号 整形数: 字体大小
            标志 整形数: 字体标志,比如粗体,斜体等

        返回值:
            字符串: 返回所有找到的坐标,格式为"x1,y1|x2,y2|x3,y3|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找字符串带字体Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindStrWithFontEx(x1, y1, x2, y2, 字符串, 颜色, 相似度, 字体, 字号, 标志)
        except Exception as e:
            print(f"Error in 查找字符串带字体Ex: {str(e)}")
            return ""

    # 添加对应的英文别名
    def FindStrExS(self, *args, **kwargs):
        """英文别名，调用查找字符串ExS"""
        return self.查找字符串ExS(*args, **kwargs)

    def FindStrFast(self, *args, **kwargs):
        """英文别名，调用查找字符串Fast"""
        return self.查找字符串Fast(*args, **kwargs)

    def FindStrFastE(self, *args, **kwargs):
        """英文别名，调用查找字符串FastE"""
        return self.查找字符串FastE(*args, **kwargs)

    def FindStrFastEx(self, *args, **kwargs):
        """英文别名，调用查找字符串FastEx"""
        return self.查找字符串FastEx(*args, **kwargs)

    def FindStrFastExS(self, *args, **kwargs):
        """英文别名，调用查找字符串FastExS"""
        return self.查找字符串FastExS(*args, **kwargs)

    def FindStrFastS(self, *args, **kwargs):
        """英文别名，调用查找字符串FastS"""
        return self.查找字符串FastS(*args, **kwargs)

    def FindStrS(self, *args, **kwargs):
        """英文别名，调用查找字符串S"""
        return self.查找字符串S(*args, **kwargs)

    def FindStrWithFont(self, *args, **kwargs):
        """英文别名，调用查找字符串带字体"""
        return self.查找字符串带字体(*args, **kwargs)

    def FindStrWithFontE(self, *args, **kwargs):
        """英文别名，调用查找字符串带字体E"""
        return self.查找字符串带字体E(*args, **kwargs)

    def FindStrWithFontEx(self, *args, **kwargs):
        """英文别名，调用查找字符串带字体Ex"""
        return self.查找字符串带字体Ex(*args, **kwargs)

    def Ocr(self, *args, **kwargs):
        """英文别名，调用识别文字"""
        return self.识别文字(*args, **kwargs)

    def OcrEx(self, *args, **kwargs):
        """英文别名，调用识别文字Ex"""
        return self.识别文字Ex(*args, **kwargs)

    def OcrInFile(self, *args, **kwargs):
        """英文别名，调用识别文字内存"""
        return self.识别文字内存(*args, **kwargs)

    def SetDict(self, *args, **kwargs):
        """英文别名，调用设置字库"""
        return self.设置字库(*args, **kwargs)

    def SetDictMem(self, *args, **kwargs):
        """英文别名，调用设置字库内存"""
        return self.设置字库内存(*args, **kwargs)

    def SetDictPwd(self, *args, **kwargs):
        """英文别名，调用设置字库密码"""
        return self.设置字库密码(*args, **kwargs)

    def SetMinColGap(self, *args, **kwargs):
        """英文别名，调用设置最小行距"""
        return self.设置最小行距(*args, **kwargs)

    def SetMinRowGap(self, *args, **kwargs):
        """英文别名，调用设置最小列宽"""
        return self.设置最小列宽(*args, **kwargs)

    def SetRowGapNoDict(self, *args, **kwargs):
        """英文别名，调用设置行间距"""
        return self.设置行间距(*args, **kwargs)

    def SetWordGapNoDict(self, *args, **kwargs):
        """英文别名，调用设置字间距"""
        return self.设置字间距(*args, **kwargs) 