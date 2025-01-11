import win32com.client

class DmFile:
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

    def CopyFile(self, src_file: str, dst_file: str, over: int) -> int:
        """
        函数简介:
            拷贝文件
        函数原型:
            long CopyFile(src_file,dst_file,over)
        参数定义:
            src_file 字符串: 原始文件名
            dst_file 字符串: 目标文件名
            over 整形数: 取值如下
                0 : 如果dst_file文件存在则不覆盖返回
                1 : 如果dst_file文件存在则覆盖
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.CopyFile(src_file, dst_file, over)

    def CreateFolder(self, folder: str) -> int:
        """
        函数简介:
            创建指定目录
        函数原型:
            long CreateFolder(folder)
        参数定义:
            folder 字符串: 目录名
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.CreateFolder(folder)

    def DecodeFile(self, file: str, pwd: str) -> int:
        """
        函数简介:
            解密指定的文件
        函数原型:
            long DecodeFile(file,pwd)
        参数定义:
            file 字符串: 文件名
            pwd 字符串: 密码
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            如果此文件没加密，调用此函数不会有任何效果
            插件所有的字库 图片 ini都是用此接口来解密
        """
        return self._dm.DecodeFile(file, pwd)

    def DeleteFile(self, file: str) -> int:
        """
        函数简介:
            删除文件
        函数原型:
            long DeleteFile(file)
        参数定义:
            file 字符串: 文件名
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.DeleteFile(file)

    def DeleteFolder(self, folder: str) -> int:
        """
        函数简介:
            删除指定目录
        函数原型:
            long DeleteFolder(folder)
        参数定义:
            folder 字符串: 目录名
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.DeleteFolder(folder)

    def DeleteIni(self, section: str, key: str, file: str) -> int:
        """
        函数简介:
            删除指定的ini小节
        函数原型:
            long DeleteIni(section,key,file)
        参数定义:
            section 字符串: 小节名
            key 字符串: 变量名. 如果这个变量为空串，则删除整个section小节
            file 字符串: ini文件名
        返回值:
            整形数: 0: 失败 1: 成功
        注: 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱
        """
        return self._dm.DeleteIni(section, key, file)

    def DeleteIniPwd(self, section: str, key: str, file: str, pwd: str) -> int:
        """
        函数简介:
            删除指定的ini小节.支持加密文件
        函数原型:
            long DeleteIniPwd(section,key,file,pwd)
        参数定义:
            section 字符串: 小节名
            key 字符串: 变量名. 如果这个变量为空串，则删除整个section小节
            file 字符串: ini文件名
            pwd 字符串: 密码
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            此函数是多线程安全的,但多进程不安全
            如果此文件没加密，调用此函数会自动加密
        """
        return self._dm.DeleteIniPwd(section, key, file, pwd)

    def DownloadFile(self, url: str, save_file: str, timeout: int) -> int:
        """
        函数简介:
            从internet上下载一个文件
        函数原型:
            long DownloadFile(url,save_file,timeout)
        参数定义:
            url 字符串: 下载的url地址
            save_file 字符串: 要保存的文件名
            timeout 整形数: 连接超时时间，单位是毫秒
        返回值:
            整形数:
            1 : 成功
            -1 : 网络连接失败
            -2 : 写入文件失败
        """
        return self._dm.DownloadFile(url, save_file, timeout)

    def EncodeFile(self, file: str, pwd: str) -> int:
        """
        函数简介:
            加密指定的文件
        函数原型:
            long EncodeFile(file,pwd)
        参数定义:
            file 字符串: 文件名
            pwd 字符串: 密码
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            如果此文件已经加密，调用此函数不会有任何效果
            插件所有的字库 图片 ini都是用此接口来加密
        """
        return self._dm.EncodeFile(file, pwd)

    def EnumIniKey(self, section: str, file: str) -> str:
        """
        函数简介:
            根据指定的ini文件以及section,枚举此section中所有的key名
        函数原型:
            string EnumIniKey(section,file)
        参数定义:
            section 字符串: 小节名. (不可为空)
            file 字符串: ini文件名
        返回值:
            字符串: 每个key用"|"来连接，如果没有key，则返回空字符串. 比如"aaa|bbb|ccc"
        注: 
            此函数是多线程安全的
            此函数无法枚举没有section的key
        """
        return self._dm.EnumIniKey(section, file)

    def EnumIniKeyPwd(self, section: str, file: str, pwd: str) -> str:
        """
        函数简介:
            根据指定的ini文件以及section,枚举此section中所有的key名.可支持加密文件
        函数原型:
            string EnumIniKeyPwd(section,file,pwd)
        参数定义:
            section 字符串: 小节名. (不可为空)
            file 字符串: ini文件名
            pwd 字符串: 密码
        返回值:
            字符串: 每个key用"|"来连接，如果没有key，则返回空字符串. 比如"aaa|bbb|ccc"
        注: 
            此函数是多线程安全的,但多进程不安全
            此函数无法枚举没有section的key
            如果文件没加密，也可以正常读取
        """
        return self._dm.EnumIniKeyPwd(section, file, pwd)

    def EnumIniSection(self, file: str) -> str:
        """
        函数简介:
            根据指定的ini文件,枚举此ini中所有的Section(小节名)
        函数原型:
            string EnumIniSection(file)
        参数定义:
            file 字符串: ini文件名
        返回值:
            字符串: 每个小节名用"|"来连接，如果没有小节，则返回空字符串. 比如"aaa|bbb|ccc"
        """
        return self._dm.EnumIniSection(file)

    def GetFileLength(self, file: str) -> int:
        """
        函数简介:
            获取指定的文件长度
        函数原型:
            long GetFileLength(file)
        参数定义:
            file 字符串: 文件名
        返回值:
            整形数: 文件长度(字节数)
        """
        return self._dm.GetFileLength(file)

    def GetRealPath(self, path: str) -> str:
        """
        函数简介:
            获取指定文件或目录的真实路径
        函数原型:
            string GetRealPath(path)
        参数定义:
            path 字符串: 路径名,可以是文件路径，也可以是目录. 这里必须是全路径
        返回值:
            字符串: 真实路径,如果失败,返回空字符串
        注: 这个功能可以获取到路径中有符号链接之后的，真实路径
        """
        return self._dm.GetRealPath(path)

    def IsFileExist(self, file: str) -> int:
        """
        函数简介:
            判断指定文件是否存在
        函数原型:
            long IsFileExist(file)
        参数定义:
            file 字符串: 文件名
        返回值:
            整形数: 0: 不存在 1: 存在
        """
        return self._dm.IsFileExist(file)

    def IsFolderExist(self, folder: str) -> int:
        """
        函数简介:
            判断指定目录是否存在
        函数原型:
            long IsFolderExist(folder)
        参数定义:
            folder 字符串: 目录名
        返回值:
            整形数: 0: 不存在 1: 存在
        """
        return self._dm.IsFolderExist(folder)

    def MoveFile(self, src_file: str, dst_file: str) -> int:
        """
        函数简介:
            移动文件
        函数原型:
            long MoveFile(src_file,dst_file)
        参数定义:
            src_file 字符串: 原始文件名
            dst_file 字符串: 目标文件名
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.MoveFile(src_file, dst_file)

    def ReadFile(self, file: str) -> str:
        """
        函数简介:
            从指定的文件读取内容
        函数原型:
            string ReadFile(file)
        参数定义:
            file 字符串: 文件
        返回值:
            字符串: 读入的文件内容
        """
        return self._dm.ReadFile(file)

    def ReadIni(self, section: str, key: str, file: str) -> str:
        """
        函数简介:
            从Ini中读取指定信息
        函数原型:
            string ReadIni(section,key,file)
        参数定义:
            section 字符串: 小节名
            key 字符串: 变量名
            file 字符串: ini文件名
        返回值:
            字符串: 字符串形式表达的读取到的内容
        注: 此函数是多线程安全的
        """
        return self._dm.ReadIni(section, key, file)

    def ReadIniPwd(self, section: str, key: str, file: str, pwd: str) -> str:
        """
        函数简介:
            从Ini中读取指定信息.可支持加密文件
        函数原型:
            string ReadIniPwd(section,key,file,pwd)
        参数定义:
            section 字符串: 小节名
            key 字符串: 变量名
            file 字符串: ini文件名
            pwd 字符串: 密码
        返回值:
            字符串: 字符串形式表达的读取到的内容
        注: 
            此函数是多线程安全的,但多进程不安全
            如果文件没加密，也可以正常读取
        """
        return self._dm.ReadIniPwd(section, key, file, pwd)

    def SelectDirectory(self) -> str:
        """
        函数简介:
            弹出选择文件夹对话框，并返回选择的文件夹
        函数原型:
            string SelectDirectory()
        返回值:
            字符串: 选择的文件夹全路径
        注: 此接口要求当前线程的COM模型必须是STA
        """
        return self._dm.SelectDirectory()

    def SelectFile(self) -> str:
        """
        函数简介:
            弹出选择文件对话框，并返回选择的文件
        函数原型:
            string SelectFile()
        返回值:
            字符串: 选择的文件全路径
        注: 此接口要求当前线程的COM模型必须是STA
        """
        return self._dm.SelectFile()

    def WriteFile(self, file: str, content: str) -> int:
        """
        函数简介:
            向指定文件追加字符串
        函数原型:
            long WriteFile(file,content)
        参数定义:
            file 字符串: 文件
            content 字符串: 写入的字符串
        返回值:
            整形数: 0: 失败 1: 成功
        """
        return self._dm.WriteFile(file, content)

    def WriteIni(self, section: str, key: str, value: str, file: str) -> int:
        """
        函数简介:
            向指定的Ini写入信息
        函数原型:
            long WriteIni(section,key,value,file)
        参数定义:
            section 字符串: 小节名
            key 字符串: 变量名
            value 字符串: 变量内容
            file 字符串: ini文件名
        返回值:
            整形数: 0: 失败 1: 成功
        注: 此函数是多线程安全的
        """
        return self._dm.WriteIni(section, key, value, file)

    def WriteIniPwd(self, section: str, key: str, value: str, file: str, pwd: str) -> int:
        """
        函数简介:
            向指定的Ini写入信息.支持加密文件
        函数原型:
            long WriteIniPwd(section,key,value,file,pwd)
        参数定义:
            section 字符串: 小节名
            key 字符串: 变量名
            value 字符串: 变量内容
            file 字符串: ini文件名
            pwd 字符串: 密码
        返回值:
            整形数: 0: 失败 1: 成功
        注: 
            此函数是多线程安全的,但多进程不安全
            如果此文件没加密，调用此函数会自动加密
        """
        return self._dm.WriteIniPwd(section, key, value, file, pwd)

    # 中文别名
    复制文件 = CopyFile
    创建目录 = CreateFolder
    解密文件 = DecodeFile
    删除文件 = DeleteFile
    删除目录 = DeleteFolder
    删除配置项 = DeleteIni
    删除加密配置项 = DeleteIniPwd
    下载文件 = DownloadFile
    加密文件 = EncodeFile
    枚举配置项 = EnumIniKey
    枚举加密配置项 = EnumIniKeyPwd
    枚举配置节 = EnumIniSection
    获取文件长度 = GetFileLength
    获取真实路径 = GetRealPath
    文件是否存在 = IsFileExist
    目录是否存在 = IsFolderExist
    移动文件 = MoveFile
    读取文件 = ReadFile
    读取配置项 = ReadIni
    读取加密配置项 = ReadIniPwd
    选择目录 = SelectDirectory
    选择文件 = SelectFile
    写入文件 = WriteFile
    写入配置项 = WriteIni
    写入加密配置项 = WriteIniPwd 