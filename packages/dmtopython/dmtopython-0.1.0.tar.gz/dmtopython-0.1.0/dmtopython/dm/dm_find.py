#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件找图找色模块API封装
用于图色查找相关的功能
'''

class DmFind:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 追加图片地址(self, 加密后的地址: str) -> int:
        """
        函数简介:
            追加指定的图片地址到加密后的图片地址序列中。
        
        函数原型:
            long AppendPicAddr(pic_info)
        
        参数定义:
            加密后的地址 字符串: 加密后的图片地址
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.find.追加图片地址("加密的图片地址")
            if ret == 1:
                print("追加图片地址成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 追加图片地址: {msg}")
            return 0
            
        try:
            return self._dm.AppendPicAddr(加密后的地址)
        except Exception as e:
            print(f"Error in 追加图片地址: {str(e)}")
            return 0

    def 比较图片(self, 图片1: str, 图片2: str, 相似度: float) -> int:
        """
        函数简介:
            比较指定的两张图片的相似度。
        
        函数原型:
            long CmpPic(pic_name1,pic_name2,sim)
        
        参数定义:
            图片1 字符串: 第一张图片
            图片2 字符串: 第二张图片
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            整形数: 0: 不相似 1: 相似
        
        示例:
            ret = dm.find.比较图片("1.bmp", "2.bmp", 0.9)
            if ret == 1:
                print("两张图片相似")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 比较图片: {msg}")
            return 0
            
        try:
            return self._dm.CmpPic(图片1, 图片2, 相似度)
        except Exception as e:
            print(f"Error in 比较图片: {str(e)}")
            return 0

    def 查找颜色(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float, 方向: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定的颜色。
        
        函数原型:
            long FindColor(x1,y1,x2,y2,color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB",比如"123456-000000"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向
                      0: 从左到右,从上到下 
                      1: 从左到右,从下到上
                      2: 从右到左,从上到下
                      3: 从右到左,从下到上
                      4: 从中心往外查找
                      5: 从上到下,从左到右
                      6: 从上到下,从右到左
                      7: 从下到上,从左到右
                      8: 从下到上,从右到左
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        
        示例:
            ret, x, y = dm.find.查找颜色(0, 0, 2000, 2000, "123456-000000", 1.0, 0)
            if ret == 1:
                print(f"找到颜色,坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找颜色: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.FindColor(x1, y1, x2, y2, 颜色, 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找颜色: {str(e)}")
            return 0, 0, 0

    def 查找颜色块(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float, 
                  连续性: int, 最小面积: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定的颜色块。
        
        函数原型:
            long FindColorBlock(x1,y1,x2,y2,color,sim,count,width,height,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
            连续性 整形数: 连续性要求
            最小面积 整形数: 最小面积,单位是像素点
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        
        示例:
            ret, x, y = dm.find.查找颜色块(0, 0, 2000, 2000, "123456-000000", 1.0, 1, 100)
            if ret == 1:
                print(f"找到颜色块,坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找颜色块: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.FindColorBlock(x1, y1, x2, y2, 颜色, 相似度, 连续性, 最小面积)
        except Exception as e:
            print(f"Error in 查找颜色块: {str(e)}")
            return 0, 0, 0

    def 查找颜色块Ex(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float, 
                     连续性: int, 最小面积: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的颜色块。
        
        函数原型:
            string FindColorBlockEx(x1,y1,x2,y2,color,sim,count,width,height)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
            连续性 整形数: 连续性要求
            最小面积 整形数: 最小面积,单位是像素点
        
        返回值:
            字符串: 返回所有颜色块信息,格式为"x1,y1,width1,height1|x2,y2,width2,height2|..."
        
        示例:
            ret = dm.find.查找颜色块Ex(0, 0, 2000, 2000, "123456-000000", 1.0, 1, 100)
            if ret:
                blocks = ret.split("|")
                for block in blocks:
                    x, y, w, h = map(int, block.split(","))
                    print(f"找到颜色块: 坐标({x}, {y}), 大小({w}, {h})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找颜色块Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindColorBlockEx(x1, y1, x2, y2, 颜色, 相似度, 连续性, 最小面积)
        except Exception as e:
            print(f"Error in 查找颜色块Ex: {str(e)}")
            return ""

    def 查找颜色Ex(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的颜色。
        
        函数原型:
            string FindColorEx(x1,y1,x2,y2,color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回所有颜色信息,格式为"x1,y1|x2,y2|x3,y3|..."
        
        示例:
            ret = dm.find.查找颜色Ex(0, 0, 2000, 2000, "123456-000000", 1.0, 0)
            if ret:
                points = ret.split("|")
                for point in points:
                    x, y = map(int, point.split(","))
                    print(f"找到颜色点: ({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找颜色Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindColorEx(x1, y1, x2, y2, 颜色, 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找颜色Ex: {str(e)}")
            return ""

    def 查找多点颜色(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float) -> int:
        """
        函数简介:
            在指定的区域内查找多个点颜色。
        
        函数原型:
            long FindMultiColor(x1,y1,x2,y2,first_color,offset_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.find.查找多点颜色(0, 0, 2000, 2000, "123456-000000|1,2,456789-000000|3,4,ABCDEF-000000", 1.0)
            if ret == 1:
                print("找到多点颜色")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找多点颜色: {msg}")
            return 0
            
        try:
            return self._dm.FindMultiColor(x1, y1, x2, y2, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 查找多点颜色: {str(e)}")
            return 0

    def 查找图片(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定的图片。
        
        函数原型:
            long FindPic(x1,y1,x2,y2,pic_name,delta_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标, 整形数: 图片序号)
        
        示例:
            ret, x, y, index = dm.find.查找图片(0, 0, 2000, 2000, "test.bmp", 1.0, 0)
            if ret == 1:
                print(f"找到图片{index},坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片: {msg}")
            return 0, 0, 0, 0
            
        try:
            return self._dm.FindPic(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片: {str(e)}")
            return 0, 0, 0, 0

    def 查找图片Ex(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的图片。
        
        函数原型:
            string FindPicEx(x1,y1,x2,y2,pic_name,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回所有找到的图片信息,格式为"x1,y1,pic1index|x2,y2,pic2index|..."
        
        示例:
            ret = dm.find.查找图片Ex(0, 0, 2000, 2000, "test.bmp|test2.bmp", 1.0, 0)
            if ret:
                pics = ret.split("|")
                for pic in pics:
                    x, y, index = map(int, pic.split(","))
                    print(f"找到图片{index},坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindPicEx(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片Ex: {str(e)}")
            return ""

    def 获取平均颜色(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        函数简介:
            获取指定区域的颜色平均值。
        
        函数原型:
            string GetAveRGB(x1,y1,x2,y2)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
        
        返回值:
            字符串: 颜色字符串,格式"RRGGBB",比如"123456"
        
        示例:
            color = dm.find.获取平均颜色(0, 0, 100, 100)
            print(f"区域平均颜色为: {color}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取平均颜色: {msg}")
            return ""
            
        try:
            return self._dm.GetAveRGB(x1, y1, x2, y2)
        except Exception as e:
            print(f"Error in 获取平均颜色: {str(e)}")
            return ""

    def 查找图片S(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定的图片,使用较快速度。
        
        函数原型:
            long FindPicS(x1,y1,x2,y2,pic_name,delta_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标, 整形数: 图片序号)
        
        示例:
            ret, x, y, index = dm.find.查找图片S(0, 0, 2000, 2000, "test.bmp", 1.0, 0)
            if ret == 1:
                print(f"找到图片{index},坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片S: {msg}")
            return 0, 0, 0, 0
            
        try:
            return self._dm.FindPicS(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片S: {str(e)}")
            return 0, 0, 0, 0

    def 查找图片相似(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定的图片,使用相似度匹配。
        
        函数原型:
            long FindPicSim(x1,y1,x2,y2,pic_name,delta_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标, 整形数: 图片序号)
        
        示例:
            ret, x, y, index = dm.find.查找图片相似(0, 0, 2000, 2000, "test.bmp", 0.9, 0)
            if ret == 1:
                print(f"找到相似图片{index},坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片相似: {msg}")
            return 0, 0, 0, 0
            
        try:
            return self._dm.FindPicSim(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片相似: {str(e)}")
            return 0, 0, 0, 0

    def 查找图片相似Ex(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有相似的图片。
        
        函数原型:
            string FindPicSimEx(x1,y1,x2,y2,pic_name,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回所有找到的图片信息,格式为"x1,y1,sim1,pic1index|x2,y2,sim2,pic2index|..."
        
        示例:
            ret = dm.find.查找图片相似Ex(0, 0, 2000, 2000, "test.bmp|test2.bmp", 0.9, 0)
            if ret:
                pics = ret.split("|")
                for pic in pics:
                    x, y, sim, index = map(float, pic.split(","))
                    print(f"找到相似图片{int(index)},坐标为({int(x)}, {int(y)}),相似度{sim}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片相似Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindPicSimEx(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片相似Ex: {str(e)}")
            return ""

    def 查找形状(self, x1: int, y1: int, x2: int, y2: int, 偏色: str, 相似度: float) -> tuple:
        """
        函数简介:
            在指定的区域内查找指定形状。
        
        函数原型:
            long FindShape(x1,y1,x2,y2,offset_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            偏色 字符串: 偏色,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标)
        
        示例:
            ret, x, y = dm.find.查找形状(0, 0, 2000, 2000, "123456-000000", 0.9)
            if ret == 1:
                print(f"找到形状,坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找形状: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.FindShape(x1, y1, x2, y2, 偏色, 相似度, 0)
        except Exception as e:
            print(f"Error in 查找形状: {str(e)}")
            return 0, 0, 0

    def 查找形状Ex(self, x1: int, y1: int, x2: int, y2: int, 偏色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的形状。
        
        函数原型:
            string FindShapeEx(x1,y1,x2,y2,offset_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            偏色 字符串: 偏色,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            字符串: 返回所有形状的坐标信息,格式为"x1,y1|x2,y2|x3,y3|..."
        
        示例:
            ret = dm.find.查找形状Ex(0, 0, 2000, 2000, "123456-000000", 0.9)
            if ret:
                shapes = ret.split("|")
                for shape in shapes:
                    x, y = map(int, shape.split(","))
                    print(f"找到形状,坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找形状Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindShapeEx(x1, y1, x2, y2, 偏色, 相似度, 0)
        except Exception as e:
            print(f"Error in 查找形状Ex: {str(e)}")
            return ""

    def 查找图片内存(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找已经加载到内存的图片。
        
        函数原型:
            long FindPicMem(x1,y1,x2,y2,pic_info,delta_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标, 整形数: 图片序号)
        
        示例:
            ret, x, y, index = dm.find.查找图片内存(0, 0, 2000, 2000, "test.bmp", 1.0, 0)
            if ret == 1:
                print(f"找到图片{index},坐标为({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片内存: {msg}")
            return 0, 0, 0, 0
            
        try:
            return self._dm.FindPicMem(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片内存: {str(e)}")
            return 0, 0, 0, 0

    def 获取屏幕数据(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        函数简介:
            获取指定区域的屏幕数据。
        
        函数原型:
            string GetScreenData(x1,y1,x2,y2)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
        
        返回值:
            字符串: 返回的是指定区域的二进制数据
        
        示例:
            data = dm.find.获取屏幕数据(0, 0, 100, 100)
            print("获取到屏幕数据")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取屏幕数据: {msg}")
            return ""
            
        try:
            return self._dm.GetScreenData(x1, y1, x2, y2)
        except Exception as e:
            print(f"Error in 获取屏幕数据: {str(e)}")
            return ""

    def 获取屏幕数据位图(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        函数简介:
            获取指定区域的屏幕数据位图。
        
        函数原型:
            string GetScreenDataBmp(x1,y1,x2,y2)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
        
        返回值:
            字符串: 返回的是bmp格式的位图数据
        
        示例:
            data = dm.find.获取屏幕数据位图(0, 0, 100, 100)
            print("获取到屏幕位图数据")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取屏幕数据位图: {msg}")
            return ""
            
        try:
            return self._dm.GetScreenDataBmp(x1, y1, x2, y2)
        except Exception as e:
            print(f"Error in 获取屏幕数据位图: {str(e)}")
            return ""

    def 获取图片大小(self, 图片: str) -> tuple:
        """
        函数简介:
            获取指定图片的大小。
        
        函数原型:
            long GetPicSize(pic_name)
        
        参数定义:
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: 宽度, 整形数: 高度)
        
        示例:
            ret, width, height = dm.find.获取图片大小("test.bmp")
            if ret == 1:
                print(f"图片大小: {width}x{height}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取图片大小: {msg}")
            return 0, 0, 0
            
        try:
            return self._dm.GetPicSize(图片)
        except Exception as e:
            print(f"Error in 获取图片大小: {str(e)}")
            return 0, 0, 0

    def 加载图片(self, 图片: str) -> int:
        """
        函数简介:
            加载指定的图片到内存。
        
        函数原型:
            long LoadPic(pic_name)
        
        参数定义:
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.find.加载图片("test.bmp")
            if ret == 1:
                print("图片加载成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 加载图片: {msg}")
            return 0
            
        try:
            return self._dm.LoadPic(图片)
        except Exception as e:
            print(f"Error in 加载图片: {str(e)}")
            return 0

    def 释放图片(self, 图片: str) -> int:
        """
        函数简介:
            释放指定的已加载的图片。
        
        函数原型:
            long FreePic(pic_name)
        
        参数定义:
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.find.释放图片("test.bmp")
            if ret == 1:
                print("图片释放成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 释放图片: {msg}")
            return 0
            
        try:
            return self._dm.FreePic(图片)
        except Exception as e:
            print(f"Error in 释放图片: {str(e)}")
            return 0

    def 绑定背景图片(self, 图片: str) -> int:
        """
        函数简介:
            绑定指定的图片为背景图片。
        
        函数原型:
            long BindBkImg(pic_name)
        
        参数定义:
            图片 字符串: 图片名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 绑定背景图片: {msg}")
            return 0
            
        try:
            return self._dm.BindBkImg(图片)
        except Exception as e:
            print(f"Error in 绑定背景图片: {str(e)}")
            return 0

    def 截图(self, x1: int, y1: int, x2: int, y2: int, 文件: str) -> int:
        """
        函数简介:
            截取指定区域的图像并保存为BMP格式。
        
        函数原型:
            long Capture(x1,y1,x2,y2,file)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            文件 字符串: 保存的文件名,保存的地方一般为SetPath中设置的目录
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 截图: {msg}")
            return 0
            
        try:
            return self._dm.Capture(x1, y1, x2, y2, 文件)
        except Exception as e:
            print(f"Error in 截图: {str(e)}")
            return 0

    def 截图GIF(self, x1: int, y1: int, x2: int, y2: int, 文件: str, 延时: int, 数量: int) -> int:
        """
        函数简介:
            连续截取指定区域的动画并保存为GIF格式。
        
        函数原型:
            long CaptureGif(x1,y1,x2,y2,file,delay,time)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            文件 字符串: 保存的文件名
            延时 整形数: 每帧间隔,单位毫秒
            数量 整形数: 总共截取多少帧
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 截图GIF: {msg}")
            return 0
            
        try:
            return self._dm.CaptureGif(x1, y1, x2, y2, 文件, 延时, 数量)
        except Exception as e:
            print(f"Error in 截图GIF: {str(e)}")
            return 0

    def 截图PNG(self, x1: int, y1: int, x2: int, y2: int, 文件: str) -> int:
        """
        函数简介:
            截取指定区域的图像并保存为PNG格式。
        
        函数原型:
            long CapturePng(x1,y1,x2,y2,file)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            文件 字符串: 保存的文件名
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 截图PNG: {msg}")
            return 0
            
        try:
            return self._dm.CapturePng(x1, y1, x2, y2, 文件)
        except Exception as e:
            print(f"Error in 截图PNG: {str(e)}")
            return 0

    def 预截图(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        函数简介:
            预先截取指定区域的图像,以便后面的FindPic,CmpPic等接口使用。
        
        函数原型:
            long CapturePre(x1,y1,x2,y2)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 预截图: {msg}")
            return 0
            
        try:
            return self._dm.CapturePre(x1, y1, x2, y2)
        except Exception as e:
            print(f"Error in 预截图: {str(e)}")
            return 0

    def 比较颜色(self, x: int, y: int, 颜色: str, 相似度: float) -> int:
        """
        函数简介:
            比较指定坐标点的颜色。
        
        函数原型:
            long CmpColor(x,y,color,sim)
        
        参数定义:
            x 整形数: X坐标
            y 整形数: Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            整形数: 0: 颜色不匹配 1: 颜色匹配
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 比较颜色: {msg}")
            return 0
            
        try:
            return self._dm.CmpColor(x, y, 颜色, 相似度)
        except Exception as e:
            print(f"Error in 比较颜色: {str(e)}")
            return 0

    def 启用调试显示(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启调试图色功能。
        
        函数原型:
            long EnableDisplayDebug(enable_debug)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用调试显示: {msg}")
            return 0
            
        try:
            return self._dm.EnableDisplayDebug(启用)
        except Exception as e:
            print(f"Error in 启用调试显示: {str(e)}")
            return 0

    def 启用找图多线程(self, 线程数: int) -> int:
        """
        函数简介:
            设置是否开启找图多线程。
        
        函数原型:
            long EnableFindPicMultithread(enable)
        
        参数定义:
            线程数 整形数: 线程数
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用找图多线程: {msg}")
            return 0
            
        try:
            return self._dm.EnableFindPicMultithread(线程数)
        except Exception as e:
            print(f"Error in 启用找图多线程: {str(e)}")
            return 0

    def 启用截图找色(self, 启用: int) -> int:
        """
        函数简介:
            设置是否开启截图找色功能。
        
        函数原型:
            long EnableGetColorByCapture(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用截图找色: {msg}")
            return 0
            
        try:
            return self._dm.EnableGetColorByCapture(启用)
        except Exception as e:
            print(f"Error in 启用截图找色: {str(e)}")
            return 0

    # 添加剩余的英文别名
    def FindPicS(self, *args, **kwargs):
        """英文别名，调用查找图片S"""
        return self.查找图片S(*args, **kwargs)

    def FindPicSim(self, *args, **kwargs):
        """英文别名，调用查找图片相似"""
        return self.查找图片相似(*args, **kwargs)

    def FindPicSimEx(self, *args, **kwargs):
        """英文别名，调用查找图片相似Ex"""
        return self.查找图片相似Ex(*args, **kwargs)

    def FindShape(self, *args, **kwargs):
        """英文别名，调用查找形状"""
        return self.查找形状(*args, **kwargs)

    def FindShapeEx(self, *args, **kwargs):
        """英文别名，调用查找形状Ex"""
        return self.查找形状Ex(*args, **kwargs)

    def FindPicMem(self, *args, **kwargs):
        """英文别名，调用查找图片内存"""
        return self.查找图片内存(*args, **kwargs)

    def GetScreenData(self, *args, **kwargs):
        """英文别名，调用获取屏幕数据"""
        return self.获取屏幕数据(*args, **kwargs)

    def GetScreenDataBmp(self, *args, **kwargs):
        """英文别名，调用获取屏幕数据位图"""
        return self.获取屏幕数据位图(*args, **kwargs)

    def GetPicSize(self, *args, **kwargs):
        """英文别名，调用获取图片大小"""
        return self.获取图片大小(*args, **kwargs)

    def LoadPic(self, *args, **kwargs):
        """英文别名，调用加载图片"""
        return self.加载图片(*args, **kwargs)

    def FreePic(self, *args, **kwargs):
        """英文别名，调用释放图片"""
        return self.释放图片(*args, **kwargs)

    # 添加英文别名
    def AppendPicAddr(self, *args, **kwargs):
        """英文别名，调用追加图片地址"""
        return self.追加图片地址(*args, **kwargs)

    def CmpPic(self, *args, **kwargs):
        """英文别名，调用比较图片"""
        return self.比较图片(*args, **kwargs)

    def FindColor(self, *args, **kwargs):
        """英文别名，调用查找颜色"""
        return self.查找颜色(*args, **kwargs)

    def FindColorBlock(self, *args, **kwargs):
        """英文别名，调用查找颜色块"""
        return self.查找颜色块(*args, **kwargs)

    def FindColorBlockEx(self, *args, **kwargs):
        """英文别名，调用查找颜色块Ex"""
        return self.查找颜色块Ex(*args, **kwargs)

    def FindColorEx(self, *args, **kwargs):
        """英文别名，调用查找颜色Ex"""
        return self.查找颜色Ex(*args, **kwargs)

    def FindMultiColor(self, *args, **kwargs):
        """英文别名，调用查找多点颜色"""
        return self.查找多点颜色(*args, **kwargs)

    def FindPic(self, *args, **kwargs):
        """英文别名，调用查找图片"""
        return self.查找图片(*args, **kwargs)

    def FindPicEx(self, *args, **kwargs):
        """英文别名，调用查找图片Ex"""
        return self.查找图片Ex(*args, **kwargs)

    def 查找多点颜色Ex(self, x1: int, y1: int, x2: int, y2: int, 颜色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的多点颜色。
        
        函数原型:
            string FindMultiColorEx(x1,y1,x2,y2,first_color,offset_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            颜色 字符串: 颜色格式串,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            字符串: 返回所有找到的坐标,格式为"x1,y1|x2,y2|x3,y3"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找多点颜色Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindMultiColorEx(x1, y1, x2, y2, 颜色, "", 相似度, 0)
        except Exception as e:
            print(f"Error in 查找多点颜色Ex: {str(e)}")
            return ""

    def 查找图片ExS(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的图片,使用较快速度。
        
        函数原型:
            string FindPicExS(x1,y1,x2,y2,pic_name,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回所有找到的图片信息,格式为"x1,y1,pic1index|x2,y2,pic2index|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片ExS: {msg}")
            return ""
            
        try:
            return self._dm.FindPicExS(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片ExS: {str(e)}")
            return ""

    def 查找图片内存Ex(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有已加载到内存中的图片。
        
        函数原型:
            string FindPicMemEx(x1,y1,x2,y2,pic_info,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回所有找到的图片信息,格式为"x1,y1,pic1index|x2,y2,pic2index|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片内存Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindPicMemEx(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片内存Ex: {str(e)}")
            return ""

    def 获取颜色(self, x: int, y: int) -> str:
        """
        函数简介:
            获取指定坐标点的颜色。
        
        函数原型:
            string GetColor(x,y)
        
        参数定义:
            x 整形数: X坐标
            y 整形数: Y坐标
        
        返回值:
            字符串: 颜色字符串,格式"RRGGBB",比如"123456"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取颜色: {msg}")
            return ""
            
        try:
            return self._dm.GetColor(x, y)
        except Exception as e:
            print(f"Error in 获取颜色: {str(e)}")
            return ""

    def 获取颜色BGR(self, x: int, y: int) -> str:
        """
        函数简介:
            获取指定坐标点的BGR颜色。
        
        函数原型:
            string GetColorBGR(x,y)
        
        参数定义:
            x 整形数: X坐标
            y 整形数: Y坐标
        
        返回值:
            字符串: BGR颜色字符串,格式"BBGGRR",比如"563412"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取颜色BGR: {msg}")
            return ""
            
        try:
            return self._dm.GetColorBGR(x, y)
        except Exception as e:
            print(f"Error in 获取颜色BGR: {str(e)}")
            return ""

    def 获取颜色HSV(self, x: int, y: int) -> str:
        """
        函数简介:
            获取指定坐标点的HSV颜色。
        
        函数原型:
            string GetColorHSV(x,y)
        
        参数定义:
            x 整形数: X坐标
            y 整形数: Y坐标
        
        返回值:
            字符串: HSV颜色字符串,格式"H.S.V",比如"0.0.100"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取颜色HSV: {msg}")
            return ""
            
        try:
            return self._dm.GetColorHSV(x, y)
        except Exception as e:
            print(f"Error in 获取颜色HSV: {str(e)}")
            return ""

    def 获取平均HSV(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        函数简介:
            获取指定区域的HSV颜色平均值。
        
        函数原型:
            string GetAveHSV(x1,y1,x2,y2)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
        
        返回值:
            字符串: HSV颜色字符串,格式"H.S.V",比如"0.0.100"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 获取平均HSV: {msg}")
            return ""
            
        try:
            return self._dm.GetAveHSV(x1, y1, x2, y2)
        except Exception as e:
            print(f"Error in 获取平均HSV: {str(e)}")
            return ""

    def RGB转BGR(self, rgb: str) -> str:
        """
        函数简介:
            将RGB颜色格式转换为BGR格式。
        
        函数原型:
            string RGB2BGR(rgb_color)
        
        参数定义:
            rgb 字符串: RGB颜色字符串,格式"RRGGBB"
        
        返回值:
            字符串: BGR颜色字符串,格式"BBGGRR"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in RGB转BGR: {msg}")
            return ""
            
        try:
            return self._dm.RGB2BGR(rgb)
        except Exception as e:
            print(f"Error in RGB转BGR: {str(e)}")
            return ""

    def 设置排除区域(self, 类型: int, info: str) -> int:
        """
        函数简介:
            设置图色查找时的排除区域。
        
        函数原型:
            long SetExcludeRegion(type,info)
        
        参数定义:
            类型 整形数: 0: 添加排除区域 1: 清除排除区域
            info 字符串: 排除区域信息,可以支持多个区域,格式为"x1,y1,x2,y2|x1,y1,x2,y2|..."
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置排除区域: {msg}")
            return 0
            
        try:
            return self._dm.SetExcludeRegion(类型, info)
        except Exception as e:
            print(f"Error in 设置排除区域: {str(e)}")
            return 0

    def 设置找图线程限制(self, 限制: int) -> int:
        """
        函数简介:
            设置找图线程限制。
        
        函数原型:
            long SetFindPicMultithreadLimit(limit)
        
        参数定义:
            限制 整形数: 线程限制数
        
        返回值:
            整形数: 0: 失败 1: 成功
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置找图线程限制: {msg}")
            return 0
            
        try:
            return self._dm.SetFindPicMultithreadLimit(限制)
        except Exception as e:
            print(f"Error in 设置找图线程限制: {str(e)}")
            return 0

    # 添加对应的英文别名
    def GetColor(self, *args, **kwargs):
        """英文别名，调用获取颜色"""
        return self.获取颜色(*args, **kwargs)

    def GetColorBGR(self, *args, **kwargs):
        """英文别名，调用获取颜色BGR"""
        return self.获取颜色BGR(*args, **kwargs)

    def GetColorHSV(self, *args, **kwargs):
        """英文别名，调用获取颜色HSV"""
        return self.获取颜色HSV(*args, **kwargs)

    def GetAveHSV(self, *args, **kwargs):
        """英文别名，调用获取平均HSV"""
        return self.获取平均HSV(*args, **kwargs)

    def RGB2BGR(self, *args, **kwargs):
        """英文别名，调用RGB转BGR"""
        return self.RGB转BGR(*args, **kwargs)

    def SetExcludeRegion(self, *args, **kwargs):
        """英文别名，调用设置排除区域"""
        return self.设置排除区域(*args, **kwargs)

    def SetFindPicMultithreadLimit(self, *args, **kwargs):
        """英文别名，调用设置找图线程限制"""
        return self.设置找图线程限制(*args, **kwargs)

    def 查找图片相似内存(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> tuple:
        """
        函数简介:
            在指定的区域内查找已加载到内存中的相似图片。
        
        函数原型:
            long FindPicSimMem(x1,y1,x2,y2,pic_info,delta_color,sim,dir,intX,intY)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            元组: (整形数: 0: 失败 1: 成功, 整形数: X坐标, 整形数: Y坐标, 整形数: 图片序号)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片相似内存: {msg}")
            return 0, 0, 0, 0
            
        try:
            return self._dm.FindPicSimMem(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片相似内存: {str(e)}")
            return 0, 0, 0, 0

    def 查找图片相似内存Ex(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找所有已加载到内存中的相似图片。
        
        函数原型:
            string FindPicSimMemEx(x1,y1,x2,y2,pic_info,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回所有找到的图片信息,格式为"x1,y1,sim1,pic1index|x2,y2,sim2,pic2index|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片相似内存Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindPicSimMemEx(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片相似内存Ex: {str(e)}")
            return ""

    def 加载图片字节(self, addr: str, size: int, 是否为图片信息: int) -> str:
        """
        函数简介:
            加载指定的图片字节数据。
        
        函数原型:
            string LoadPicByte(addr,size,is_pic_info)
        
        参数定义:
            addr 字符串: 图片字节数据的地址
            size 整形数: 字节数据的大小
            是否为图片信息 整形数: 0: 不是图片信息 1: 是图片信息
        
        返回值:
            字符串: 返回加载的图片信息
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 加载图片字节: {msg}")
            return ""
            
        try:
            return self._dm.LoadPicByte(addr, size, 是否为图片信息)
        except Exception as e:
            print(f"Error in 加载图片字节: {str(e)}")
            return ""

    def 匹配图片名(self, 图片: str) -> str:
        """
        函数简介:
            匹配指定的图片名。
        
        函数原型:
            string MatchPicName(pic_name)
        
        参数定义:
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        
        返回值:
            字符串: 返回匹配的图片名
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 匹配图片名: {msg}")
            return ""
            
        try:
            return self._dm.MatchPicName(图片)
        except Exception as e:
            print(f"Error in 匹配图片名: {str(e)}")
            return ""

    # 添加对应的英文别名
    def FindPicSimMem(self, *args, **kwargs):
        """英文别名，调用查找图片相似内存"""
        return self.查找图片相似内存(*args, **kwargs)

    def FindPicSimMemEx(self, *args, **kwargs):
        """英文别名，调用查找图片相似内存Ex"""
        return self.查找图片相似内存Ex(*args, **kwargs)

    def LoadPicByte(self, *args, **kwargs):
        """英文别名，调用加载图片字节"""
        return self.加载图片字节(*args, **kwargs)

    def MatchPicName(self, *args, **kwargs):
        """英文别名，调用匹配图片名"""
        return self.匹配图片名(*args, **kwargs)

    def 显示是否消失(self) -> int:
        """
        函数简介:
            判断图色是否消失。
        
        函数原型:
            long IsDisplayDead()
        
        参数定义:
            无
        
        返回值:
            整形数: 0: 没有消失 1: 已经消失
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 显示是否消失: {msg}")
            return 0
            
        try:
            return self._dm.IsDisplayDead()
        except Exception as e:
            print(f"Error in 显示是否消失: {str(e)}")
            return 0

    def 查找形状E(self, x1: int, y1: int, x2: int, y2: int, 偏色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找指定形状。
        
        函数原型:
            string FindShapeE(x1,y1,x2,y2,offset_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            偏色 字符串: 偏色,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            字符串: 返回所有形状的坐标信息,格式为"x1,y1|x2,y2|x3,y3|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找形状E: {msg}")
            return ""
            
        try:
            return self._dm.FindShapeE(x1, y1, x2, y2, 偏色, 相似度, 0)
        except Exception as e:
            print(f"Error in 查找形状E: {str(e)}")
            return ""

    # 添加对应的英文别名
    def IsDisplayDead(self, *args, **kwargs):
        """英文别名，调用显示是否消失"""
        return self.显示是否消失(*args, **kwargs)

    def FindShapeE(self, *args, **kwargs):
        """英文别名，调用查找形状E"""
        return self.查找形状E(*args, **kwargs)

    def BindBkImg(self, *args, **kwargs):
        """英文别名，调用绑定背景图片"""
        return self.绑定背景图片(*args, **kwargs)

    def Capture(self, *args, **kwargs):
        """英文别名，调用截图"""
        return self.截图(*args, **kwargs)

    def CaptureGif(self, *args, **kwargs):
        """英文别名，调用截图GIF"""
        return self.截图GIF(*args, **kwargs)

    def CapturePng(self, *args, **kwargs):
        """英文别名，调用截图PNG"""
        return self.截图PNG(*args, **kwargs)

    def CapturePre(self, *args, **kwargs):
        """英文别名，调用预截图"""
        return self.预截图(*args, **kwargs)

    def CmpColor(self, *args, **kwargs):
        """英文别名，调用比较颜色"""
        return self.比较颜色(*args, **kwargs)

    def EnableDisplayDebug(self, *args, **kwargs):
        """英文别名，调用启用调试显示"""
        return self.启用调试显示(*args, **kwargs)

    def EnableFindPicMultithread(self, *args, **kwargs):
        """英文别名，调用启用找图多线程"""
        return self.启用找图多线程(*args, **kwargs)

    def EnableGetColorByCapture(self, *args, **kwargs):
        """英文别名，调用启用截图找色"""
        return self.启用截图找色(*args, **kwargs)

    def 查找图片E(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找指定的图片。
        
        函数原型:
            string FindPicE(x1,y1,x2,y2,pic_name,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回找到的图片信息,格式为"x,y,pic_index"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片E: {msg}")
            return ""
            
        try:
            return self._dm.FindPicE(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片E: {str(e)}")
            return ""

    def 查找图片内存E(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找已加载到内存中的图片。
        
        函数原型:
            string FindPicMemE(x1,y1,x2,y2,pic_info,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回找到的图片信息,格式为"x,y,pic_index"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片内存E: {msg}")
            return ""
            
        try:
            return self._dm.FindPicMemE(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片内存E: {str(e)}")
            return ""

    def 查找图片相似E(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找相似图片。
        
        函数原型:
            string FindPicSimE(x1,y1,x2,y2,pic_name,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回找到的图片信息,格式为"x,y,sim,pic_index"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片相似E: {msg}")
            return ""
            
        try:
            return self._dm.FindPicSimE(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片相似E: {str(e)}")
            return ""

    def 查找图片相似内存E(self, x1: int, y1: int, x2: int, y2: int, 图片: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            在指定的区域内查找已加载到内存中的相似图片。
        
        函数原型:
            string FindPicSimMemE(x1,y1,x2,y2,pic_info,delta_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            图片 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 小数型: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向,可参考查找颜色的方向说明
        
        返回值:
            字符串: 返回找到的图片信息,格式为"x,y,sim,pic_index"
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找图片相似内存E: {msg}")
            return ""
            
        try:
            return self._dm.FindPicSimMemE(x1, y1, x2, y2, 图片, "", 相似度, 方向)
        except Exception as e:
            print(f"Error in 查找图片相似内存E: {str(e)}")
            return ""

    def 查找形状Ex(self, x1: int, y1: int, x2: int, y2: int, 偏色: str, 相似度: float) -> str:
        """
        函数简介:
            在指定的区域内查找所有符合条件的形状。
        
        函数原型:
            string FindShapeEx(x1,y1,x2,y2,offset_color,sim,dir)
        
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            偏色 字符串: 偏色,可以支持偏色,格式为"RRGGBB-DRDGDB"
            相似度 小数型: 相似度,取值范围0.1-1.0
        
        返回值:
            字符串: 返回所有形状的坐标信息,格式为"x1,y1|x2,y2|x3,y3|..."
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 查找形状Ex: {msg}")
            return ""
            
        try:
            return self._dm.FindShapeEx(x1, y1, x2, y2, 偏色, 相似度, 0)
        except Exception as e:
            print(f"Error in 查找形状Ex: {str(e)}")
            return ""

    # 添加对应的英文别名
    def FindPicE(self, *args, **kwargs):
        """英文别名，调用查找图片E"""
        return self.查找图片E(*args, **kwargs)

    def FindPicMemE(self, *args, **kwargs):
        """英文别名，调用查找图片内存E"""
        return self.查找图片内存E(*args, **kwargs)

    def FindPicSimE(self, *args, **kwargs):
        """英文别名，调用查找图片相似E"""
        return self.查找图片相似E(*args, **kwargs)

    def FindPicSimMemE(self, *args, **kwargs):
        """英文别名，调用查找图片相似内存E"""
        return self.查找图片相似内存E(*args, **kwargs)

    def FindShapeEx(self, *args, **kwargs):
        """英文别名，调用查找形状Ex"""
        return self.查找形状Ex(*args, **kwargs)

    def 设置图片密码(self, 密码: str) -> int:
        """
        函数简介:
            设置图片密码，对于加密的图片，此函数必须在使用图片之前调用。

        函数原型:
            long SetPicPwd(pwd)

        参数定义:
            密码 字符串: 图片密码

        返回值:
            整形数: 0: 失败 1: 成功

        示例:
            ret = dm.find.设置图片密码("123456")
            if ret == 1:
                print("设置图片密码成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置图片密码: {msg}")
            return 0
            
        try:
            return self._dm.SetPicPwd(密码)
        except Exception as e:
            print(f"Error in 设置图片密码: {str(e)}")
            return 0

    # 添加对应的英文别名
    def SetPicPwd(self, *args, **kwargs):
        """英文别名，调用设置图片密码"""
        return self.设置图片密码(*args, **kwargs)

    # ... 继续添加其他英文别名 ... 