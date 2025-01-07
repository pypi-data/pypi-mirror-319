#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件AI模块API封装
整个Ai接口是通过外挂模块来实现的.   ai.module通过后台下载.

在调用Ai接口之前,需要保证LoadAi或者LoadAiMemory接口成功.

另外,由于是内存加载,卸载模块会导致程序出异常,所以只提供了加载接口(LoadAi和LoadAiMemory),没有提供卸载接口. 所以要特别注意,千万不能在LoadAi或者LoadAiMemory后卸载对象. 这样会导致模块没卸载,从而内存泄漏. 除非是程序结束. 

关于Yolo部分,由于模型很占用内存空间,并且检测接口很占用内存和CPU,所以在多线程中AiYoloDetectXX系列接口不建议频繁调用,更不可以用此接口来代替找图等接口.

如果只是单线程调用,或者同一时间只有一个线程调用AiYoloDetectXX系列接口,那么没什么影响.

内部实现上,Yolo是使用了全局的静态模型. 所有的对象是共用模型. 所以在多线程的使用上要特别注意.

对于同一个序号的模型,在多线程上是排队执行的. 尤其是同一个脚本程序控制很多窗口时,那么多线程执行AiYoloDetect系列接口时,并且使用的序号是相同的,那么效率会大打折扣.

另外在脚本程序下,识别效率会不如Yolo综合工具里的效率. 因为32位程序的优化不如64位.

另外也不要问我为何没有GPU加速,因为cuda不支持32位程序.

具体的使用例子请查看我录制的视频.

 

注:
如果想提高检测效率，两个途径
1. 使用更小更快的预训练模型. 比如yolov5n
2. 运行的机器CPU核心数越多,效率越高. 因为检测函数内部是多线程执行的.

如果想提高检测精度,两个途径
1. 使用更大但是更慢的预训练模型. 比如yolov5x
2. 对于每个类尽可能多的提供训练图片. 尽可能多的提供各种复杂背景下的训练图片. 尽可能对每个类在各种复杂背景下都提供训练图片. 训练的轮次可以稍微多一些.

如果发现自己训练后的模型,会越训练越差,说明是你训练的过头了(过拟合),减少轮次,重新训练.


