#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件Foobar模块API封装
用于创建和操作自定义的工具栏窗口
'''

class DmFoobar:
    def __init__(self, dm=None):
        self._dm = dm

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def 创建自定义(self, 窗口句柄: int, 横坐标: int, 纵坐标: int, 图片名: str, 透明色: str, 相似度: float) -> int:
        """
        函数简介:
            根据指定的位图创建一个自定义形状的窗口
        
        函数原型:
            long CreateFoobarCustom(hwnd,x,y,pic_name,trans_color,sim)
        
        参数定义:
            窗口句柄 整形数: 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
            横坐标 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            纵坐标 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            图片名 字符串: 位图名字. 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制
            透明色 字符串: 透明色(RRGGBB)
            相似度 双精度浮点数: 透明色的相似值 0.1-1.0
        
        返回值:
            整形数: 创建成功的窗口句柄
        
        示例:
            foobar = dm.CreateFoobarCustom(hwnd,10,10,"菜单.bmp","FF00FF",1.0)
            foobar = dm.CreateFoobarCustom(hwnd,10,10,"@9237392578,2345","FF00FF",1.0)
        
        注: 
            foobar不能在本进程窗口内创建.
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 创建自定义: {msg}")
            return 0
            
        try:
            return self._dm.CreateFoobarCustom(窗口句柄, 横坐标, 纵坐标, 图片名, 透明色, 相似度)
        except Exception as e:
            print(f"Error in 创建自定义: {str(e)}")
            return 0

    def 创建椭圆(self, 横坐标: int, 纵坐标: int, 宽度: int, 高度: int, 颜色: str, 透明色: str, 相似度: float) -> int:
        """
        函数简介:
            在指定的位置创建一个椭圆
        
        函数原型:
            long CreateFoobarEllipse(x,y,w,h,color,trans_color,sim)
        
        参数定义:
            横坐标 整形数: 左上角X坐标
            纵坐标 整形数: 左上角Y坐标
            宽度 整形数: 椭圆的宽度
            高度 整形数: 椭圆的高度
            颜色 字符串: 填充颜色 格式"RRGGBB"
            透明色 字符串: 透明颜色 格式"RRGGBB"
            相似度 双精度浮点数: 透明色的相似值 0.1-1.0
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.创建椭圆(10, 10, 50, 30, "ff0000", "000000", 1.0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 创建椭圆: {msg}")
            return 0
            
        try:
            return self._dm.CreateFoobarEllipse(横坐标, 纵坐标, 宽度, 高度, 颜色, 透明色, 相似度)
        except Exception as e:
            print(f"Error in 创建椭圆: {str(e)}")
            return 0

    def 创建矩形(self, 横坐标: int, 纵坐标: int, 宽度: int, 高度: int, 颜色: str, 透明色: str, 相似度: float) -> int:
        """
        函数简介:
            在指定的位置创建一个矩形
        
        函数原型:
            long CreateFoobarRect(x,y,w,h,color,trans_color,sim)
        
        参数定义:
            横坐标 整形数: 左上角X坐标
            纵坐标 整形数: 左上角Y坐标
            宽度 整形数: 矩形的宽度
            高度 整形数: 矩形的高度
            颜色 字符串: 填充颜色 格式"RRGGBB"
            透明色 字符串: 透明颜色 格式"RRGGBB"
            相似度 双精度浮点数: 透明色的相似值 0.1-1.0
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.创建矩形(10, 10, 50, 30, "ff0000", "000000", 1.0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 创建矩形: {msg}")
            return 0
            
        try:
            return self._dm.CreateFoobarRect(横坐标, 纵坐标, 宽度, 高度, 颜色, 透明色, 相似度)
        except Exception as e:
            print(f"Error in 创建矩形: {str(e)}")
            return 0

    def 创建圆角矩形(self, 横坐标: int, 纵坐标: int, 宽度: int, 高度: int, 颜色: str, 透明色: str, 相似度: float) -> int:
        """
        函数简介:
            在指定的位置创建一个圆角矩形
        
        函数原型:
            long CreateFoobarRoundRect(x,y,w,h,color,trans_color,sim)
        
        参数定义:
            横坐标 整形数: 左上角X坐标
            纵坐标 整形数: 左上角Y坐标
            宽度 整形数: 矩形的宽度
            高度 整形数: 矩形的高度
            颜色 字符串: 填充颜色 格式"RRGGBB"
            透明色 字符串: 透明颜色 格式"RRGGBB"
            相似度 双精度浮点数: 透明色的相似值 0.1-1.0
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.创建圆角矩形(10, 10, 50, 30, "ff0000", "000000", 1.0)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 创建圆角矩形: {msg}")
            return 0
            
        try:
            return self._dm.CreateFoobarRoundRect(横坐标, 纵坐标, 宽度, 高度, 颜色, 透明色, 相似度)
        except Exception as e:
            print(f"Error in 创建圆角矩形: {str(e)}")
            return 0

    def 清除文本(self) -> int:
        """
        函数简介:
            清除已经存在的所有文本。
            此函数会清除工具栏上所有已经显示的文本。
            如果需要重新显示文本，需要重新调用打印文本或绘制文本函数。
        
        函数原型:
            long FoobarClearText()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.清除文本()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 清除文本: {msg}")
            return 0
            
        try:
            return self._dm.FoobarClearText()
        except Exception as e:
            print(f"Error in 清除文本: {str(e)}")
            return 0

    def 关闭(self) -> int:
        """
        函数简介:
            关闭已经创建的工具栏。
            此函数会释放工具栏占用的所有资源。
            在程序结束前必须调用此函数释放工具栏，否则可能会导致下次无法创建工具栏。
        
        函数原型:
            long FoobarClose()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.关闭()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 关闭: {msg}")
            return 0
            
        try:
            return self._dm.FoobarClose()
        except Exception as e:
            print(f"Error in 关闭: {str(e)}")
            return 0

    def 画线(self, 起点x: int, 起点y: int, 终点x: int, 终点y: int, 颜色: str, 样式: int, 宽度: int) -> int:
        """
        函数简介:
            在指定的位置画线。
            此函数用于在工具栏上绘制直线。
            线条可以是实线或虚线，可以设置颜色和宽度。
        
        函数原型:
            long FoobarDrawLine(x1,y1,x2,y2,color,style,width)
        
        参数定义:
            起点x 整形数: 起点X坐标
            起点y 整形数: 起点Y坐标
            终点x 整形数: 终点X坐标
            终点y 整形数: 终点Y坐标
            颜色 字符串: 线条颜色 格式"RRGGBB"
            样式 整形数: 线条样式 0: 实线 1: 虚线
            宽度 整形数: 线条宽度
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.画线(10, 10, 100, 100, "ff0000", 0, 1)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 画线: {msg}")
            return 0
            
        try:
            return self._dm.FoobarDrawLine(起点x, 起点y, 终点x, 终点y, 颜色, 样式, 宽度)
        except Exception as e:
            print(f"Error in 画线: {str(e)}")
            return 0

    def 画图(self, 横坐标: int, 纵坐标: int, 图片名: str) -> int:
        """
        函数简介:
            在指定的位置画图片。
            图片是相对于工具栏而言的，不是屏幕。
            要注意现在的大漠插件，对于图像格式支持较少。
            24位bmp是完全支持的,其他格式不完全支持。
            所以尽量用24位bmp图片。
        
        函数原型:
            long FoobarDrawPic(x,y,pic_name)
        
        参数定义:
            横坐标 整形数: 图片左上角X坐标
            纵坐标 整形数: 图片左上角Y坐标
            图片名 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.画图(10, 10, "test.bmp")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 画图: {msg}")
            return 0
        
        try:
            return self._dm.FoobarDrawPic(横坐标, 纵坐标, 图片名)
        except Exception as e:
            print(f"Error in 画图: {str(e)}")
            return 0

    def 绘制文本(self, 横坐标: int, 纵坐标: int, 文本: str) -> int:
        """
        函数简介:
            在指定的位置写文字。
            此函数用于在工具栏的指定位置绘制文本。
            文本会根据当前的字体设置来显示。
        
        函数原型:
            long FoobarDrawText(x,y,text)
        
        参数定义:
            横坐标 整形数: 左上角X坐标
            纵坐标 整形数: 左上角Y坐标
            文本 字符串: 要显示的文本内容
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.绘制文本(10, 10, "hello")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 绘制文本: {msg}")
            return 0
        
        try:
            return self._dm.FoobarDrawText(横坐标, 纵坐标, 文本)
        except Exception as e:
            print(f"Error in 绘制文本: {str(e)}")
            return 0

    def 填充矩形(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 颜色: str) -> int:
        """
        函数简介:
            在指定的位置填充矩形。
            此函数用于在工具栏上填充一个实心矩形。
            可以指定填充颜色。
        
        函数原型:
            long FoobarFillRect(x1,y1,x2,y2,color)
        
        参数定义:
            左上x 整形数: 左上角X坐标
            左上y 整形数: 左上角Y坐标
            右下x 整形数: 右下角X坐标
            右下y 整形数: 右下角Y坐标
            颜色 字符串: 填充颜色 格式"RRGGBB"
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.填充矩形(10, 10, 100, 100, "ff0000")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 填充矩形: {msg}")
            return 0
            
        try:
            return self._dm.FoobarFillRect(左上x, 左上y, 右下x, 右下y, 颜色)
        except Exception as e:
            print(f"Error in 填充矩形: {str(e)}")
            return 0

    def 锁定(self, 状态: int) -> int:
        """
        函数简介:
            锁定指定的工具栏,不能再加入图片和文字等。
            锁定后工具栏将不能再添加任何内容。
            需要添加内容时需要先调用解锁函数。
        
        函数原型:
            long FoobarLock(lock)
        
        参数定义:
            状态 整形数: 0: 解锁 1: 锁定
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.锁定(1)  # 锁定工具栏
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 锁定: {msg}")
            return 0
        
        try:
            return self._dm.FoobarLock(状态)
        except Exception as e:
            print(f"Error in 锁定: {str(e)}")
            return 0

    def 打印文本(self, 文本: str) -> int:
        """
        函数简介:
            在工具栏上打印文字,可以替换原来的文字或者加入新的文字。
            此函数是在工具栏最后一行追加一行文本。
            如果要替换原来的文本,需要调用清除文本函数。
            文本会根据当前的字体设置来显示。
        
        函数原型:
            long FoobarPrintText(text)
        
        参数定义:
            文本 字符串: 要打印的文字串. 如果要换行,可以用\\n
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.打印文本("hello\\nworld")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 打印文本: {msg}")
            return 0
        
        try:
            return self._dm.FoobarPrintText(文本)
        except Exception as e:
            print(f"Error in 打印文本: {str(e)}")
            return 0

    def 设置字体(self, 字体名称: str, 大小: int, 样式: int) -> int:
        """
        函数简介:
            设置文字的字体,大小,样式等。
            此函数会影响后续所有文本显示的字体样式。
        
        函数原型:
            long FoobarSetFont(font_name,size,flag)
        
        参数定义:
            字体名称 字符串: 字体名称
            大小 整形数: 字体大小
            样式 整形数: 取值定义如下:
                       0 : 正常
                       1 : 粗体
                       2 : 斜体
                       4 : 下划线
                       8 : 删除线
                       这些值可以相加,比如粗体加斜体就是1+2=3
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.设置字体("宋体", 12, 1)  # 设置粗体宋体12号字
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置字体: {msg}")
            return 0
        
        try:
            return self._dm.FoobarSetFont(字体名称, 大小, 样式)
        except Exception as e:
            print(f"Error in 设置字体: {str(e)}")
            return 0

    def 设置保存(self, 文件名: str) -> int:
        """
        函数简介:
            把工具栏保存到文件,可以用于加密处理。
            此函数可以将当前工具栏的所有设置保存到指定文件中。
        
        函数原型:
            long FoobarSetSave(file)
        
        参数定义:
            文件名 字符串: 保存的文件名
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.设置保存("test.fbt")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置保存: {msg}")
            return 0
            
        try:
            return self._dm.FoobarSetSave(文件名)
        except Exception as e:
            print(f"Error in 设置保存: {str(e)}")
            return 0

    def 开始GIF(self, 横坐标: int, 纵坐标: int, 图片名: str, 播放次数: int) -> int:
        """
        函数简介:
            在指定的位置显示动画GIF图片。
            此函数不阻塞，也就是说GIF图片会一直播放。
            直到主动调用停止GIF函数来停止。
        
        函数原型:
            long FoobarStartGif(x,y,pic_name,repeat_limit)
        
        参数定义:
            横坐标 整形数: 左上角X坐标
            纵坐标 整形数: 左上角Y坐标
            图片名 字符串: 图片名
            播放次数 整形数: 播放次数,0表示一直播放
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.开始GIF(10, 10, "test.gif", 0)  # 无限循环播放
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 开始GIF: {msg}")
            return 0
        
        try:
            return self._dm.FoobarStartGif(横坐标, 纵坐标, 图片名, 播放次数)
        except Exception as e:
            print(f"Error in 开始GIF: {str(e)}")
            return 0

    def 停止GIF(self) -> int:
        """
        函数简介:
            停止正在播放的GIF动画。
            此函数用于停止由开始GIF函数启动的GIF动画。
        
        函数原型:
            long FoobarStopGif()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.停止GIF()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 停止GIF: {msg}")
            return 0
        
        try:
            return self._dm.FoobarStopGif()
        except Exception as e:
            print(f"Error in 停止GIF: {str(e)}")
            return 0

    def 设置文本行间距(self, 间距: int) -> int:
        """
        函数简介:
            设置文本行之间的间距。
            默认间距是3像素。
            此设置会影响后续所有的文本显示。
        
        函数原型:
            long FoobarTextLineGap(gap)
        
        参数定义:
            间距 整形数: 间距,单位是像素
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.设置文本行间距(5)  # 设置行间距为5像素
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置文本行间距: {msg}")
            return 0
        
        try:
            return self._dm.FoobarTextLineGap(间距)
        except Exception as e:
            print(f"Error in 设置文本行间距: {str(e)}")
            return 0

    def 设置文本打印方向(self, 方向: int) -> int:
        """
        函数简介:
            设置文本打印时的方向。
            此函数用于设置文本的显示方向。
            设置后会影响后续所有文本的显示方向。
        
        函数原型:
            long FoobarTextPrintDir(dir)
        
        参数定义:
            方向 整形数: 文本方向
                       0: 从左到右打印文本
                       1: 从右到左打印文本
                       2: 从上到下打印文本
                       3: 从下到上打印文本
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.设置文本打印方向(2)  # 设置文本从上到下打印
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置文本打印方向: {msg}")
            return 0
        
        try:
            return self._dm.FoobarTextPrintDir(方向)
        except Exception as e:
            print(f"Error in 设置文本打印方向: {str(e)}")
            return 0

    def 设置文本区域(self, 横坐标: int, 纵坐标: int, 宽度: int, 高度: int) -> int:
        """
        函数简介:
            设置打印时的文本区域。
            此函数调用后，工具栏的文本将只显示在指定的区域内。
            如果文本内容超出了区域范围，将会自动换行或者隐藏。
            如果要取消文本区域的限制，可以把区域设置为工具栏的大小。
        
        函数原型:
            long FoobarTextRect(x,y,w,h)
        
        参数定义:
            横坐标 整形数: 左上角X坐标
            纵坐标 整形数: 左上角Y坐标
            宽度 整形数: 区域宽度
            高度 整形数: 区域高度
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.设置文本区域(10, 10, 100, 100)
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 设置文本区域: {msg}")
            return 0
        
        try:
            return self._dm.FoobarTextRect(横坐标, 纵坐标, 宽度, 高度)
        except Exception as e:
            print(f"Error in 设置文本区域: {str(e)}")
            return 0

    def 解锁(self) -> int:
        """
        函数简介:
            解锁指定的工具栏。
            解锁后可以继续加入图片和文字等。
            与锁定函数配对使用。
        
        函数原型:
            long FoobarUnlock()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.解锁()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 解锁: {msg}")
            return 0
        
        try:
            return self._dm.FoobarUnlock()
        except Exception as e:
            print(f"Error in 解锁: {str(e)}")
            return 0

    def 更新(self) -> int:
        """
        函数简介:
            更新工具栏,所有之前的文字和图片等都会显示出来。
            注意：调用Foobar系列函数进行绘制文字或图像后。
            要调用这个函数才能立即看到结果。
            此函数会强制刷新工具栏的显示内容。
            如果工具栏内容频繁变化，建议不要频繁调用此函数。
            可以等待所有内容都设置完毕后再调用一次。
        
        函数原型:
            long FoobarUpdate()
        
        参数定义:
            无参数
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.foobar.更新()
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 更新: {msg}")
            return 0
        
        try:
            return self._dm.FoobarUpdate()
        except Exception as e:
            print(f"Error in 更新: {str(e)}")
            return 0

    def CreateFoobarCustom(self, *args, **kwargs):
        """英文别名，调用创建自定义"""
        return self.创建自定义(*args, **kwargs)
    
    def CreateFoobarEllipse(self, *args, **kwargs):
        """英文别名，调用创建椭圆"""
        return self.创建椭圆(*args, **kwargs)
    
    def CreateFoobarRect(self, *args, **kwargs):
        """英文别名，调用创建矩形"""
        return self.创建矩形(*args, **kwargs)
    
    def CreateFoobarRoundRect(self, *args, **kwargs):
        """英文别名，调用创建圆角矩形"""
        return self.创建圆角矩形(*args, **kwargs)
    
    def FoobarClearText(self, *args, **kwargs):
        """英文别名，调用清除文本"""
        return self.清除文本(*args, **kwargs)
    
    def FoobarClose(self, *args, **kwargs):
        """英文别名，调用关闭"""
        return self.关闭(*args, **kwargs)
    
    def FoobarDrawLine(self, *args, **kwargs):
        """英文别名，调用画线"""
        return self.画线(*args, **kwargs)
    
    def FoobarDrawPic(self, *args, **kwargs):
        """英文别名，调用画图"""
        return self.画图(*args, **kwargs)
    
    def FoobarDrawText(self, *args, **kwargs):
        """英文别名，调用绘制文本"""
        return self.绘制文本(*args, **kwargs)
    
    def FoobarFillRect(self, *args, **kwargs):
        """英文别名，调用填充矩形"""
        return self.填充矩形(*args, **kwargs)
    
    def FoobarLock(self, *args, **kwargs):
        """英文别名，调用锁定"""
        return self.锁定(*args, **kwargs)
    
    def FoobarPrintText(self, *args, **kwargs):
        """英文别名，调用打印文本"""
        return self.打印文本(*args, **kwargs)
    
    def FoobarSetFont(self, *args, **kwargs):
        """英文别名，调用设置字体"""
        return self.设置字体(*args, **kwargs)
    
    def FoobarSetSave(self, *args, **kwargs):
        """英文别名，调用设置保存"""
        return self.设置保存(*args, **kwargs)
    
    def FoobarStartGif(self, *args, **kwargs):
        """英文别名，调用开始GIF"""
        return self.开始GIF(*args, **kwargs)
    
    def FoobarStopGif(self, *args, **kwargs):
        """英文别名，调用停止GIF"""
        return self.停止GIF(*args, **kwargs)
    
    def FoobarTextLineGap(self, *args, **kwargs):
        """英文别名，调用设置文本行间距"""
        return self.设置文本行间距(*args, **kwargs)
    
    def FoobarTextPrintDir(self, *args, **kwargs):
        """英文别名，调用设置文本打印方向"""
        return self.设置文本打印方向(*args, **kwargs)
    
    def FoobarTextRect(self, *args, **kwargs):
        """英文别名，调用设置文本区域"""
        return self.设置文本区域(*args, **kwargs)
    
    def FoobarUnlock(self, *args, **kwargs):
        """英文别名，调用解锁"""
        return self.解锁(*args, **kwargs)
    
    def FoobarUpdate(self, *args, **kwargs):
        """英文别名，调用更新"""
        return self.更新(*args, **kwargs) 