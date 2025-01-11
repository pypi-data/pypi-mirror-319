import win32com.client

class DmOcr:
    def __init__(self, dm):
        self._dm = dm

    def AddDict(self, index: int, dict_info: str) -> int:
        """
        函数简介:
            给指定的字库中添加一条字库信息
        函数原型:
            long AddDict(index,dict_info)
        参数定义:
            index 整形数: 字库的序号,取值为0-99,目前最多支持100个字库
            dict_info 字符串: 字库描述串，具体参考大漠综合工具中的字符定义
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            此函数尽量在小字库中使用，大字库中使用AddDict速度比较慢
            此函数是向指定的字库所在的内存中添加,而不是往文件中添加
            添加以后立刻就可以用于文字识别,无须再SetDict
            如果要保存添加进去的字库信息，需要调用SaveDict
        """
        return self._dm.AddDict(index, dict_info)

    def ClearDict(self, index: int) -> int:
        """
        函数简介:
            清空指定的字库
        函数原型:
            long ClearDict(index)
        参数定义:
            index 整形数: 字库的序号,取值为0-99,目前最多支持100个字库
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            此函数尽量在小字库中使用
            此函数支持清空内存中的字库，而不是字库文件本身
        """
        return self._dm.ClearDict(index)

    def EnableShareDict(self, enable: int) -> int:
        """
        函数简介:
            允许当前调用的对象使用全局字库
        函数原型:
            long EnableShareDict(enable)
        参数定义:
            enable 整形数: 0: 关闭 1: 打开
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            一旦当前对象开启了全局字库,那么所有的和文字识别，字库相关的接口都认为是对全局字库的操作
            如果所有对象都要需要全局字库,可以选一个主对象开启使用全局字库，并且设置好字库，其他对象只需要开启全局字库即可
            第一个开启全局字库并且设置字库的主对象不可以被释放
            此主对象在修改字库时,其它任何对象都不可以对全局字库进行操作
        """
        return self._dm.EnableShareDict(enable)

    def FetchWord(self, x1: int, y1: int, x2: int, y2: int, color: str, word: str) -> str:
        """
        函数简介:
            根据指定的范围,以及指定的颜色描述，提取点阵信息
        函数原型:
            string FetchWord(x1, y1, x2, y2, color, word)
        参数定义:
            x1 整形数: 左上角X坐标
            y1 整形数: 左上角Y坐标
            x2 整形数: 右下角X坐标
            y2 整形数: 右下角Y坐标
            color 字符串: 颜色格式串.注意，RGB和HSV,以及灰度格式都支持
            word 字符串: 待定义的文字,不能为空，且不能为关键符号"$"
        返回值:
            字符串: 识别到的点阵信息，可用于AddDict；如果失败，返回空
        """
        return self._dm.FetchWord(x1, y1, x2, y2, color, word)

    def FindStr(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> tuple[int, int, int]:
        """
        函数简介:
            在屏幕范围内查找字符串
        函数原型:
            long FindStr(x1,y1,x2,y2,string,color_format,sim,intX,intY)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合，比如"长安|洛阳|大雁塔"
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            tuple[int, int, int]: (index, x, y)
            index: 返回字符串的索引,没找到返回-1
            x: 返回X坐标,没找到返回-1
            y: 返回Y坐标,没找到返回-1
        注: 
            此函数的原理是先Ocr识别，然后再查找,所以速度比FindStrFast要慢
            一般字库字符数量小于100左右，模糊度为1.0时，用FindStr要快一些,否则用FindStrFast
        """
        x = self._dm.GetPointWindow(0)
        y = self._dm.GetPointWindow(1)
        ret = self._dm.FindStr(x1, y1, x2, y2, string, color_format, sim, x, y)
        return ret, x, y

    def FindStrE(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        函数简介:
            在屏幕范围内查找字符串,返回字符串格式
        函数原型:
            string FindStrE(x1,y1,x2,y2,string,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回字符串序号以及X和Y坐标,形式如"id|x|y"
            没找到时返回"-1|-1|-1"
        """
        return self._dm.FindStrE(x1, y1, x2, y2, string, color_format, sim)

    def SetDict(self, index: int, file: str) -> int:
        """
        函数简介:
            设置字库文件
        函数原型:
            long SetDict(index,file)
        参数定义:
            index 整形数: 字库的序号,取值为0-99,目前最多支持100个字库
            file 字符串: 字库文件名
        返回值:
            整形数: 0: 失败 1: 成功
        注: 此函数速度很慢，全局初始化时调用一次即可，切换字库用UseDict
        """
        return self._dm.SetDict(index, file)

    def SetDictMem(self, index: int, addr: int, size: int) -> int:
        """
        函数简介:
            从内存中设置字库
        函数原型:
            long SetDictMem(index,addr,size)
        参数定义:
            index 整形数: 字库的序号,取值为0-99,目前最多支持100个字库
            addr 整形数: 数据地址
            size 整形数: 字库长度
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            此函数速度很慢，全局初始化时调用一次即可，切换字库用UseDict
            此函数不支持加密的内存字库
        """
        return self._dm.SetDictMem(index, addr, size)

    def SetDictPwd(self, pwd: str) -> int:
        """
        函数简介:
            设置字库的密码
        函数原型:
            long SetDictPwd(pwd)
        参数定义:
            pwd 字符串: 字库密码
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            如果使用了多字库,所有字库的密码必须一样
            此函数必须在SetDict之前调用,否则会解密失败
        """
        return self._dm.SetDictPwd(pwd)

    def SetExactOcr(self, exact_ocr: int) -> int:
        """
        函数简介:
            设定是否开启精准识别
        函数原型:
            long SetExactOcr(exact_ocr)
        参数定义:
            exact_ocr 整形数: 0: 关闭精准识别 1: 开启精准识别
        返回值:
            整形数: 0: 失败 1: 成功
        注: 精准识别开启后，行间距和列间距会对识别结果造成较大影响
        """
        return self._dm.SetExactOcr(exact_ocr)

    def SetMinColGap(self, min_col_gap: int) -> int:
        """
        函数简介:
            设定列间距
        函数原型:
            long SetMinColGap(min_col_gap)
        参数定义:
            min_col_gap 整形数: 最小列间距
        返回值:
            整形数: 0: 失败 1: 成功
        注: 此设置如果不为0,那么将不能识别连体字,慎用
        """
        return self._dm.SetMinColGap(min_col_gap)

    def SetMinRowGap(self, min_row_gap: int) -> int:
        """
        函数简介:
            设定行间距
        函数原型:
            long SetMinRowGap(min_row_gap)
        参数定义:
            min_row_gap 整形数: 最小行间距
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetMinRowGap(min_row_gap)

    def SetRowGapNoDict(self, row_gap: int) -> int:
        """
        函数简介:
            设定文字的行距(不使用字库)
        函数原型:
            long SetRowGapNoDict(row_gap)
        参数定义:
            row_gap 整形数: 文字行距
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetRowGapNoDict(row_gap)

    def SetWordGap(self, word_gap: int) -> int:
        """
        函数简介:
            设定词组间的间隔
        函数原型:
            long SetWordGap(word_gap)
        参数定义:
            word_gap 整形数: 单词间距
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetWordGap(word_gap)

    def SetWordGapNoDict(self, word_gap: int) -> int:
        """
        函数简介:
            设定词组间的间隔(不使用字库)
        函数原型:
            long SetWordGapNoDict(word_gap)
        参数定义:
            word_gap 整形数: 单词间距
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetWordGapNoDict(word_gap)

    def SetWordLineHeight(self, line_height: int) -> int:
        """
        函数简介:
            设定文字的平均行高
        函数原型:
            long SetWordLineHeight(line_height)
        参数定义:
            line_height 整形数: 行高
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetWordLineHeight(line_height)

    def SetWordLineHeightNoDict(self, line_height: int) -> int:
        """
        函数简介:
            设定文字的平均行高(不使用字库)
        函数原型:
            long SetWordLineHeightNoDict(line_height)
        参数定义:
            line_height 整形数: 行高
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetWordLineHeightNoDict(line_height)

    def UseDict(self, index: int) -> int:
        """
        函数简介:
            使用指定的字库文件进行识别
        函数原型:
            long UseDict(index)
        参数定义:
            index 整形数: 字库编号(0-99)
        返回值:
            整形数: 0: 失败 1: 成功
        注: 设置之后永久生效，除非再次设定
        """
        return self._dm.UseDict(index)

    def FindStrEx(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        函数简介:
            在屏幕范围内查找字符串,返回所有位置
        函数原型:
            string FindStrEx(x1,y1,x2,y2,string,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回所有找到的坐标,格式如"id,x,y|id,x,y..|id,x,y"
        """
        return self._dm.FindStrEx(x1, y1, x2, y2, string, color_format, sim)

    def FindStrFast(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> tuple[int, int, int]:
        """
        函数简介:
            快速查找字符串
        函数原型:
            long FindStrFast(x1,y1,x2,y2,string,color_format,sim,intX,intY)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            tuple[int, int, int]: (index, x, y)
            index: 返回字符串的索引,没找到返回-1
            x: 返回X坐标,没找到返回-1
            y: 返回Y坐标,没找到返回-1
        """
        x = self._dm.GetPointWindow(0)
        y = self._dm.GetPointWindow(1)
        ret = self._dm.FindStrFast(x1, y1, x2, y2, string, color_format, sim, x, y)
        return ret, x, y

    def FindStrFastE(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        函数简介:
            快速查找字符串,返回字符串格式
        函数原型:
            string FindStrFastE(x1,y1,x2,y2,string,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回字符串序号以及X和Y坐标,形式如"id|x|y"
            没找到时返回"-1|-1|-1"
        """
        return self._dm.FindStrFastE(x1, y1, x2, y2, string, color_format, sim)

    def FindStrFastEx(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        函数简介:
            快速查找字符串,返回所有位置
        函数原型:
            string FindStrFastEx(x1,y1,x2,y2,string,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回所有找到的坐标,格式如"id,x,y|id,x,y..|id,x,y"
        """
        return self._dm.FindStrFastEx(x1, y1, x2, y2, string, color_format, sim)

    def FindStrS(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> tuple[int, int]:
        """
        函数简介:
            查找字符串,返回坐标
        函数原型:
            long FindStrS(x1,y1,x2,y2,string,color_format,sim,intX,intY)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            string 字符串: 待查找的字符串,可以是字符串组合
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            tuple[int, int]: (x, y)
            x: 返回X坐标,没找到返回-1
            y: 返回Y坐标,没找到返回-1
        """
        x = self._dm.GetPointWindow(0)
        y = self._dm.GetPointWindow(1)
        ret = self._dm.FindStrS(x1, y1, x2, y2, string, color_format, sim, x, y)
        if ret == 0:
            return -1, -1
        return x, y

    def Ocr(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> str:
        """
        函数简介:
            识别屏幕范围内的字符串
        函数原型:
            string Ocr(x1,y1,x2,y2,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回识别到的字符串
        """
        return self._dm.Ocr(x1, y1, x2, y2, color_format, sim)

    def OcrEx(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> str:
        """
        函数简介:
            识别屏幕范围内的字符串,返回识别到的字符串及坐标
        函数原型:
            string OcrEx(x1,y1,x2,y2,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回识别到的字符串及坐标,格式如"字符串1,x1,y1|字符串2,x2,y2|..."
        """
        return self._dm.OcrEx(x1, y1, x2, y2, color_format, sim)

    def SaveDict(self, index: int, file: str) -> int:
        """
        函数简介:
            保存字库到文件
        函数原型:
            long SaveDict(index,file)
        参数定义:
            index 整形数: 字库的序号(0-99)
            file 字符串: 字库文件名
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SaveDict(index, file)

    def OcrInFile(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, color_format: str, sim: float) -> str:
        """
        函数简介:
            从文件中识别文字
        函数原型:
            string OcrInFile(x1,y1,x2,y2,pic_name,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            pic_name 字符串: 图片文件名
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            字符串: 返回识别到的字符串
        """
        return self._dm.OcrInFile(x1, y1, x2, y2, pic_name, color_format, sim)

    def SetColGapNoDict(self, col_gap: int) -> int:
        """
        函数简介:
            设定列间距(不使用字库)
        函数原型:
            long SetColGapNoDict(col_gap)
        参数定义:
            col_gap 整形数: 列间距
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetColGapNoDict(col_gap)

    def SetDictPwdNoDict(self, pwd: str) -> int:
        """
        函数简介:
            设置字库密码(不使用字库)
        函数原型:
            long SetDictPwdNoDict(pwd)
        参数定义:
            pwd 字符串: 字库密码
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetDictPwdNoDict(pwd)

    def GetDict(self) -> str:
        """
        函数简介:
            获取字库信息
        函数原型:
            string GetDict(index)
        参数定义:
            无
        返回值:
            字符串: 字库信息
        """
        return self._dm.GetDict()

    def GetDictCount(self) -> int:
        """
        函数简介:
            获取字库数量
        函数原型:
            long GetDictCount()
        参数定义:
            无
        返回值:
            整形数: 字库数量
        """
        return self._dm.GetDictCount()

    def GetDictInfo(self, index: int) -> str:
        """
        函数简介:
            获取字库详细信息
        函数原型:
            string GetDictInfo(index)
        参数定义:
            index 整形数: 字库序号(0-99)
        返回值:
            字符串: 字库详细信息
        """
        return self._dm.GetDictInfo(index)

    def GetNowDict(self) -> int:
        """
        函数简介:
            获取当前使用的字库序号
        函数原型:
            long GetNowDict()
        参数定义:
            无
        返回值:
            整形数: 当前使用的字库序号
        """
        return self._dm.GetNowDict()

    def GetWordResultCount(self) -> int:
        """
        函数简介:
            获取识别到的字符数量
        函数原型:
            long GetWordResultCount()
        参数定义:
            无
        返回值:
            整形数: 识别到的字符数量
        """
        return self._dm.GetWordResultCount()

    def GetWordResultPos(self, index: int) -> tuple[int, int, int, int]:
        """
        函数简介:
            获取识别到的字符坐标
        函数原型:
            long GetWordResultPos(index,x1,y1,x2,y2)
        参数定义:
            index 整形数: 字符序号
        返回值:
            tuple[int, int, int, int]: (x1, y1, x2, y2) 字符的左上角和右下角坐标
        """
        x1 = self._dm.GetPointWindow(0)
        y1 = self._dm.GetPointWindow(1)
        x2 = self._dm.GetPointWindow(2)
        y2 = self._dm.GetPointWindow(3)
        ret = self._dm.GetWordResultPos(index, x1, y1, x2, y2)
        if ret == 0:
            return -1, -1, -1, -1
        return x1, y1, x2, y2

    def GetWords(self, index: int, color_format: str) -> str:
        """
        函数简介:
            获取指定字库中的字符
        函数原型:
            string GetWords(index,color_format)
        参数定义:
            index 整形数: 字库序号(0-99)
            color_format 字符串: 颜色格式串
        返回值:
            字符串: 字库中的字符
        """
        return self._dm.GetWords(index, color_format)

    def GetWordsNoDict(self, x1: int, y1: int, x2: int, y2: int, color_format: str) -> str:
        """
        函数简介:
            不使用字库时，获取识别到的字符
        函数原型:
            string GetWordsNoDict(x1,y1,x2,y2,color_format)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            color_format 字符串: 颜色格式串
        返回值:
            字符串: 识别到的字符
        """
        return self._dm.GetWordsNoDict(x1, y1, x2, y2, color_format)

    def OcrExOne(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> tuple[str, int, int]:
        """
        函数简介:
            识别屏幕范围内的字符串(返回第一个)
        函数原型:
            string OcrExOne(x1,y1,x2,y2,color_format,sim)
        参数定义:
            x1 整形数: 区域的左上X坐标
            y1 整形数: 区域的左上Y坐标
            x2 整形数: 区域的右下X坐标
            y2 整形数: 区域的右下Y坐标
            color_format 字符串: 颜色格式串
            sim 双精度浮点数: 相似度,取值范围0.1-1.0
        返回值:
            tuple[str, int, int]: (str, x, y) 识别到的字符串及其坐标
        """
        result = self._dm.OcrExOne(x1, y1, x2, y2, color_format, sim)
        if not result:
            return "", -1, -1
        parts = result.split(",")
        if len(parts) != 3:
            return "", -1, -1
        return parts[0], int(parts[1]), int(parts[2])

    def SetOcrEngine(self, engine: int) -> int:
        """
        函数简介:
            设置OCR引擎
        函数原型:
            long SetOcrEngine(engine)
        参数定义:
            engine 整形数: 引擎类型
            0: 默认引擎
            1: 精准引擎
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetOcrEngine(engine)

    def SetOcrMatchMode(self, mode: int) -> int:
        """
        函数简介:
            设置OCR匹配模式
        函数原型:
            long SetOcrMatchMode(mode)
        参数定义:
            mode 整形数: 匹配模式
            0: 精准匹配
            1: 模糊匹配
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetOcrMatchMode(mode)

    def SetOcrOutputLen(self, len: int) -> int:
        """
        函数简介:
            设置OCR输出长度
        函数原型:
            long SetOcrOutputLen(len)
        参数定义:
            len 整形数: 输出长度
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetOcrOutputLen(len)

    def SetOcrTimeout(self, timeout: int) -> int:
        """
        函数简介:
            设置OCR超时时间
        函数原型:
            long SetOcrTimeout(timeout)
        参数定义:
            timeout 整形数: 超时时间(毫秒)
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetOcrTimeout(timeout)

    def UseOcrEngine(self, engine: int) -> int:
        """
        函数简介:
            使用OCR引擎
        函数原型:
            long UseOcrEngine(engine)
        参数定义:
            engine 整形数: 引擎类型
            0: 默认引擎
            1: 精准引擎
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.UseOcrEngine(engine)

    def UseOcrMatchMode(self, mode: int) -> int:
        """
        函数简介:
            使用OCR匹配模式
        函数原型:
            long UseOcrMatchMode(mode)
        参数定义:
            mode 整形数: 匹配模式
            0: 精准匹配
            1: 模糊匹配
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.UseOcrMatchMode(mode)

    def UseOcrOutputLen(self, len: int) -> int:
        """
        函数简介:
            使用OCR输出长度
        函数原型:
            long UseOcrOutputLen(len)
        参数定义:
            len 整形数: 输出长度
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.UseOcrOutputLen(len)

    # 中文别名
    添加字库 = AddDict
    清空字库 = ClearDict
    开启全局字库 = EnableShareDict
    提取文字 = FetchWord
    查找文字 = FindStr
    查找文字Ex = FindStrE
    查找文字Ex = FindStrEx
    快速查找文字 = FindStrFast
    快速查找文字E = FindStrFastE
    快速查找文字Ex = FindStrFastEx
    查找文字S = FindStrS
    获取字库 = GetDict
    获取字库数量 = GetDictCount
    获取字库信息 = GetDictInfo
    获取当前字库 = GetNowDict
    获取识别结果数量 = GetWordResultCount
    获取识别结果位置 = GetWordResultPos
    获取字库字符 = GetWords
    获取无字库字符 = GetWordsNoDict
    文字识别 = Ocr
    文字识别Ex = OcrEx
    文字识别单个 = OcrExOne
    文件识别 = OcrInFile
    保存字库 = SaveDict
    设置无字库列间距 = SetColGapNoDict
    设置字库 = SetDict
    设置内存字库 = SetDictMem
    设置字库密码 = SetDictPwd
    设置无字库密码 = SetDictPwdNoDict
    设置精准识别 = SetExactOcr
    设置最小列间距 = SetMinColGap
    设置最小行间距 = SetMinRowGap
    设置无字库行距 = SetRowGapNoDict
    设置词间距 = SetWordGap
    设置无字库词间距 = SetWordGapNoDict
    设置行高 = SetWordLineHeight
    设置无字库行高 = SetWordLineHeightNoDict
    使用字库 = UseDict
    设置OCR引擎 = SetOcrEngine
    设置OCR匹配模式 = SetOcrMatchMode
    设置OCR输出长度 = SetOcrOutputLen
    设置OCR超时 = SetOcrTimeout
    使用OCR引擎 = UseOcrEngine
    使用OCR匹配模式 = UseOcrMatchMode
    使用OCR输出长度 = UseOcrOutputLen