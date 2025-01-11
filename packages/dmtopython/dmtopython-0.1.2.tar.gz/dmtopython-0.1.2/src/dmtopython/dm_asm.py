class DmAsm:
    def __init__(self, dm):
        self._dm = dm

    def AsmAdd(self, asm_ins: str) -> int:
        """
        函数简介:
            添加指定的MASM汇编指令. 支持标准的masm汇编指令.
        函数原型:
            long AsmAdd(asm_ins)
        参数定义:
            asm_ins 字符串: MASM汇编指令,大小写均可以
            比如 "mov eax,1" ,也支持直接加入字节，比如"emit 90 90 90 90"等.
            同时也支持跳转指令，标记. 标记必须以":"开头.
            跳转指令后必须接本次AsmCall之前的存在的有效Label.
            另外跳转只支持短跳转,就是跳转的字节码不能超过128个字节.
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.AsmAdd(asm_ins)

    def AsmCall(self, hwnd: int, mode: int) -> int:
        """
        函数简介:
            执行用AsmAdd加到缓冲中的指令.
        函数原型:
            LONGLONG AsmCall(hwnd,mode)
        参数定义:
            hwnd 整形数: 窗口句柄
            mode 整形数: 模式，取值如下
            0: 在本进程中进行执行，这时hwnd无效. 注: 此模式会创建线程.
            1: 对hwnd指定的进程内执行,注入模式为创建远程线程
            2: 必须在对目标窗口进行注入绑定后,才可以用此模式(直接在目标进程创建线程)
            3: 同模式2,但是此模式不会创建线程,而直接在hwnd所在线程执行.
            4: 同模式0, 但是此模式不会创建线程,直接在当前调用AsmCall的线程内执行.
            5: 对hwnd指定的进程内执行,注入模式为APC. 此模式必须开启memory盾
            6: 直接hwnd所在线程执行.
        返回值:
            长整形数: 获取执行汇编代码以后的EAX的值(32位进程),或者RAX的值(64位进程)
            -200: 执行中出现错误
            -201: 使用模式5时，没有开启memory盾
        """
        return self._dm.AsmCall(hwnd, mode)

    def AsmCallEx(self, hwnd: int, mode: int, base_addr: str) -> int:
        """
        函数简介:
            执行用AsmAdd加到缓冲中的指令. 这个接口同AsmCall,
            但是由于插件内部在每次AsmCall时,都会有对目标进程分配内存的操作,这样会不够效率.
            所以增加这个接口，可以让调用者指定分配好的内存,并在此内存上执行call的操作.
        函数原型:
            LONGLONG AsmCallEx(hwnd,mode,base_addr)
        参数定义:
            hwnd 整形数: 窗口句柄
            mode 整形数: 同AsmCall的mode参数
            base_addr 字符串: 16进制格式. 比如"45A00000"
            此参数指定的地址必须要求有可读可写可执行属性.
            并且内存大小最少要200个字节. 模式6要求至少400个字节.
        返回值:
            长整形数: 同AsmCall的返回值
        """
        return self._dm.AsmCallEx(hwnd, mode, base_addr)

    def AsmClear(self) -> int:
        """
        函数简介:
            清除汇编指令缓冲区 用AsmAdd添加到缓冲的指令全部清除
        函数原型:
            long AsmClear()
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.AsmClear()

    def AsmSetTimeout(self, time_out: int, param: int) -> int:
        """
        函数简介:
            此接口对AsmCall和AsmCallEx中的模式5和6中内置的一些延时参数进行设置.
        函数原型:
            long AsmSetTimeout(time_out,param)
        参数定义:
            time_out 整形数: 超时时间(毫秒),默认10000,-1表示无限等待
            param 整形数: 模式6的执行间隔(毫秒),默认100
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.AsmSetTimeout(time_out, param)

    def Assemble(self, base_addr: int, is_64bit: int) -> str:
        """
        函数简介:
            把汇编缓冲区的指令转换为机器码 并用16进制字符串的形式输出
        函数原型:
            string Assemble(base_addr,is_64bit)
        参数定义:
            base_addr 长整形数: 用AsmAdd添加到缓冲区的第一条指令所在的地址
            is_64bit 整形数: 表示缓冲区的指令是32位还是64位. 32位表示为0,64位表示为1
        返回值:
            字符串: 机器码，比如 "aa bb cc"这样的形式
        """
        return self._dm.Assemble(base_addr, is_64bit)

    def DisAssemble(self, asm_code: str, base_addr: int, is_64bit: int) -> str:
        """
        函数简介:
            把指定的机器码转换为汇编语言输出
        函数原型:
            string DisAssemble(asm_code,base_addr,is_64bit)
        参数定义:
            asm_code 字符串: 机器码，形式如 "aa bb cc"这样的16进制表示的字符串
            base_addr 长整形数: 指令所在的地址
            is_64bit 整形数: 表示asm_code表示的指令是32位还是64位. 32位表示为0,64位表示为1
        返回值:
            字符串: MASM汇编语言字符串.如果有多条指令，则每条指令以字符"|"连接.
        """
        return self._dm.DisAssemble(asm_code, base_addr, is_64bit)

    def SetShowAsmErrorMsg(self, show: int) -> int:
        """
        函数简介:
            设置是否弹出汇编功能中的错误提示,默认是打开.
        函数原型:
            long SetShowAsmErrorMsg(show)
        参数定义:
            show 整形数: 0表示不打开,1表示打开
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.SetShowAsmErrorMsg(show)

    # 中文别名
    添加汇编指令 = AsmAdd
    执行汇编指令 = AsmCall
    执行汇编指令Ex = AsmCallEx
    清空汇编指令 = AsmClear
    设置汇编超时 = AsmSetTimeout
    汇编转机器码 = Assemble
    机器码转汇编 = DisAssemble
    设置显示汇编错误 = SetShowAsmErrorMsg 