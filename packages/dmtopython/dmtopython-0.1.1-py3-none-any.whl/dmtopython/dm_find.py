import win32com.client

class DmFind:
    def __init__(self, dm=None, code=None, key=None):
        """初始化DmFind对象
        
        参数:
            dm: 已经初始化的大漠对象,如果为None则自动初始化
            code: 注册码
            key: 注册key
        """
        if dm is None:
            self._dm = win32com.client.Dispatch('dm.dmsoft')
            if code is not None and key is not None:
                self._dm.Reg(code, key)
        else:
            self._dm = dm

    def FindPic(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的图片
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标  
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 返回找到的图片序号(从0开始索引),没找到返回-1
        """
        return self._dm.FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicEx(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的所有图片
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有找到的坐标,格式如"id,x,y|id,x,y..|id,x,y"
        """
        return self._dm.FindPicEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicE(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的图片,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回找到的图片序号和坐标,格式如"index|x|y",比如"3|100|200"
        """
        return self._dm.FindPicE(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicS(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的图片,返回文件名
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回找到的图片的文件名,没找到返回空字符串
        """
        return self._dm.FindPicS(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicMem(self, x1, y1, x2, y2, pic_info, delta_color, sim, dir):
        """查找内存中的图片
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_info: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 返回找到的图片序号(从0开始索引),没找到返回-1
        """
        return self._dm.FindPicMem(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindPicMemEx(self, x1, y1, x2, y2, pic_info, delta_color, sim, dir):
        """查找内存中的所有图片
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_info: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有找到的坐标,格式如"id,x,y|id,x,y..|id,x,y"
        """
        return self._dm.FindPicMemEx(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindPicMemE(self, x1, y1, x2, y2, pic_info, delta_color, sim, dir):
        """查找内存中的图片,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_info: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回找到的图片序号和坐标,格式如"index|x|y",比如"3|100|200"
        """
        return self._dm.FindPicMemE(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def SetFindPicMultithreadLimit(self, limit):
        """设置多线程查找图片的线程数量
        
        参数:
            limit: 线程数量
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.SetFindPicMultithreadLimit(limit)

    def SetPicPwd(self, pwd):
        """设置图片密码
        
        参数:
            pwd: 图片密码
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.SetPicPwd(pwd)

    def FindColor(self, x1, y1, x2, y2, color, sim, dir):
        """查找指定区域内的颜色
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 0表示没找到,1表示找到
        """
        return self._dm.FindColor(x1, y1, x2, y2, color, sim, dir)

    def FindColorEx(self, x1, y1, x2, y2, color, sim, dir):
        """查找指定区域内的所有颜色
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有颜色信息的坐标值,格式为"x1,y1|x2,y2|..."
        """
        return self._dm.FindColorEx(x1, y1, x2, y2, color, sim, dir)

    def FindColorBlock(self, x1, y1, x2, y2, color, sim, count, width, height):
        """查找指定区域内的颜色块
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            count: 在宽度为width,高度为height的颜色块中,符合color颜色的最小数量
            width: 颜色块的宽度
            height: 颜色块的高度
            
        返回值:
            整数: 0表示没找到,1表示找到
        """
        return self._dm.FindColorBlock(x1, y1, x2, y2, color, sim, count, width, height)

    def FindMulColor(self, x1, y1, x2, y2, color, sim):
        """查找指定区域内的所有颜色
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            
        返回值:
            整数: 0表示没找到或部分颜色没找到,1表示所有颜色都找到
        """
        return self._dm.FindMulColor(x1, y1, x2, y2, color, sim)

    def FindMultiColor(self, x1, y1, x2, y2, first_color, offset_color, sim, dir):
        """根据指定的多点查找颜色坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            first_color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
            offset_color: 偏移颜色,格式为"x1|y1|RRGGBB-DRDGDB,x2|y2|RRGGBB-DRDGDB"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 0表示没找到,1表示找到
        """
        return self._dm.FindMultiColor(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def FindMultiColorEx(self, x1, y1, x2, y2, first_color, offset_color, sim, dir):
        """根据指定的多点查找所有颜色坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            first_color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
            offset_color: 偏移颜色,格式为"x1|y1|RRGGBB-DRDGDB,x2|y2|RRGGBB-DRDGDB"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有颜色信息的坐标值,格式为"x1,y1|x2,y2|..."
        """
        return self._dm.FindMultiColorEx(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def CaptureGif(self, x1, y1, x2, y2, file_name, delay, time):
        """抓取指定区域的动画,保存为gif格式
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            file_name: 保存的文件名
            delay: 每帧间隔,单位毫秒,建议60
            time: 总共时长,单位毫秒
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.CaptureGif(x1, y1, x2, y2, file_name, delay, time)

    def CapturePre(self, file_name):
        """抓取上次操作的图色区域,保存为指定文件
        
        参数:
            file_name: 保存的文件名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.CapturePre(file_name)

    def CapturePng(self, x1, y1, x2, y2, file_name):
        """抓取指定区域的图像,保存为png格式
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            file_name: 保存的文件名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.CapturePng(x1, y1, x2, y2, file_name)

    def CaptureJpg(self, x1, y1, x2, y2, file_name):
        """抓取指定区域的图像,保存为jpg格式
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            file_name: 保存的文件名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.CaptureJpg(x1, y1, x2, y2, file_name)

    def CaptureBmp(self, x1, y1, x2, y2, file_name):
        """抓取指定区域的图像,保存为bmp格式
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            file_name: 保存的文件名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.CaptureBmp(x1, y1, x2, y2, file_name)

    def IsDisplayDead(self, x1, y1, x2, y2, t):
        """判断指定区域的图像是否有变化
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            t: 判断时间,单位毫秒
            
        返回值:
            整数: 0表示没有变化,1表示有变化
        """
        return self._dm.IsDisplayDead(x1, y1, x2, y2, t)

    def GetPicSize(self, pic_name):
        """获取指定图片的尺寸
        
        参数:
            pic_name: 图片文件名,比如"1.bmp"
            
        返回值:
            字符串: 返回图片尺寸,格式为"w,h",比如"30,20"
        """
        return self._dm.GetPicSize(pic_name)

    def LoadPic(self, pic_name):
        """预先加载指定的图片
        
        参数:
            pic_name: 图片文件名,可以是多个图片,比如"1.bmp|2.bmp|3.bmp",也可以使用通配符,比如"*.bmp"
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.LoadPic(pic_name)

    def FreePic(self, pic_name):
        """释放指定的图片
        
        参数:
            pic_name: 图片文件名,可以是多个图片,比如"1.bmp|2.bmp|3.bmp",也可以使用通配符,比如"*.bmp"
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.FreePic(pic_name)

    def AppendPicAddr(self, pic_info, addr, size):
        """对指定的数据地址和长度,组合成新的参数
        
        参数:
            pic_info: 老的地址描述串
            addr: 数据地址
            size: 数据长度
            
        返回值:
            字符串: 新的地址描述串
        """
        return self._dm.AppendPicAddr(pic_info, addr, size)

    def BGR2RGB(self, bgr_color):
        """把BGR(按键格式)的颜色格式转换为RGB
        
        参数:
            bgr_color: BGR格式的颜色字符串
            
        返回值:
            字符串: RGB格式的字符串
        """
        return self._dm.BGR2RGB(bgr_color)

    def FindPicSim(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的图片,使用相似度比较
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 最小百分比相似率(0-100)
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 返回找到的图片序号(从0开始索引),没找到返回-1
        """
        return self._dm.FindPicSim(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicSimEx(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的所有图片,使用相似度比较
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 最小百分比相似率(0-100)
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有找到的坐标,格式如"id,sim,x,y|id,sim,x,y..|id,sim,x,y"
        """
        return self._dm.FindPicSimEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicSimE(self, x1, y1, x2, y2, pic_name, delta_color, sim, dir):
        """查找指定区域内的图片,使用相似度比较,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_name: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 最小百分比相似率(0-100)
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回找到的图片序号和坐标,格式如"index|x|y",比如"3|100|200"
        """
        return self._dm.FindPicSimE(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicSimMem(self, x1, y1, x2, y2, pic_info, delta_color, sim, dir):
        """查找内存中的图片,使用相似度比较
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_info: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 最小百分比相似率(0-100)
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 返回找到的图片序号(从0开始索引),没找到返回-1
        """
        return self._dm.FindPicSimMem(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindPicSimMemEx(self, x1, y1, x2, y2, pic_info, delta_color, sim, dir):
        """查找内存中的所有图片,使用相似度比较
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_info: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 最小百分比相似率(0-100)
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有找到的坐标,格式如"id,sim,x,y|id,sim,x,y..|id,sim,x,y"
        """
        return self._dm.FindPicSimMemEx(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindPicSimMemE(self, x1, y1, x2, y2, pic_info, delta_color, sim, dir):
        """查找内存中的图片,使用相似度比较,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            pic_info: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            delta_color: 颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40
            sim: 最小百分比相似率(0-100)
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回找到的图片序号和坐标,格式如"index|x|y",比如"3|100|200"
        """
        return self._dm.FindPicSimMemE(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindShape(self, x1, y1, x2, y2, offset_color, sim, dir):
        """查找指定的形状
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            offset_color: 坐标偏移描述,格式为"x1|y1|e1,x2|y2|e2"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            整数: 0表示没找到,1表示找到
        """
        return self._dm.FindShape(x1, y1, x2, y2, offset_color, sim, dir)

    def FindShapeE(self, x1, y1, x2, y2, offset_color, sim, dir):
        """查找指定的形状,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            offset_color: 坐标偏移描述,格式为"x1|y1|e1,x2|y2|e2"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回坐标,格式如"x|y",比如"100|200"
        """
        return self._dm.FindShapeE(x1, y1, x2, y2, offset_color, sim, dir)

    def FindShapeEx(self, x1, y1, x2, y2, offset_color, sim, dir):
        """查找指定的所有形状
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            offset_color: 坐标偏移描述,格式为"x1|y1|e1,x2|y2|e2"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回所有形状的坐标,格式为"x1,y1|x2,y2|..."
        """
        return self._dm.FindShapeEx(x1, y1, x2, y2, offset_color, sim, dir)

    def GetAveHSV(self, x1, y1, x2, y2):
        """获取指定区域的HSV颜色平均值
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            
        返回值:
            字符串: 返回HSV颜色值,格式为"H.S.V",比如"0.0.255"
        """
        return self._dm.GetAveHSV(x1, y1, x2, y2)

    def GetAveRGB(self, x1, y1, x2, y2):
        """获取指定区域的RGB颜色平均值
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            
        返回值:
            字符串: 返回RGB颜色值,格式为"RRGGBB",比如"FFFFFF"
        """
        return self._dm.GetAveRGB(x1, y1, x2, y2)

    def GetColor(self, x, y):
        """获取指定坐标的RGB颜色
        
        参数:
            x: X坐标
            y: Y坐标
            
        返回值:
            字符串: 返回RGB颜色值,格式为"RRGGBB",比如"FFFFFF"
        """
        return self._dm.GetColor(x, y)

    def GetColorBGR(self, x, y):
        """获取指定坐标的BGR颜色
        
        参数:
            x: X坐标
            y: Y坐标
            
        返回值:
            字符串: 返回BGR颜色值,格式为"BBGGRR",比如"FFFFFF"
        """
        return self._dm.GetColorBGR(x, y)

    def GetColorHSV(self, x, y):
        """获取指定坐标的HSV颜色
        
        参数:
            x: X坐标
            y: Y坐标
            
        返回值:
            字符串: 返回HSV颜色值,格式为"H.S.V",比如"0.0.255"
        """
        return self._dm.GetColorHSV(x, y)

    def GetColorNum(self, x1, y1, x2, y2, color, sim):
        """获取指定区域内某个颜色的数量
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            
        返回值:
            整数: 返回颜色数量
        """
        return self._dm.GetColorNum(x1, y1, x2, y2, color, sim)

    def GetScreenData(self, x1, y1, x2, y2):
        """获取指定区域的二进制颜色数据
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            
        返回值:
            整数: 返回二进制颜色数据的地址
        """
        return self._dm.GetScreenData(x1, y1, x2, y2)

    def GetScreenDataBmp(self, x1, y1, x2, y2):
        """获取指定区域的图像,用24位位图的数据格式返回
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.GetScreenDataBmp(x1, y1, x2, y2)

    def ImageToBmp(self, pic_name, bmp_name):
        """转换图片格式为24位BMP格式
        
        参数:
            pic_name: 要转换的图片名
            bmp_name: 要保存的BMP图片名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.ImageToBmp(pic_name, bmp_name)

    def RGB2BGR(self, rgb_color):
        """把RGB的颜色格式转换为BGR(按键格式)
        
        参数:
            rgb_color: RGB格式的颜色字符串
            
        返回值:
            字符串: BGR格式的字符串
        """
        return self._dm.RGB2BGR(rgb_color)

    def SetExcludeRegion(self, mode, info):
        """设置图色排除区域
        
        参数:
            mode: 模式,0表示添加,1表示设置颜色,2表示清空
            info: 根据mode的取值来决定
                mode=0: 区域格式为"x1,y1,x2,y2|x3,y3,x4,y4|..."
                mode=1: 颜色格式为"RRGGBB"
                mode=2: 此参数无效
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.SetExcludeRegion(mode, info)

    def SetFindPicMultithreadCount(self, count):
        """设置多线程找图的线程数量
        
        参数:
            count: 线程数量,最小不能小于2
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.SetFindPicMultithreadCount(count)

    def Capture(self, x1, y1, x2, y2, file_name):
        """抓取指定区域的图像,保存为24位位图
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            file_name: 保存的文件名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.Capture(x1, y1, x2, y2, file_name)

    def CmpColor(self, x, y, color, sim):
        """比较指定坐标点的颜色
        
        参数:
            x: X坐标
            y: Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            
        返回值:
            整数: 0表示颜色匹配,1表示颜色不匹配
        """
        return self._dm.CmpColor(x, y, color, sim)

    def EnableDisplayDebug(self, enable_debug):
        """开启图色调试模式,此模式会稍许降低图色和文字识别的速度
        
        参数:
            enable_debug: 0表示关闭,1表示开启
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.EnableDisplayDebug(enable_debug)

    def EnableFindPicMultithread(self, enable):
        """开启多线程找图
        
        参数:
            enable: 0表示关闭,1表示开启
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.EnableFindPicMultithread(enable)

    def EnableGetColorByCapture(self, enable):
        """允许以截图方式获取颜色
        
        参数:
            enable: 0表示关闭,1表示开启
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.EnableGetColorByCapture(enable)

    def FindColorBlockEx(self, x1, y1, x2, y2, color, sim, count, width, height):
        """查找指定区域内的所有颜色块
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            count: 在宽度为width,高度为height的颜色块中,符合color颜色的最小数量
            width: 颜色块的宽度
            height: 颜色块的高度
            
        返回值:
            字符串: 返回所有颜色块信息的坐标值,格式为"x1,y1|x2,y2|..."
        """
        return self._dm.FindColorBlockEx(x1, y1, x2, y2, color, sim, count, width, height)

    def FindColorE(self, x1, y1, x2, y2, color, sim, dir):
        """查找指定区域内的颜色,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回坐标,格式为"x|y",比如"100|200"
        """
        return self._dm.FindColorE(x1, y1, x2, y2, color, sim, dir)

    def FindMultiColorE(self, x1, y1, x2, y2, first_color, offset_color, sim, dir):
        """根据指定的多点查找颜色坐标,返回坐标
        
        参数:
            x1: 区域的左上X坐标
            y1: 区域的左上Y坐标
            x2: 区域的右下X坐标
            y2: 区域的右下Y坐标
            first_color: 颜色格式为"RRGGBB-DRDGDB",比如"123456-000000"
            offset_color: 偏移颜色,格式为"x1|y1|RRGGBB-DRDGDB,x2|y2|RRGGBB-DRDGDB"
            sim: 相似度,取值范围0.1-1.0
            dir: 查找方向 0:从左到右,从上到下 1:从左到右,从下到上 2:从右到左,从上到下 3:从右到左,从下到上
            
        返回值:
            字符串: 返回坐标,格式为"x|y",比如"100|200"
        """
        return self._dm.FindMultiColorE(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def LoadPicByte(self, addr, size, pic_name):
        """从内存加载图片
        
        参数:
            addr: BMP图像首地址
            size: BMP图像大小
            pic_name: 文件名,指定这个地址对应的图片名
            
        返回值:
            整数: 0表示失败,1表示成功
        """
        return self._dm.LoadPicByte(addr, size, pic_name)

    def MatchPicName(self, pic_name):
        """根据通配符获取文件集合
        
        参数:
            pic_name: 文件名,可以使用通配符,比如"*.bmp"
            
        返回值:
            字符串: 返回的是通配符对应的文件集合,每个图片以|分割
        """
        return self._dm.MatchPicName(pic_name)

    # 中文别名
    找图 = FindPic
    找图Ex = FindPicEx
    找图E = FindPicE
    找图S = FindPicS
    找图内存 = FindPicMem
    找图内存Ex = FindPicMemEx
    找图内存E = FindPicMemE
    找图相似 = FindPicSim
    找图相似Ex = FindPicSimEx
    找图相似E = FindPicSimE
    找图相似内存 = FindPicSimMem
    找图相似内存Ex = FindPicSimMemEx
    找图相似内存E = FindPicSimMemE
    找形状 = FindShape
    找形状E = FindShapeE
    找形状Ex = FindShapeEx
    找色 = FindColor
    找色Ex = FindColorEx
    找色块 = FindColorBlock
    找多点色 = FindMultiColor
    找多点色Ex = FindMultiColorEx
    找多色 = FindMulColor
    获取HSV平均值 = GetAveHSV
    获取RGB平均值 = GetAveRGB
    获取颜色 = GetColor
    获取颜色BGR = GetColorBGR
    获取颜色HSV = GetColorHSV
    获取颜色数量 = GetColorNum
    获取屏幕数据 = GetScreenData
    获取屏幕数据位图 = GetScreenDataBmp
    捕获动画 = CaptureGif
    捕获上次操作区域 = CapturePre
    捕获PNG图片 = CapturePng
    捕获JPG图片 = CaptureJpg
    捕获BMP图片 = CaptureBmp
    判断图像是否有变化 = IsDisplayDead
    获取图片大小 = GetPicSize
    加载图片 = LoadPic
    释放图片 = FreePic
    添加图片地址 = AppendPicAddr
    图片转BMP = ImageToBmp
    BGR转RGB = BGR2RGB
    RGB转BGR = RGB2BGR
    设置排除区域 = SetExcludeRegion
    设置多线程找图数量 = SetFindPicMultithreadCount
    设置多线程找图线程数 = SetFindPicMultithreadLimit
    设置图片密码 = SetPicPwd
    抓图 = Capture
    比较颜色 = CmpColor
    开启调试模式 = EnableDisplayDebug
    开启多线程找图 = EnableFindPicMultithread
    开启截图获取颜色 = EnableGetColorByCapture
    找色块Ex = FindColorBlockEx
    找色E = FindColorE
    找多点色E = FindMultiColorE
    从内存加载图片 = LoadPicByte
    匹配图片名 = MatchPicName 