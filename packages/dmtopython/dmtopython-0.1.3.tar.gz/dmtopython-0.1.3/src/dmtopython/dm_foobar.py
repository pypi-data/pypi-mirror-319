import win32com.client

class DmFoobar:
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

    def CreateFoobarCustom(self, hwnd, x, y, pic_name, trans_color, sim):
        """
        函数简介:
            根据指定的位图创建一个自定义形状的窗口
        函数原型:
            long CreateFoobarCustom(hwnd,x,y,pic_name,trans_color,sim)
        参数定义:
            hwnd 整形数: 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            pic_name 字符串: 位图名字. 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制.
            trans_color 字符串: 透明色(RRGGBB)
            sim 双精度浮点数: 透明色的相似值 0.1-1.0
        返回值:
            整形数: 创建成功的窗口句柄
        注: foobar不能在本进程窗口内创建.
        """
        return self._dm.CreateFoobarCustom(hwnd, x, y, pic_name, trans_color, sim)

    def CreateFoobarEllipse(self, hwnd, x, y, w, h):
        """
        函数简介:
            创建一个椭圆窗口
        函数原型:
            long CreateFoobarEllipse(hwnd,x,y,w,h)
        参数定义:
            hwnd 整形数: 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            w 整形数: 矩形区域的宽度
            h 整形数: 矩形区域的高度
        返回值:
            整形数: 创建成功的窗口句柄
        注: foobar不能在本进程窗口内创建.
        """
        return self._dm.CreateFoobarEllipse(hwnd, x, y, w, h)

    def CreateFoobarRect(self, hwnd, x, y, w, h):
        """
        函数简介:
            创建一个矩形窗口
        函数原型:
            long CreateFoobarRect(hwnd,x,y,w,h)
        参数定义:
            hwnd 整形数: 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            w 整形数: 矩形区域的宽度
            h 整形数: 矩形区域的高度
        返回值:
            整形数: 创建成功的窗口句柄
        注: foobar不能在本进程窗口内创建.
        """
        return self._dm.CreateFoobarRect(hwnd, x, y, w, h)

    def CreateFoobarRoundRect(self, hwnd, x, y, w, h, rw, rh):
        """
        函数简介:
            创建一个圆角矩形窗口
        函数原型:
            long CreateFoobarRoundRect(hwnd,x,y,w,h,rw,rh)
        参数定义:
            hwnd 整形数: 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            w 整形数: 矩形区域的宽度
            h 整形数: 矩形区域的高度
            rw 整形数: 圆角的宽度
            rh 整形数: 圆角的高度
        返回值:
            整形数: 创建成功的窗口句柄
        注: foobar不能在本进程窗口内创建.
        """
        return self._dm.CreateFoobarRoundRect(hwnd, x, y, w, h, rw, rh)

    def FoobarClearText(self, hwnd):
        """
        函数简介:
            清除指定的Foobar滚动文本区
        函数原型:
            long FoobarClearText(hwnd)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarClearText(hwnd)

    def FoobarClose(self, hwnd):
        """
        函数简介:
            关闭一个Foobar,注意,必须调用此函数来关闭窗口,用SetWindowState也可以关闭,但会造成内存泄漏.
        函数原型:
            long FoobarClose(hwnd)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarClose(hwnd)

    def FoobarDrawLine(self, hwnd, x1, y1, x2, y2, color, style, width):
        """
        函数简介:
            在指定的Foobar窗口内部画线条.
        函数原型:
            long FoobarDrawLine(hwnd,x1,y1,x2,y2,color,style,width)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
            x1 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y1 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            x2 整形数: 右下角X坐标(相对于hwnd客户区坐标)
            y2 整形数: 右下角Y坐标(相对于hwnd客户区坐标)
            color 字符串: 填充的颜色值
            style 整形数: 画笔类型. 0为实线. 1为虚线
            width 整形数: 线条宽度.
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 当style为1时，线条宽度必须也是1.否则线条是实线.
        """
        return self._dm.FoobarDrawLine(hwnd, x1, y1, x2, y2, color, style, width)

    def FoobarDrawPic(self, hwnd, x, y, pic_name, trans_color):
        """
        函数简介:
            在指定的Foobar窗口绘制图像
        函数原型:
            long FoobarDrawPic(hwnd,x,y,pic_name,trans_color)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            pic_name 字符串: 图像文件名 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制.
            trans_color 字符串: 图像透明色
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarDrawPic(hwnd, x, y, pic_name, trans_color)

    def FoobarDrawText(self, hwnd, x, y, w, h, text, color, align):
        """
        函数简介:
            在指定的Foobar窗口绘制文字
        函数原型:
            long FoobarDrawText(hwnd,x,y,w,h,text,color,align)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            w 整形数: 矩形区域的宽度
            h 整形数: 矩形区域的高度
            text 字符串: 字符串
            color 字符串: 文字颜色值
            align 整形数: 取值定义如下
                1: 左对齐
                2: 中间对齐
                4: 右对齐
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarDrawText(hwnd, x, y, w, h, text, color, align)

    def FoobarFillRect(self, hwnd, x1, y1, x2, y2, color):
        """
        函数简介:
            在指定的Foobar窗口内部填充矩形
        函数原型:
            long FoobarFillRect(hwnd,x1,y1,x2,y2,color)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
            x1 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y1 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            x2 整形数: 右下角X坐标(相对于hwnd客户区坐标)
            y2 整形数: 右下角Y坐标(相对于hwnd客户区坐标)
            color 字符串: 填充的颜色值
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarFillRect(hwnd, x1, y1, x2, y2, color)

    def FoobarLock(self, hwnd):
        """
        函数简介:
            锁定指定的Foobar窗口,不能通过鼠标来移动
        函数原型:
            long FoobarLock(hwnd)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarLock(hwnd)

    def FoobarPrintText(self, hwnd, text, color):
        """
        函数简介:
            向指定的Foobar窗口区域内输出滚动文字
        函数原型:
            long FoobarPrintText(hwnd,text,color)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            text 字符串: 文本内容
            color 字符串: 文本颜色
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarPrintText(hwnd, text, color)

    def FoobarSetFont(self, hwnd, font_name, size, flag):
        """
        函数简介:
            设置指定Foobar窗口的字体
        函数原型:
            long FoobarSetFont(hwnd,font_name,size,flag)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            font_name 字符串: 系统字体名,注意,必须保证系统中有此字体
            size 整形数: 字体大小
            flag 整形数: 取值定义如下
                0: 正常字体
                1: 粗体
                2: 斜体
                4: 下划线
                文字可以是以上的组合 比如粗斜体就是1+2,斜体带下划线就是:2+4等.
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarSetFont(hwnd, font_name, size, flag)

    def FoobarSetSave(self, hwnd, file, enable, header):
        """
        函数简介:
            设置保存指定的Foobar滚动文本区信息到文件.
        函数原型:
            long FoobarSetSave(hwnd,file,enable,header)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            file 字符串: 保存的文件名
            enable 整形数: 取值如下
                0: 关闭向文件输出 (默认是0)
                1: 开启向文件输出
            header 字符串: 输出的附加头信息. (比如行数 日期 时间信息) 格式是如下格式串的顺序组合.如果为空串，表示无附加头.
                "%L0nd%" 表示附加头信息带有行号，并且是按照十进制输出. n表示按多少个十进制数字补0对齐.
                "%L0nx%" 表示附加头信息带有行号，并且是按照16进制小写输出.
                "%L0nX%" 表示附加头信息带有行号，并且是按照16进制大写输出.
                "%yyyy%" 表示年
                "%MM%" 表示月
                "%dd%" 表示日
                "%hh%" 表示小时
                "%mm%" 表示分钟
                "%ss%" 表示秒
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarSetSave(hwnd, file, enable, header)

    def FoobarSetTrans(self, hwnd, is_trans, color, sim):
        """
        函数简介:
            设置指定Foobar窗口的是否透明
        函数原型:
            long FoobarSetTrans(hwnd,is_trans,color,sim)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            is_trans 整形数: 是否透明. 0为不透明(此时,color和sim无效)，1为透明.
            color 字符串: 透明色(RRGGBB)
            sim 双精度浮点数: 透明色的相似值 0.1-1.0
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 调用此接口，最好打开windows的dwm. 否则可能会卡.
        """
        return self._dm.FoobarSetTrans(hwnd, is_trans, color, sim)

    def FoobarStartGif(self, hwnd, x, y, pic_name, repeat_limit, delay):
        """
        函数简介:
            在指定的Foobar窗口绘制gif动画.
        函数原型:
            long FoobarStartGif(hwnd,x,y,pic_name,repeat_limit,delay)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            pic_name 字符串: 图像文件名 如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制.
            repeat_limit 整形数: 表示重复GIF动画的次数，如果是0表示一直循环显示.大于0，则表示循环指定的次数以后就停止显示.
            delay 整形数: 表示每帧GIF动画之间的时间间隔.如果是0，表示使用GIF内置的时间，如果大于0，表示使用自定义的时间间隔.
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 当foobar关闭时，所有播放的gif也会自动关闭，内部资源也会自动释放，没必要一定去调用FoobarStopGif函数.
        另外，所有gif动画是在顶层显示，在默认绘图层和Print层之上. gif之间的显示顺序按照调用FoobarStartGif的顺序决定.
        """
        return self._dm.FoobarStartGif(hwnd, x, y, pic_name, repeat_limit, delay)

    def FoobarStopGif(self, hwnd, x, y, pic_name):
        """
        函数简介:
            停止在指定foobar里显示的gif动画.
        函数原型:
            long FoobarStopGif(hwnd,x,y,pic_name)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
            x 整形数: 左上角X坐标(相对于hwnd客户区坐标)
            y 整形数: 左上角Y坐标(相对于hwnd客户区坐标)
            pic_name 字符串: 图像文件名
        返回值:
            整形数:
            0: 失败
            1: 成功
        注: 当foobar关闭时，所有播放的gif也会自动关闭，内部资源也会自动释放，没必要一定去调用FoobarStopGif函数.
        另外，对于在不同的坐标显示的gif动画，插件内部会认为是不同的GIF.所以停止GIF时，一定要和FoobarStartGif时指定的x,y坐标一致.
        """
        return self._dm.FoobarStopGif(hwnd, x, y, pic_name)

    def FoobarTextLineGap(self, hwnd, line_gap):
        """
        函数简介:
            设置滚动文本区的文字行间距,默认是3
        函数原型:
            long FoobarTextLineGap(hwnd,line_gap)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            line_gap 整形数: 文本行间距
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarTextLineGap(hwnd, line_gap)

    def FoobarTextPrintDir(self, hwnd, dir):
        """
        函数简介:
            设置滚动文本区的文字输出方向,默认是0
        函数原型:
            long FoobarTextPrintDir(hwnd,dir)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            dir 整形数: 0 表示向下输出
                       1 表示向上输出
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarTextPrintDir(hwnd, dir)

    def FoobarTextRect(self, hwnd, x, y, w, h):
        """
        函数简介:
            设置指定Foobar窗口的滚动文本框范围,默认的文本框范围是窗口区域
        函数原型:
            long FoobarTextRect(hwnd,x,y,w,h)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
            x 整形数: x坐标
            y 整形数: y坐标
            w 整形数: 宽度
            h 整形数: 高度
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarTextRect(hwnd, x, y, w, h)

    def FoobarUnlock(self, hwnd):
        """
        函数简介:
            解锁指定的Foobar窗口,可以通过鼠标来移动
        函数原型:
            long FoobarUnlock(hwnd)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FoobarUnlock(hwnd)

    def FoobarUpdate(self, hwnd):
        """
        函数简介:
            刷新指定的Foobar窗口
        函数原型:
            long FoobarUpdate(hwnd)
        参数定义:
            hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的
        返回值:
            整形数:
            0: 失败
            1: 成功
        注意: 所有绘制完成以后,必须通过调用此函数来刷新窗口,否则窗口内容不会改变.
        """
        return self._dm.FoobarUpdate(hwnd)

    # 更新中文函数名部分
    创建自定义形状窗口 = CreateFoobarCustom
    创建椭圆窗口 = CreateFoobarEllipse
    创建矩形窗口 = CreateFoobarRect
    创建圆角矩形窗口 = CreateFoobarRoundRect
    清除文本 = FoobarClearText
    关闭窗口 = FoobarClose
    画线 = FoobarDrawLine
    绘制图片 = FoobarDrawPic
    绘制文字 = FoobarDrawText
    填充矩形 = FoobarFillRect
    锁定窗口 = FoobarLock
    打印文字 = FoobarPrintText
    设置字体 = FoobarSetFont
    设置保存 = FoobarSetSave
    设置透明 = FoobarSetTrans
    播放动画 = FoobarStartGif
    停止动画 = FoobarStopGif
    设置行间距 = FoobarTextLineGap
    设置文字方向 = FoobarTextPrintDir
    设置文本区域 = FoobarTextRect
    解锁窗口 = FoobarUnlock
    刷新窗口 = FoobarUpdate
    # ... 继续添加其他中文函数名 ... 