'''

from typing import Tuple, Optional

class DmAi:
    def __init__(self, dm=None):
        self._dm = dm
        self._ai_loaded = False

    def _check_dm(self):
        if not self._dm:
            print("未初始化 DM 对象")
            return False, "未初始化 DM 对象"
        return True, ""

    def _check_ai_loaded(self):
        if not self._ai_loaded:
            print("未加载AI模块，请先调用 加载AI模块 或 加载AI内存模块")
            return False, "未加载AI模块，请先调用 加载AI模块 或 加载AI内存模块"
        return True, ""

    def 启用_显示找图结果(self, 启用: int) -> int:
        """
        函数简介:
            设置是否在调用AI找图系列接口时,弹出找图结果的窗口。
            方便调试。
            默认是关闭的。
        
        函数原型:
            long AiEnableFindPicWindow(enable)
        
        参数定义:
            启用 整形数: 0: 关闭 1: 开启
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            ret = dm.ai.启用_显示找图结果(1)  # 开启找图结果显示
            if ret == 1:
                print("设置成功")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 启用_显示找图结果: {msg}")
            return 0
            
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in 启用_显示找图结果: {msg}")
            return 0
            
        try:
            return self._dm.AiEnableFindPicWindow(启用)
        except Exception as e:
            print(f"Error in 启用_显示找图结果: {str(e)}")
            return 0

    def AI找图(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 图片名: str, 相似度: float, 方向: int, 返回x: int, 返回y: int) -> int:
        """
        函数简介:
            查找指定区域内的图片。
            位图必须是24位色格式,支持透明色。
            当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理。
            这个函数可以查找多个图片,只返回第一个找到的X Y坐标。
            此接口使用Ai模块来实现,比传统的FindPic的效果更好。不需要训练。
        
        函数原型:
            long AiFindPic(x1,y1,x2,y2,pic_name,sim,dir,intX,intY)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            图片名 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 双精度浮点数: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向 
                       0: 从左到右,从上到下 
                       1: 从左到右,从下到上 
                       2: 从右到左,从上到下 
                       3: 从右到左,从下到上
            返回x 整形数: 返回图片左上角的X坐标
            返回y 整形数: 返回图片左上角的Y坐标
        
        返回值:
            整形数: 返回找到的图片的序号,从0开始索引.如果没找到返回-1
        
        示例:
            ret, x, y = dm.ai.AI找图(0, 0, 2000, 2000, "1.bmp|2.bmp|3.bmp", 0.9, 0, x, y)
            if ret >= 0:
                print(f"找到图片,序号:{ret} 坐标:({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in AI找图: {msg}")
            return -1
            
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in AI找图: {msg}")
            return -1
            
        try:
            return self._dm.AiFindPic(左上x, 左上y, 右下x, 右下y, 图片名, 相似度, 方向, 返回x, 返回y)
        except Exception as e:
            print(f"Error in AI找图: {str(e)}")
            return -1

    def AI找图Ex(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 图片名: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            查找指定区域内的图片。
            位图必须是24位色格式,支持透明色。
            当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理。
            这个函数可以查找多个图片,并且返回所有找到的图像的坐标。
            此接口使用Ai模块来实现,比传统的FindPicEx的效果更好。不需要训练。
        
        函数原型:
            string AiFindPicEx(x1,y1,x2,y2,pic_name,sim,dir)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            图片名 字符串: 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            相似度 双精度浮点数: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向 
                       0: 从左到右,从上到下 
                       1: 从左到右,从下到上 
                       2: 从右到左,从上到下 
                       3: 从右到左,从下到上
        
        返回值:
            字符串: 返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y" (图片左上角的坐标)
                   比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),
                   第二个是序号为2的图片,坐标(30,40)
                   (由于内存限制,返回的图片数量最多为1500个左右)
        
        示例:
            ret = dm.ai.AI找图Ex(0, 0, 2000, 2000, "1.bmp|2.bmp|3.bmp", 0.9, 0)
            if ret:
                for item in ret.split("|"):
                    id, x, y = item.split(",")
                    print(f"找到第{id}号图片,坐标是:({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in AI找图Ex: {msg}")
            return ""
            
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in AI找图Ex: {msg}")
            return ""
            
        try:
            return self._dm.AiFindPicEx(左上x, 左上y, 右下x, 右下y, 图片名, 相似度, 方向)
        except Exception as e:
            print(f"Error in AI找图Ex: {str(e)}")
            return ""

    def AI找图内存版(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 图片信息: str, 相似度: float, 方向: int, 返回x: int, 返回y: int) -> int:
        """
        函数简介:
            查找指定区域内的图片。
            位图必须是24位色格式,支持透明色。
            当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理。
            这个函数可以查找多个图片,只返回第一个找到的X Y坐标。
            这个函数要求图片是数据地址。
            此接口使用Ai模块来实现,比传统的FindPicMem的效果更好。不需要训练。
        
        函数原型:
            long AiFindPicMem(x1,y1,x2,y2,pic_info,sim,dir,intX,intY)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            图片信息 字符串: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            相似度 双精度浮点数: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向 
                       0: 从左到右,从上到下 
                       1: 从左到右,从下到上 
                       2: 从右到左,从上到下 
                       3: 从右到左,从下到上
            返回x 整形数: 返回图片左上角的X坐标
            返回y 整形数: 返回图片左上角的Y坐标
        
        返回值:
            整形数: 返回找到的图片的序号,从0开始索引.如果没找到返回-1
        
        示例:
            # 组合图片地址信息
            pic_info = dm.AppendPicAddr("", 12034, 643)
            pic_info = dm.AppendPicAddr(pic_info, 328435, 8935)
            
            # 查找图片
            ret, x, y = dm.ai.AI找图内存版(0, 0, 2000, 2000, pic_info, 0.9, 0, x, y)
            if ret >= 0:
                print(f"找到图片,序号:{ret} 坐标:({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in AI找图内存版: {msg}")
            return -1
            
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in AI找图内存版: {msg}")
            return -1
            
        try:
            return self._dm.AiFindPicMem(左上x, 左上y, 右下x, 右下y, 图片信息, 相似度, 方向, 返回x, 返回y)
        except Exception as e:
            print(f"Error in AI找图内存版: {str(e)}")
            return -1

    def AI找图Ex内存版(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 图片信息: str, 相似度: float, 方向: int) -> str:
        """
        函数简介:
            查找指定区域内的图片。
            位图必须是24位色格式,支持透明色。
            当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理。
            这个函数可以查找多个图片,并且返回所有找到的图像的坐标。
            这个函数要求图片是数据地址。
            此接口使用Ai模块来实现,比传统的FindPicMemEx的效果更好。不需要训练。
        
        函数原型:
            string AiFindPicMemEx(x1,y1,x2,y2,pic_info,sim,dir)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            图片信息 字符串: 图片数据地址集合,格式为"地址1,长度1|地址2,长度2.....|地址n,长度n"
            相似度 双精度浮点数: 相似度,取值范围0.1-1.0
            方向 整形数: 查找方向 
                       0: 从左到右,从上到下 
                       1: 从左到右,从下到上 
                       2: 从右到左,从上到下 
                       3: 从右到左,从下到上
        
        返回值:
            字符串: 返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y" (图片左上角的坐标)
                   比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),
                   第二个是序号为2的图片,坐标(30,40)
                   (由于内存限制,返回的图片数量最多为1500个左右)
        
        示例:
            # 组合图片地址信息
            pic_info = dm.AppendPicAddr("", 12034, 643)
            pic_info = dm.AppendPicAddr(pic_info, 328435, 8935)
            
            # 查找所有匹配的图片
            ret = dm.ai.AI找图Ex内存版(0, 0, 2000, 2000, pic_info, 0.9, 0)
            if ret:
                for item in ret.split("|"):
                    id, x, y = item.split(",")
                    print(f"找到第{id}号图片,坐标是:({x}, {y})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in AI找图Ex内存版: {msg}")
            return ""
            
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in AI找图Ex内存版: {msg}")
            return ""
            
        try:
            return self._dm.AiFindPicMemEx(左上x, 左上y, 右下x, 右下y, 图片信息, 相似度, 方向)
        except Exception as e:
            print(f"Error in AI找图Ex内存版: {str(e)}")
            return ""

    def YOLO检测对象(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 置信度: float, 框合并阈值: float) -> str:
        """
        函数简介:
            在指定范围内检测对象。
            需要先加载Ai模块。
        
        函数原型:
            string AiYoloDetectObjects(x1,y1,x2,y2,prob,iou)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            置信度 双精度浮点数: 置信度阈值,超过这个值的对象才会被检测
            框合并阈值 双精度浮点数: 用于对多个检测框进行合并,取值建议0.4-0.6之间
        
        返回值:
            字符串: 返回的是所有检测到的对象,格式是"类名,置信度,x,y,w,h|...."
        
        示例:
            dm.ai.YOLO使用模型(0)
            ret = dm.ai.YOLO检测对象(0, 0, 2000, 2000, 0.5, 0.45)
            if ret:
                for obj in ret.split("|"):
                    cls, prob, x, y, w, h = obj.split(",")
                    print(f"找到{cls}, 置信度:{prob}, 位置:({x},{y},{w},{h})")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in YOLO检测对象: {msg}")
            return ""
        
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in YOLO检测对象: {msg}")
            return ""
        
        try:
            return self._dm.AiYoloDetectObjects(左上x, 左上y, 右下x, 右下y, 置信度, 框合并阈值)
        except Exception as e:
            print(f"Error in YOLO检测对象: {str(e)}")
            return ""

    def YOLO检测对象到数据(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 置信度: float, 框合并阈值: float, 数据指针: int, 数据长度: int, 模式: int) -> int:
        """
        函数简介:
            在指定范围内检测对象,把结果输出到BMP图像数据。
            用于二次开发。
            需要先加载Ai模块。
        
        函数原型:
            long AiYoloDetectObjectsToDataBmp(x1,y1,x2,y2,prob,iou,data,size,mode)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            置信度 双精度浮点数: 置信度阈值,超过这个值的对象才会被检测
            框合并阈值 双精度浮点数: 用于对多个检测框进行合并,取值建议0.4-0.6之间
            数据指针 整形数: 返回图片的数据指针
            数据长度 整形数: 返回图片的数据长度
            模式 整形数: 0表示绘制的文字信息里包含置信度,1表示不包含
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            data = 0
            size = 0
            ret = dm.ai.YOLO检测对象到数据(0, 0, 2000, 2000, 0.5, 0.45, data, size, 0)
            if ret == 1:
                print(f"检测成功,数据长度:{size}")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in YOLO检测对象到数据: {msg}")
            return 0
        
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in YOLO检测对象到数据: {msg}")
            return 0
        
        try:
            return self._dm.AiYoloDetectObjectsToDataBmp(左上x, 左上y, 右下x, 右下y, 置信度, 框合并阈值, 数据指针, 数据长度, 模式)
        except Exception as e:
            print(f"Error in YOLO检测对象到数据: {str(e)}")
            return 0

    def YOLO检测对象到文件(self, 左上x: int, 左上y: int, 右下x: int, 右下y: int, 置信度: float, 框合并阈值: float, 文件名: str, 模式: int) -> int:
        """
        函数简介:
            在指定范围内检测对象,把结果输出到指定的BMP文件。
            需要先加载Ai模块。
        
        函数原型:
            long AiYoloDetectObjectsToFile(x1,y1,x2,y2,prob,iou,file,mode)
        
        参数定义:
            左上x 整形数: 区域的左上X坐标
            左上y 整形数: 区域的左上Y坐标
            右下x 整形数: 区域的右下X坐标
            右下y 整形数: 区域的右下Y坐标
            置信度 双精度浮点数: 置信度阈值,超过这个值的对象才会被检测
            框合并阈值 双精度浮点数: 用于对多个检测框进行合并,取值建议0.4-0.6之间
            文件名 字符串: 图片名,比如"test.bmp"
            模式 整形数: 0表示绘制的文字信息里包含置信度,1表示不包含
        
        返回值:
            整形数: 0: 失败 1: 成功
        
        示例:
            dm.ai.YOLO使用模型(0)
            ret = dm.ai.YOLO检测对象到文件(0, 0, 2000, 2000, 0.5, 0.45, "test.bmp", 0)
            if ret == 1:
                print("检测结果已保存到文件")
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in YOLO检测对象到文件: {msg}")
            return 0
        
        ai_ret, msg = self._check_ai_loaded()
        if not ai_ret:
            print(f"Error in YOLO检测对象到文件: {msg}")
            return 0
        
        try:
            return self._dm.AiYoloDetectObjectsToFile(左上x, 左上y, 右下x, 右下y, 置信度, 框合并阈值, 文件名, 模式)
        except Exception as e:
            print(f"Error in YOLO检测对象到文件: {str(e)}")
            return 0

    def YOLO释放模型(self, 序号: int) -> int:
        """
        函数简介:
            卸载指定的模型。
            需要先加载Ai模块。
        
        函数原型:
            long AiYoloFreeModel(index)
        
        参数定义:
            序号 整形数: 模型的序号,最多支持20个,从0开始
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.ai.YOLO释放模型(0)
            if ret == 1:
                print("模型释放成功")
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloFreeModel(序号)
        except Exception as e:
            print(f"Error in YOLO释放模型: {str(e)}")
            return 0

    def YOLO对象转字符串(self, 对象列表: str) -> str:
        """
        函数简介:
            把通过YOLO检测对象或者YOLO排序对象的结果,按照顺序把class信息连接输出。
            需要先加载Ai模块。
        
        函数原型:
            string AiYoloObjectsToString(objects)
        
        参数定义:
            对象列表 字符串: YOLO检测对象或者YOLO排序对象的返回值
        
        返回值:
            字符串: 返回的是class信息连接后的信息
        
        示例:
            dm.ai.YOLO使用模型(0)
            objects = dm.ai.YOLO检测对象(0, 0, 2000, 2000, 0.5, 0.45)
            sorted_objects = dm.ai.YOLO排序对象(objects)
            print(dm.ai.YOLO对象转字符串(sorted_objects))
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloObjectsToString(对象列表)
        except Exception as e:
            print(f"Error in YOLO对象转字符串: {str(e)}")
            return ""

    def YOLO设置模型(self, 序号: int, 文件名: str, 密码: str = "") -> int:
        """
        函数简介:
            从文件加载指定的模型。
            需要先加载Ai模块。
            
            注意:
            模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型。
            另外,加载onnx时得确保和这个onnx同名的class文件也在同目录下。
            比如加载xxxx.onnx,那么必须得有个相应的xxxx.class。
        
        函数原型:
            long AiYoloSetModel(index,file,pwd)
        
        参数定义:
            序号 整形数: 模型的序号,最多支持20个,从0开始
            文件名 字符串: 模型文件名,比如"xxxx.onnx"或者"xxxx.dmx"
            密码 字符串: 模型的密码,仅对dmx格式有效
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            # 加载onnx模型
            ret = dm.ai.YOLO设置模型(0, "xxxx.onnx", "")
            # 加载dmx模型
            ret = dm.ai.YOLO设置模型(1, "xxxx.dmx", "123")
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloSetModel(序号, 文件名, 密码)
        except Exception as e:
            print(f"Error in YOLO设置模型: {str(e)}")
            return 0

    def YOLO设置内存模型(self, 序号: int, 数据地址: int, 数据大小: int, 密码: str) -> int:
        """
        函数简介:
            从内存加载指定的模型。
            仅支持dmx格式的内存。
            需要先加载Ai模块。
            
            注意:
            模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型。
        
        函数原型:
            long AiYoloSetModelMemory(index,data,size,pwd)
        
        参数定义:
            序号 整形数: 模型的序号,最多支持20个,从0开始
            数据地址 整形数: dmx模型的内存地址
            数据大小 整形数: dmx模型的大小
            密码 字符串: dmx模型的密码
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            ret = dm.ai.YOLO设置内存模型(0, 2343253, 23432432, "123")
            if ret == 1:
                print("内存模型加载成功")
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloSetModelMemory(序号, 数据地址, 数据大小, 密码)
        except Exception as e:
            print(f"Error in YOLO设置内存模型: {str(e)}")
            return 0

    def YOLO设置版本(self, ver: str) -> int:
        """
        函数简介:
            设置Yolo的版本
        
        函数原型:
            long AiYoloSetVersion(ver)
        
        参数定义:
            ver 字符串: Yolo的版本信息,目前可选的值只有"v5-7.0"
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            let ret = window.pywebview.api.dm.ai.YOLO设置版本("v5-7.0");
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloSetVersion(ver)
        except Exception as e:
            print(f"Error in YOLO设置版本: {str(e)}")
            return 0

    def YOLO排序对象(self, objects: str, height: int = 0) -> str:
        """
        函数简介:
            把通过AiYoloDetectObjects的结果进行排序。
            排序按照从上到下,从左到右。
        
        函数原型:
            string AiYoloSortsObjects(objects,height)
        
        参数定义:
            objects 字符串: AiYoloDetectObjects的返回值
            height 整形数: 行高信息,排序时需要使用此行高。
                    用于确定两个检测框是否处于同一行。
                    如果两个框的Y坐标相差绝对值小于此行高,认为是同一行。
        
        返回值:
            字符串: 返回的是所有检测到的对象。格式是"类名,置信度,x,y,w,h|...."。
                 如果没检测到任何对象,返回空字符串。
        
        示例:
            window.pywebview.api.dm.ai.YOLO使用模型(0);
            let objects = window.pywebview.api.dm.ai.YOLO检测对象(0, 0, 2000, 2000, 0.5, 0.45);
            let sorted_objects = window.pywebview.api.dm.ai.YOLO排序对象(objects);
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloSortsObjects(objects, height)
        except Exception as e:
            print(f"Error in YOLO排序对象: {str(e)}")
            return ""

    def YOLO使用模型(self, index: int) -> int:
        """
        函数简介:
            切换当前使用的模型序号。
            用于AiYoloDetectXX等系列接口。
        
        函数原型:
            long AiYoloUseModel(index)
        
        参数定义:
            index 整形数: 模型的序号,最多支持20个,从0开始
        
        返回值:
            整形数: 1: 成功 0: 失败
        
        示例:
            let ret = window.pywebview.api.dm.ai.YOLO使用模型(0);
        """
        try:
            self._check_dm()
            self._check_ai_loaded()
            return self._dm.AiYoloUseModel(index)
        except Exception as e:
            print(f"Error in YOLO使用模型: {str(e)}")
            return 0

    def 加载AI模块(self, file: str) -> int:
        """
        函数简介:
            加载Ai模块。
            Ai模块从后台下载。
            模块加载仅支持所有的正式版本。
        
        函数原型:
            long LoadAi(file)
        
        参数定义:
            file 字符串: ai模块的路径。
            比如绝对路径c:\\ai.module或者相对路径ai.module等。
        
        返回值:
            整形数: 1: 成功
                    -1: 打开文件失败
                    -2: 内存初始化失败。如果是正式版本,出现这个错误可以联系我解决。
                    -3: 参数错误
                    -4: 加载错误
                    -5: Ai模块初始化失败
                    -6: 内存分配失败
        
        示例:
            let ret = window.pywebview.api.dm.ai.加载AI模块("ai.module");
            console.log(ret);
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 加载AI模块: {msg}")
            return -1
            
        try:
            ret = self._dm.LoadAi(file)
            if ret == 1:
                self._ai_loaded = True
            return ret
        except Exception as e:
            print(f"Error in 加载AI模块: {str(e)}")
            return -1

    def 加载AI内存模块(self, data: int, size: int) -> int:
        """
        函数简介:
            从内存加载Ai模块。
            Ai模块从后台下载。
            模块加载仅支持所有的正式版本。
        
        函数原型:
            long LoadAiMemory(data,size)
        
        参数定义:
            data 整形数: ai模块在内存中的地址
            size 整形数: ai模块在内存中的大小
        
        返回值:
            整形数: 1: 成功
                    -1: 打开文件失败
                    -2: 内存初始化失败。如果是正式版本,出现这个错误可以联系我解决。
                    -3: 参数错误
                    -4: 加载错误
                    -5: Ai模块初始化失败
                    -6: 内存分配失败
        
        示例:
            // 先获取ai.module的内存地址
            let ret = window.pywebview.api.dm.ai.加载AI内存模块(234735, 32948);
            console.log(ret);
        """
        dm_ret, msg = self._check_dm()
        if not dm_ret:
            print(f"Error in 加载AI内存模块: {msg}")
            return -1
            
        try:
            ret = self._dm.LoadAiMemory(data, size)
            if ret == 1:
                self._ai_loaded = True
            return ret
        except Exception as e:
            print(f"Error in 加载AI内存模块: {str(e)}")
            return -1

    def AiFindPic(self, *args, **kwargs):
        """英文别名，调用AI找图"""
        return self.AI找图(*args, **kwargs)

    def AiFindPicEx(self, *args, **kwargs):
        """英文别名，调用AI找图Ex"""
        return self.AI找图Ex(*args, **kwargs)

    def AiFindPicMem(self, *args, **kwargs):
        """英文别名，调用AI找图内存版"""
        return self.AI找图内存版(*args, **kwargs)

    def AiFindPicMemEx(self, *args, **kwargs):
        """英文别名，调用AI找图Ex内存版"""
        return self.AI找图Ex内存版(*args, **kwargs)

    def AiYoloDetectObjects(self, *args, **kwargs):
        """英文别名，调用YOLO检测对象"""
        return self.YOLO检测对象(*args, **kwargs)

    def AiYoloDetectObjectsToDataBmp(self, *args, **kwargs):
        """英文别名，调用YOLO检测对象到数据"""
        return self.YOLO检测对象到数据(*args, **kwargs)

    def AiYoloDetectObjectsToFile(self, *args, **kwargs):
        """英文别名，调用YOLO检测对象到文件"""
        return self.YOLO检测对象到文件(*args, **kwargs)

    def AiYoloFreeModel(self, *args, **kwargs):
        """英文别名，调用YOLO释放模型"""
        return self.YOLO释放模型(*args, **kwargs)

    def AiYoloObjectsToString(self, *args, **kwargs):
        """英文别名，调用YOLO对象转字符串"""
        return self.YOLO对象转字符串(*args, **kwargs)

    def AiYoloSetModel(self, *args, **kwargs):
        """英文别名，调用YOLO设置模型"""
        return self.YOLO设置模型(*args, **kwargs)

    def AiYoloSetModelMemory(self, *args, **kwargs):
        """英文别名，调用YOLO设置内存模型"""
        return self.YOLO设置内存模型(*args, **kwargs)

    def AiYoloSetVersion(self, *args, **kwargs):
        """英文别名，调用YOLO设置版本"""
        return self.YOLO设置版本(*args, **kwargs)

    def AiYoloSortsObjects(self, *args, **kwargs):
        """英文别名，调用YOLO排序对象"""
        return self.YOLO排序对象(*args, **kwargs)

    def AiYoloUseModel(self, *args, **kwargs):
        """英文别名，调用YOLO使用模型"""
        return self.YOLO使用模型(*args, **kwargs)

    def LoadAi(self, *args, **kwargs):
        """英文别名，调用加载AI模块"""
        return self.加载AI模块(*args, **kwargs)

    def LoadAiMemory(self, *args, **kwargs):
        """英文别名，调用加载AI内存模块"""
        return self.加载AI内存模块(*args, **kwargs)

    def AiEnableFindPicWindow(self, *args, **kwargs):
        """英文别名，调用启用_显示找图结果"""
        return self.启用_显示找图结果(*args, **kwargs)

