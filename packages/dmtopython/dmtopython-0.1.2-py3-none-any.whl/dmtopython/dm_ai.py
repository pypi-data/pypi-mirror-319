import win32com.client

class DmAi:
    def __init__(self, dm=None, code=None, key=None):
        if dm:
            self._dm = dm
        else:
            self._dm = win32com.client.Dispatch('dm.dmsoft')
            if code and key:
                self._dm.Reg(code, key)
        
        
    def AiYoloDetectObjects(self, x1, y1, x2, y2, prob, iou):
        """函数简介:
        需要先加载Ai模块. 在指定范围内检测对象.
        
        函数原型:
        string AiYoloDetectObjects(x1, y1, x2, y2,prob,iou)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        prob双精度浮点数: 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测
        iou 双精度浮点数: 用于对多个检测框进行合并. 越大越不容易合并(很多框重叠). 
                         越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间. 
        
        返回值:
        字符串:
        返回的是所有检测到的对象.格式是"类名,置信度,x,y,w,h|....". 如果没检测到任何对象,返回空字符串.
        
        示例:
        dm.AiYoloUseModel 0
        objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)
        if len(objects) > 0 then
            ss = split(objects,"|")
            index = 0
            count = UBound(ss) + 1
            Do While index < count
                TracePrint ss(index)
                sss = split(ss(index),",")
                class_info = int(sss(0))
                prob_info = Csng(sss(1))
                x = int(sss(2))
                y = int(sss(3))
                w = int(sss(4))
                h = int(sss(5))
                index = index+1
            Loop
        end if
        
        注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型. 
        如果多个线程里,UseModel的序号是相同的,那么如果同时执行此接口时,会排队执行.
        """
        return self._dm.AiYoloDetectObjects(x1, y1, x2, y2, prob, iou)
        
    # 中文别名
    Yolo对象检测 = AiYoloDetectObjects
    
    def AiYoloDetectObjectsToDataBmp(self, x1, y1, x2, y2, prob, iou, data, size, mode):
        """函数简介:
        需要先加载Ai模块. 在指定范围内检测对象,把结果输出到BMP图像数据.用于二次开发.
        
        函数原型:
        long AiYoloDetectObjectsToDataBmp(x1, y1, x2, y2,prob,iou,data,size,mode)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        prob双精度浮点数: 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测
        iou 双精度浮点数: 用于对多个检测框进行合并. 越大越不容易合并(很多框重叠). 
                         越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间. 
        data 变参指针:返回图片的数据指针
        size 变参指针:返回图片的数据长度
        mode 整形数: 0表示绘制的文字信息里包含置信度. 1表示不包含.
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型. 
        如果多个线程里,UseModel的序号是相同的,那么如果同时执行此接口时,会排队执行.
        """
        return self._dm.AiYoloDetectObjectsToDataBmp(x1, y1, x2, y2, prob, iou, data, size, mode)
        
    # 中文别名
    Yolo对象检测到BMP数据 = AiYoloDetectObjectsToDataBmp
    
    def AiYoloDetectObjectsToFile(self, x1, y1, x2, y2, prob, iou, file, mode):
        """函数简介:
        需要先加载Ai模块. 在指定范围内检测对象,把结果输出到指定的BMP文件.
        
        函数原型:
        long AiYoloDetectObjectsToFile(x1, y1, x2, y2,prob,iou,file,mode)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        prob双精度浮点数: 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测
        iou 双精度浮点数: 用于对多个检测框进行合并. 越大越不容易合并(很多框重叠). 
                         越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间. 
        file 字符串:图片名,比如"test.bmp"
        mode 整形数: 0表示绘制的文字信息里包含置信度. 1表示不包含.
        
        返回值:
        整形数:
        0 : 失败
        1 : 成功
        
        注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型. 
        如果多个线程里,UseModel的序号是相同的,那么如果同时执行此接口时,会排队执行.
        """
        return self._dm.AiYoloDetectObjectsToFile(x1, y1, x2, y2, prob, iou, file, mode)
        
    # 中文别名
    Yolo对象检测到BMP文件 = AiYoloDetectObjectsToFile
    
    def AiYoloFreeModel(self, index):
        """函数简介:
        需要先加载Ai模块. 卸载指定的模型
        
        函数原型:
        long AiYoloFreeModel(index)
        
        参数定义:
        index 整形数: 模型的序号. 最多支持20个. 从0开始
        
        返回值:
        整形数:
        1 表示成功
        0 失败
        
        注:模型内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.
        """
        return self._dm.AiYoloFreeModel(index)
        
    # 中文别名
    Yolo释放模型 = AiYoloFreeModel
    
    def AiYoloObjectsToString(self, objects):
        """函数简介:
        需要先加载Ai模块. 把通过AiYoloDetectObjects或者是AiYoloSortsObjects的结果,按照顺序把class信息连接输出.
        
        函数原型:
        string AiYoloObjectsToString(objects)
        
        参数定义:
        objects 字符串: AiYoloDetectObjects或者AiYoloSortsObjects的返回值.
        
        返回值:
        字符串:
        返回的是class信息连接后的信息.
        
        示例:
        dm.AiYoloUseModel 0
        objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)
        sorted_objects = dm.AiYoloSortsObjects(objects)
        TracePrint dm.AiYoloObjectsToString(sorted_objects)
        """
        return self._dm.AiYoloObjectsToString(objects)
        
    # 中文别名
    Yolo对象转字符串 = AiYoloObjectsToString
    
    def AiYoloSetModel(self, index, file, pwd):
        """函数简介:
        需要先加载Ai模块. 从文件加载指定的模型.
        
        函数原型:
        long AiYoloSetModel(index,file,pwd)
        
        参数定义:
        index 整形数: 模型的序号. 最多支持20个. 从0开始
        file字符串: 模型文件名. 比如"xxxx.onnx"或者"xxxx.dmx"
        pwd字符串: 模型的密码. 仅对dmx格式有效.
        
        返回值:
        整形数:
        1 表示成功
        0 失败
        
        示例:
        dm.AiYoloSetModel 0,"xxxx.onnx",""
        dm.AiYoloSetModel 1,"xxxx.dmx","123"
        
        注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型. 另外,
        加载onnx时得确保和这个onnx同名的class文件也在同目录下. 
        比如加载xxxx.onnx,那么必须得有个相应的xxxx.class.
        """
        return self._dm.AiYoloSetModel(index, file, pwd)
        
    # 中文别名
    Yolo设置模型 = AiYoloSetModel
    
    def AiYoloSetModelMemory(self, index, data, size, pwd):
        """函数简介:
        需要先加载Ai模块. 从内存加载指定的模型. 仅支持dmx格式的内存
        
        函数原型:
        long AiYoloSetModelMemory(index,data,size,pwd)
        
        参数定义:
        index 整形数: 模型的序号. 最多支持20个. 从0开始
        data 整形数: dmx模型的内存地址
        size 整形数: dmx模型的大小
        pwd字符串: dmx模型的密码
        
        返回值:
        整形数:
        1 表示成功
        0 失败
        
        示例:
        dm.AiYoloSetModelMemory 0,2343253,23432432,"123"
        
        注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.
        """
        return self._dm.AiYoloSetModelMemory(index, data, size, pwd)
        
    # 中文别名
    Yolo从内存设置模型 = AiYoloSetModelMemory
    
    def AiYoloSetVersion(self, ver):
        """函数简介:
        需要先加载Ai模块. 设置Yolo的版本
        
        函数原型:
        long AiYoloSetVersion(ver)
        
        参数定义:
        ver字符串: Yolo的版本信息. 需要在加载Ai模块后,第一时间调用. 目前可选的值只有"v5-7.0"
        
        返回值:
        整形数:
        1 表示成功
        0 失败
        
        示例:
        dm.AiYoloSetVersion "v5-7.0"
        """
        return self._dm.AiYoloSetVersion(ver)
        
    # 中文别名
    Yolo设置版本 = AiYoloSetVersion
    
    def AiYoloSortsObjects(self, objects, height=0):
        """函数简介:
        需要先加载Ai模块. 把通过AiYoloDetectObjects的结果进行排序. 排序按照从上到下,从左到右.
        
        函数原型:
        string AiYoloSortsObjects(objects,height)
        
        参数定义:
        objects 字符串: AiYoloDetectObjects的返回值
        height整形数: 行高信息. 排序时需要使用此行高. 用于确定两个检测框是否处于同一行. 
                     如果两个框的Y坐标相差绝对值小于此行高,认为是同一行.
        
        返回值:
        字符串:
        返回的是所有检测到的对象.格式是"类名,置信度,x,y,w,h|....". 如果没检测到任何对象,返回空字符串.
        
        示例:
        dm.AiYoloUseModel 0
        objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)
        sorted_objects = dm.AiYoloSortsObjects(objects)
        """
        return self._dm.AiYoloSortsObjects(objects, height)
        
    # 中文别名
    Yolo对象排序 = AiYoloSortsObjects
    
    def AiYoloUseModel(self, index):
        """函数简介:
        需要先加载Ai模块. 切换当前使用的模型序号.用于AiYoloDetectXX等系列接口.
        
        函数原型:
        long AiYoloUseModel(index)
        
        参数定义:
        index 整形数: 模型的序号. 最多支持20个. 从0开始
        
        返回值:
        整形数:
        1 表示成功
        0 失败
        
        示例:
        dm.AiYoloUseModel 0
        """
        return self._dm.AiYoloUseModel(index)
        
    # 中文别名
    Yolo使用模型 = AiYoloUseModel
    
    def LoadAi(self, file):
        """函数简介:
        加载Ai模块. Ai模块从后台下载. 模块加载仅支持所有的正式版本。具体可以看DmGuard里系统版本的说明.
        
        函数原型:
        long LoadAi(file)
        
        参数定义:
        file 字符串: ai模块的路径. 比如绝对路径c:\\ai.module或者相对路径ai.module等.
        
        返回值:
        整形数:
        1 表示成功
        -1 打开文件失败
        -2 内存初始化失败. 如果是正式版本,出现这个错误可以联系我解决.
        -3 参数错误
        -4 加载错误
        -5 Ai模块初始化失败
        -6 内存分配失败
        
        示例:
        dm.SetPath dm.GetBasePath()
        dm_ret = dm.LoadAi("ai.module")
        TracePrint dm_ret
        """
        return self._dm.LoadAi(file)
        
    # 中文别名
    加载AI = LoadAi
    
    def LoadAiMemory(self, data, size):
        """函数简介:
        从内存加载Ai模块. Ai模块从后台下载. 模块加载仅支持所有的正式版本。具体可以看DmGuard里系统版本的说明.
        
        函数原型:
        long LoadAiMemory(data,size)
        
        参数定义:
        data 整形数: ai模块在内存中的地址
        size 整形数: ai模块在内存中的大小
        
        返回值:
        整形数:
        1 表示成功
        -1 打开文件失败
        -2 内存初始化失败. 如果是正式版本,出现这个错误可以联系我解决.
        -3 参数错误
        -4 加载错误
        -5 Ai模块初始化失败
        -6 内存分配失败
        
        示例:
        // 先获取ai.module的内存地址
        dm_ret = dm.LoadAiMemory(234735,32948)
        TracePrint dm_ret
        """
        return self._dm.LoadAiMemory(data, size)
        
    # 中文别名
    从内存加载AI = LoadAiMemory
    
    def AiEnableFindPicWindow(self, enable):
        """函数简介:
        设置是否在调用AiFindPicXX系列接口时,是否弹出找图结果的窗口. 方便调试. 默认是关闭的.
        
        函数原型:
        long AiEnableFindPicWindow(enable)
        
        参数定义:
        enable 整形数: 0 关闭
        1 开启
        
        返回值:
        整形数:
        0: 失败
        1: 成功
        """
        return self._dm.AiEnableFindPicWindow(enable)
        
    # 中文别名
    AI启用找图窗口 = AiEnableFindPicWindow
    
    def AiFindPic(self, x1, y1, x2, y2, pic_name, sim, dir, intX=0, intY=0):
        """函数简介:
        查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
        这个函数可以查找多个图片,只返回第一个找到的X Y坐标.
        此接口使用Ai模块来实现,比传统的FindPic的效果更好. 不需要训练
        
        函数原型:
        long AiFindPic(x1, y1, x2, y2, pic_name,sim, dir,intX, intY)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        pic_name 字符串:图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        sim 双精度浮点数:相似度,取值范围0.1-1.0
        dir 整形数:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上
        intX 变参指针:返回图片左上角的X坐标
        intY 变参指针:返回图片左上角的Y坐标
        
        返回值:
        整形数:
        返回找到的图片的序号,从0开始索引.如果没找到返回-1
        
        示例:
        dm_ret = dm.AiFindPic(0,0,2000,2000,"1.bmp|2.bmp|3.bmp",0.9,0,intX,intY)
        If intX >= 0 and intY >= 0 Then
            MessageBox "找到"
        End If
        
        此接口需要ai.module 4.0及其之后的版本.
        """
        return self._dm.AiFindPic(x1, y1, x2, y2, pic_name, sim, dir, intX, intY)
        
    # 中文别名
    AI找图 = AiFindPic
    
    def AiFindPicEx(self, x1, y1, x2, y2, pic_name, sim, dir):
        """函数简介:
        查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
        这个函数可以查找多个图片,并且返回所有找到的图像的坐标.
        此接口使用Ai模块来实现,比传统的FindPicEx的效果更好.不需要训练
        
        函数原型:
        string AiFindPicEx(x1, y1, x2, y2, pic_name,sim, dir)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        pic_name 字符串:图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
        sim 双精度浮点数:相似度,取值范围0.1-1.0
        dir 整形数:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上
        
        返回值:
        字符串:
        返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y" (图片左上角的坐标)
        比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),第二个是序号为2的图片,坐标(30,40)
        (由于内存限制,返回的图片数量最多为1500个左右)
        
        示例:
        dm_ret = dm.AiFindPicEx(0,0,2000,2000,"test.bmp|test2.bmp|test3.bmp|test4.bmp|test5.bmp" ,1.0,0)
        If len(dm_ret) > 0 Then
            ss = split(dm_ret,"|")
            index = 0
            count = UBound(ss) + 1
            Do While index < count
                TracePrint ss(index)
                sss = split(ss(index),",")
                id = int(sss(0))
                x = int(sss(1))
                y = int(sss(2))
                dm.MoveTo x,y
                Delay 1000
                index = index+1
            Loop
        End If
        
        此接口需要ai.module 4.0及其之后的版本.
        """
        return self._dm.AiFindPicEx(x1, y1, x2, y2, pic_name, sim, dir)
        
    # 中文别名
    AI找图Ex = AiFindPicEx
    
    def AiFindPicMem(self, x1, y1, x2, y2, pic_info, sim, dir, intX=0, intY=0):
        """函数简介:
        查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
        这个函数可以查找多个图片,只返回第一个找到的X Y坐标. 这个函数要求图片是数据地址.
        此接口使用Ai模块来实现,比传统的FindPicMem的效果更好.不需要训练
        
        函数原型:
        long AiFindPicMem(x1, y1, x2, y2, pic_info,sim, dir,intX, intY)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        pic_info 字符串: 图片数据地址集合. 格式为"地址1,长度1|地址2,长度2.....|地址n,长度n". 可以用AppendPicAddr来组合.
        地址表示24位位图资源在内存中的首地址，用十进制的数值表示
        长度表示位图资源在内存中的长度，用十进制数值表示.
        sim 双精度浮点数:相似度,取值范围0.1-1.0
        dir 整形数:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上
        intX 变参指针:返回图片左上角的X坐标
        intY 变参指针:返回图片左上角的Y坐标
        
        返回值:
        整形数:
        返回找到的图片的序号,从0开始索引.如果没找到返回-1
        
        示例:
        pic_info = ""
        pic_info = dm.AppendPicAddr(pic_info,12034,643)
        pic_info = dm.AppendPicAddr(pic_info,328435,8935)
        pic_info = dm.AppendPicAddr(pic_info,809234,789)
        dm_ret = dm.AiFindPicMem(0,0,2000,2000, pic_info,0.9,0,intX,intY)
        If intX >= 0 and intY >= 0 Then
            MessageBox "找到"
        End If
        
        注 : 内存中的图片格式必须是24位色，并且不能加密.
        此接口需要ai.module 4.0及其之后的版本.
        """
        return self._dm.AiFindPicMem(x1, y1, x2, y2, pic_info, sim, dir, intX, intY)
        
    # 中文别名
    AI找图内存 = AiFindPicMem
    
    def AiFindPicMemEx(self, x1, y1, x2, y2, pic_info, sim, dir):
        """函数简介:
        查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.
        这个函数可以查找多个图片,并且返回所有找到的图像的坐标. 这个函数要求图片是数据地址.
        此接口使用Ai模块来实现,比传统的FindPicMemEx的效果更好.不需要训练
        
        函数原型:
        string AiFindPicMemEx(x1, y1, x2, y2, pic_info,sim, dir)
        
        参数定义:
        x1 整形数:区域的左上X坐标
        y1 整形数:区域的左上Y坐标
        x2 整形数:区域的右下X坐标
        y2 整形数:区域的右下Y坐标
        pic_info 字符串: 图片数据地址集合. 格式为"地址1,长度1|地址2,长度2.....|地址n,长度n". 可以用AppendPicAddr来组合.
        地址表示24位位图资源在内存中的首地址，用十进制的数值表示
        长度表示位图资源在内存中的长度，用十进制数值表示.
        sim 双精度浮点数:相似度,取值范围0.1-1.0
        dir 整形数:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上
        
        返回值:
        字符串:
        返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y" (图片左上角的坐标)
        比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),第二个是序号为2的图片,坐标(30,40)
        (由于内存限制,返回的图片数量最多为1500个左右)
        
        示例:
        pic_info = ""
        pic_info = dm.AppendPicAddr(pic_info,12034,643)
        pic_info = dm.AppendPicAddr(pic_info,328435,8935)
        pic_info = dm.AppendPicAddr(pic_info,809234,789)
        dm_ret = dm.AiFindPicMemEx(0,0,2000,2000, pic_info ,1.0,0)
        If len(dm_ret) > 0 Then
            ss = split(dm_ret,"|")
            index = 0
            count = UBound(ss) + 1
            Do While index < count
                TracePrint ss(index)
                sss = split(ss(index),",")
                id = int(sss(0))
                x = int(sss(1))
                y = int(sss(2))
                dm.MoveTo x,y
                Delay 1000
                index = index+1
            Loop
        End If
        
        注 : 内存中的图片格式必须是24位色，并且不能加密.
        此接口需要ai.module 4.0及其之后的版本.
        """
        return self._dm.AiFindPicMemEx(x1, y1, x2, y2, pic_info, sim, dir)
        
    # 中文别名
    AI找图内存Ex = AiFindPicMemEx 