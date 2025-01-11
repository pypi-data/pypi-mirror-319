'''
答题接口和答题器之间的通讯协议

数据结构定义:

// 答题类型 对应于FaqRequestPacket中的request_type
#define REQUEST_TYPE_POS   0           // 坐标
#define REQUEST_TYPE_ABCD  1           // 选项
#define REQUEST_TYPE_OTHER 2           // 文本
#define REQUEST_TYPE_DOUBLE_POS 3      // 双坐标

 

#pragma pack(push) //保存对齐状态
#pragma pack(4)//设定为4字节对齐

// 发送包结构体
typedef struct
{
    // 服务器转发用(分流的时候可能会用到)
    SOCKET socket;               // 分流上级发送的socket id.
    char  ip[32];                // 分流上级机器IP

// 客户端内容
    DWORD request_type; // 答题类型
    DWORD data_len;     // 真实数据的长度
    char  data[1];      // 数据指针.
}FaqRequestPacket;

// 接收包结构体
typedef struct
{
    // 服务器转发用
    SOCKET socket;         // 同FaqRequestPacket
    char  ip[32];          // 同FaqRequestPacket

// 客户端内容
    char result[256];      // 接收到的答案. 文本形式描述. 
}FaqReceivePacket;

#pragma pack(pop)//恢复对齐状态

组织结构图通讯过程流程描述



 

 

 

 

 

 

 

 

 

 

 

 

 

发送数据包详细格式解析:

发送的数据包由包头+数据体两部分组成.

其中包头的长度是sizeof(FaqRequestPacket). 

数据体的长度是FaqRequestPacket结构体中data_len指定的长度. 用图形描述如下:

                              整个数据包(发送)

    

        FaqRequestPacket(12字节)  |    数据(数据头+数据体)

 

      长度sizeof(FaqRequestPacket)        长度(data_len)

 

其中数据部分的结构定义如下:

数据部分包含2部分，数据头和数据体.
数据头12个字节. 前4个字节是一个头标识. 内容是4个字符 'D' 'M' 'F' 'Q'.
接下来4个字节的内容表示当前图像有多少帧. 如果是静态图像此值为1或者65535. (65535表示是BMP图像数据，65534表示是TXT文字数据(文字编码是GBK))
再接下来4个字节表示每帧之间的延时是多少毫秒. 如果是静态图像此值为0

数据体部分是连续顺序存放图片数据. 按照帧的顺序依次存放. 每个帧前的4个字节表示当前帧有多少个字节.比如
(长度)帧数1(长度)帧数2……(长度)帧数N.   每个帧的图像格式是jpeg或者bmp格式,或者是TXT文字数据

综上,发送包总的长度描述如下:
12字节(sizeof(FaqRequestPacket)) + 12字节(数据头) + 4字节(第一帧长度) + (第一帧数据) + 4字节(第二帧长度) + (第二帧数据) + ….


接收包的格式很简单。就不多说了.

 

注意的是，以上只是接收和发送的纯数据格式. 真正发送时，还会在包头加上序列号，长度等校验信息. 以下是我用到的发送和接收数据的函数源码. 其他语言也可以参考.

 

 

// Common Return Code.

#define RET_SUCCESS                                  1

#define RET_FAIL                                 -1

 

#define RET_NET_NOT_INIT                         -2

#define RET_NO_ERROR                             1

#define RET_ACCEPT_SOCKET_ERROR                      -1

#define RET_CLIENT_SOCKET_ERROR                      -2

#define RET_NO_SOCKET                                -3

#define RET_NO_CONNECTION                            -4

#define RET_SOCKET_CLOSED                            0

#define RET_TIMEOUT                                  -5

#define RET_SOCKET_SHUT_DOWN                         -6

#define RET_SERVER_NOT_PREPARED                      -7

#define RET_SOCKET_NO_ORDER                          -8

#define RET_CONNECT                                  -9

#define RET_DISCONNECT                               -10

#define RET_NO_AVAILABLE_PEER                        -11

#define RET_NO_PEER                                  -12

#define RET_NO_PACKAGE                               -13

 

#define READ_TIMEOUT                             5000

#define WRITE_TIMEOUT                                5000

 

#define READ_UNIT_SIZE                        512 // less than general MTU size.

#define WRITE_UNIT_SIZE                       512 // less than general MTU size.

#define MSG_LEN_INFO_SIZE                     4

 

#define MAX_NET_TRIAL                         30

 

#define CHECK_ALIVE_VALUE                     -987654321

 

#define MAX_RECV_AGAIN                        3

 

int TCPRead(SOCKET Socket, char *Buffer, DWORD BufferSize, DWORD TimeoutMilli, DWORD *ErrorCode)

{

    BOOL bError;

    int ReturnCode;

    char LenInfo[MSG_LEN_INFO_SIZE];

    int RetLen;

    char ReadBuff[READ_UNIT_SIZE];

    DWORD CopyingSize;

    int ResRecv;

    int Timeout;

    char *pReadingPoint;

    int ToReadSize;

    int UnitReadSize;

    int TimeoutOld;

    int OutLen;

    int LoopCount;

    int RecvAgainCount;

 

    bError = 0;

    ReturnCode = RET_FAIL;

    TimeoutOld = -1;

 

    if (0 > Socket || 0 == ErrorCode)

    {

       bError = 1;

       ReturnCode = RET_FAIL;

       goto ErrHand;

    }

 

    *ErrorCode = 0;

 

    OutLen = sizeof (TimeoutOld);

    if (SOCKET_ERROR == getsockopt(Socket, SOL_SOCKET, SO_RCVTIMEO, (char *)&TimeoutOld, &OutLen))

    {

       *ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET_FAIL;

       goto ErrHand;

    }

 

    Timeout = TimeoutMilli; // Assigning is due to input the address of the Timeout. 0 = infinite.

    if (SOCKET_ERROR == setsockopt(Socket, SOL_SOCKET, SO_RCVTIMEO, (char *)&Timeout, sizeof (Timeout)))

    {

       *ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET_FAIL;

       goto ErrHand;

    }

 

    if (0 == Buffer || 0 == BufferSize)

    {

RecvAgainNew:     

       RecvAgainCount = 0;

RecvAgain:

       ZeroMemory(LenInfo, sizeof (LenInfo));

       ResRecv = recv(Socket, LenInfo, sizeof (LenInfo), MSG_PEEK);

       if (SOCKET_ERROR == ResRecv)

       { 

           *ErrorCode = WSAGetLastError();

           

           if (WSAECONNRESET == *ErrorCode || WSAECONNABORTED == *ErrorCode || WSAESHUTDOWN == *ErrorCode || WSAENETRESET == *ErrorCode)

           {

              bError = 1;

              ReturnCode = RET_SOCKET_SHUT_DOWN;

              goto ErrHand;

           }

           else if (WSAETIMEDOUT == *ErrorCode)

           {

              bError = 1;

              ReturnCode = RET_TIMEOUT;

              goto ErrHand;

           }

           

           bError = 1;

           ReturnCode = RET_FAIL;

           goto ErrHand;

       }

       else if (0 == ResRecv) // socket closed.

       {

           bError = 1;

           ReturnCode = RET_SOCKET_CLOSED;

           goto ErrHand;

       }

       else if (sizeof (LenInfo) > ResRecv)

       {

           if (MAX_RECV_AGAIN <= RecvAgainCount)

           {

              bError = 1;

              ReturnCode = RET_FAIL;

              goto ErrHand;

           }

           RecvAgainCount++;

           goto RecvAgain;

       }

       else if (sizeof (LenInfo) != ResRecv)

       {

           bError = 1;

           ReturnCode = RET_FAIL;

           goto ErrHand;

       }

       else

       {

           memcpy(&RetLen, LenInfo, sizeof (LenInfo));

           if (CHECK_ALIVE_VALUE == RetLen)

           {

              ResRecv = recv(Socket, LenInfo, sizeof (LenInfo), 0); // recv() may return arbitrary value. <- but it can handle the size of data as much as MTU.

              if (SOCKET_ERROR == ResRecv)

              { 

                  *ErrorCode = WSAGetLastError();

                  

                  if (WSAECONNRESET == *ErrorCode || WSAECONNABORTED == *ErrorCode || WSAESHUTDOWN == *ErrorCode || WSAENETRESET == *ErrorCode)

                  {

                     bError = 1;

                     ReturnCode = RET_SOCKET_SHUT_DOWN;

                     goto ErrHand;

                  }

                  else if (WSAETIMEDOUT == *ErrorCode)

                  {

                     bError = 1;

                     ReturnCode = RET_TIMEOUT;

                     goto ErrHand;

                  }

                  

                  bError = 1;

                  ReturnCode = RET_FAIL;

                  goto ErrHand;

              }

              else if (0 == ResRecv) // socket closed.

              {

                  bError = 1;

                  ReturnCode = RET_SOCKET_CLOSED;

                  goto ErrHand;

              }

 

              goto RecvAgainNew;

           }

           else if (0 >= RetLen)

           {

              bError = 1;

              ReturnCode = RET_SOCKET_NO_ORDER;

              goto ErrHand;

           }

           else

           {

              bError = 0;

              ReturnCode = RetLen;

              goto ErrHand;

           }

       }

    }

    else // read the data.

    {

       CopyingSize = 0;

       LoopCount = 0;

       ToReadSize = BufferSize + sizeof (LenInfo);

       while (1)

       {

           if (sizeof (ReadBuff) <= ToReadSize)

           {

              UnitReadSize = sizeof (ReadBuff);

           }

           else

           {

              UnitReadSize = ToReadSize;

           }

           ZeroMemory(ReadBuff, sizeof (ReadBuff));

           pReadingPoint = ReadBuff;

           ResRecv = recv(Socket, pReadingPoint, UnitReadSize, 0);

           if (SOCKET_ERROR == ResRecv)

           { 

              *ErrorCode = WSAGetLastError();

 

              if (WSAECONNRESET == *ErrorCode || WSAECONNABORTED == *ErrorCode || WSAESHUTDOWN == *ErrorCode || WSAENETRESET == *ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET_SOCKET_SHUT_DOWN;

                  goto ErrHand;

              }

              else if (WSAETIMEDOUT == *ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET_TIMEOUT;

                  goto ErrHand;

              }

 

              bError = 1;

              ReturnCode = RET_FAIL;

              goto ErrHand;

           }

           else if (0 == ResRecv) // socket closed.

           {

              bError = 1;

              ReturnCode = RET_SOCKET_CLOSED;

              goto ErrHand;

           }

           else

           {

              if (0 == LoopCount)

              {

                  memcpy(Buffer + CopyingSize, ReadBuff + sizeof (LenInfo), ResRecv - sizeof (LenInfo));

                  CopyingSize += ResRecv - sizeof (LenInfo);

              }

              else

              {

                  memcpy(Buffer + CopyingSize, ReadBuff, ResRecv);

                  CopyingSize += ResRecv;

              }

              LoopCount++;

              ToReadSize -= ResRecv;

 

              if (0 >= ToReadSize)

              {

                  break;

              }

           }

       }

 

       bError = 0;

       ReturnCode = CopyingSize;

       goto ErrHand;

    }

 

ErrHand:

    if (-1 != TimeoutOld)

    {

       Timeout = TimeoutOld;

       if (SOCKET_ERROR == setsockopt(Socket, SOL_SOCKET, SO_RCVTIMEO, (char *)&Timeout, sizeof (Timeout)))

       {

           *ErrorCode = WSAGetLastError();

           bError = 1;

           ReturnCode = RET_FAIL;

           goto ErrHand;

       }

    }

 

    return ReturnCode;

} // TCPRead()

 

int TCPWrite(SOCKET Socket, char *Buffer, DWORD BufferSize, DWORD TimeoutMilli, DWORD *ErrorCode)

{

    BOOL bError;

    int ReturnCode;

    DWORD WritingSize;

    int ResSend;

    int Timeout;

    int TimeoutOld;

    int OutLen;

    int ToSendSize;

    int ToSendSizeUnit;

    int RemainedUnit;

    int Loop;

    int SendingNumber;

    char *pIndex;

    char WriteBuf[WRITE_UNIT_SIZE];

    char *pIndexUnit;

 

    bError = 0;

    ReturnCode = RET_FAIL;

    TimeoutOld = -1;

 

    if (0 > Socket || 0 == Buffer || 0 == BufferSize || 0 == ErrorCode)

    {

       bError = 1;

       ReturnCode = RET_FAIL;

       goto ErrHand;

    }

 

    *ErrorCode = 0;

 

    OutLen = sizeof (TimeoutOld);

    if (SOCKET_ERROR == getsockopt(Socket, SOL_SOCKET, SO_SNDTIMEO, (char *)&TimeoutOld, &OutLen))

    {

       *ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET_FAIL;

       goto ErrHand;

    }

 

    Timeout = TimeoutMilli; // Assigning is due to input the address of the Timeout. 0 = infinite.

    if (SOCKET_ERROR == setsockopt(Socket, SOL_SOCKET, SO_SNDTIMEO, (char *)&Timeout, sizeof (Timeout)))

    {

       *ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET_FAIL;

       goto ErrHand;

    }

 

    SendingNumber = ((BufferSize + sizeof (BufferSize)) / WRITE_UNIT_SIZE) + ((0 != ((BufferSize + sizeof (BufferSize)) % WRITE_UNIT_SIZE)) ? 1 : 0);

    WritingSize = 0;

    pIndex = Buffer;

    ToSendSize = BufferSize;

    for (Loop = 0; Loop < SendingNumber; Loop++)

    {

       if (0 == Loop)

       {

           ZeroMemory(WriteBuf, sizeof (WriteBuf));

           ToSendSizeUnit = ((WRITE_UNIT_SIZE - sizeof (BufferSize)) > ToSendSize) ? ToSendSize : WRITE_UNIT_SIZE - sizeof (BufferSize);

           memcpy(WriteBuf, &BufferSize, sizeof (BufferSize));

           memcpy(WriteBuf + sizeof (BufferSize), pIndex, ToSendSizeUnit);

           pIndex += ToSendSizeUnit;

           ToSendSize -= ToSendSizeUnit;

           ToSendSizeUnit += sizeof (BufferSize); // compensation.

       }

       else

        {

           ZeroMemory(WriteBuf, sizeof (WriteBuf));

           ToSendSizeUnit = (WRITE_UNIT_SIZE > ToSendSize) ? ToSendSize : WRITE_UNIT_SIZE;

           memcpy(WriteBuf, pIndex, ToSendSizeUnit);

           pIndex += ToSendSizeUnit;

           ToSendSize -= ToSendSizeUnit;

       }

 

       RemainedUnit = ToSendSizeUnit;

       pIndexUnit = WriteBuf;

       while (0 < RemainedUnit)

       {

           ResSend = send(Socket, pIndexUnit, RemainedUnit, 0); // send() operates as all or nothing.

           if (SOCKET_ERROR == ResSend)

           { 

              *ErrorCode = WSAGetLastError();

              

              if (WSAECONNRESET == *ErrorCode || WSAECONNABORTED == *ErrorCode || WSAESHUTDOWN == *ErrorCode || WSAENETRESET == *ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET_SOCKET_SHUT_DOWN;

                  goto ErrHand;

              }

              else if (WSAETIMEDOUT == *ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET_TIMEOUT;

                  goto ErrHand;

              }

              

              bError = 1;

              ReturnCode = RET_FAIL;

              goto ErrHand;

           }

           else if (0 == ResSend) // socket closed.

           {

              bError = 1;

              ReturnCode = RET_SOCKET_CLOSED;

              goto ErrHand;

           }

           else if (ResSend == RemainedUnit) // the normal case.

           {

              WritingSize += ResSend;

              RemainedUnit -= ResSend;

           }

           else if (ResSend > RemainedUnit)

           {

              bError = 1;

              ReturnCode = RET_FAIL;

              goto ErrHand;

           }

           else if (ResSend < RemainedUnit)

           {

              WritingSize += ResSend;

              RemainedUnit -= ResSend;

              pIndexUnit += ResSend;

           }

           else // what? error.

           {

              bError = 1;

              ReturnCode = RET_FAIL;

              goto ErrHand;

           }

       }

    }

 

ErrHand:

    if (-1 != TimeoutOld)

    {

       Timeout = TimeoutOld;

       if (SOCKET_ERROR == setsockopt(Socket, SOL_SOCKET, SO_SNDTIMEO, (char *)&Timeout, sizeof (Timeout)))

       {

           *ErrorCode = WSAGetLastError();

           bError = 1;

           ReturnCode = RET_FAIL;

       }

    }

 

    if (1 == bError)

    {

       return ReturnCode;

    }

 

    ReturnCode = WritingSize - sizeof (BufferSize);

    return ReturnCode;

} // TCPWrite()
'''

import win32com.client
class DmFaq:
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
    def FaqCancel(self):
        """
        函数简介:
            可以把上次FaqPost的发送取消,接着下一次FaqPost
        函数原型:
            long FaqCancel()
        返回值:
            整形数:
            0: 失败
            1: 成功
        """
        return self._dm.FaqCancel()

    def FaqCapture(self, x1, y1, x2, y2, quality, delay, time):
        """
        函数简介:
            截取指定范围内的动画或者图像,并返回此句柄
        函数原型:
            long FaqCapture(x1, y1, x2, y2, quality, delay, time)
        参数定义:
            x1 整形数: 左上角X坐标
            y1 整形数: 左上角Y坐标
            x2 整形数: 右下角X坐标
            y2 整形数: 右下角Y坐标
            quality 整形数: 图像或动画品质,取值范围(1-100或者250) 当此值为250时,会截取无损bmp图像数据
            delay 整形数: 截取动画时用,表示相隔两帧间的时间间隔,单位毫秒 (如果只是截取静态图像,这个参数必须是0)
            time 整形数: 表示总共截取多久的动画,单位毫秒 (如果只是截取静态图像,这个参数必须是0)
        返回值:
            整形数: 图像或者动画句柄
        """
        return self._dm.FaqCapture(x1, y1, x2, y2, quality, delay, time)

    def FaqCaptureFromFile(self, x1, y1, x2, y2, file, quality):
        """
        函数简介:
            截取指定图片中的图像,并返回此句柄
        函数原型:
            long FaqCaptureFromFile(x1, y1, x2, y2, file, quality)
        参数定义:
            x1 整形数: 左上角X坐标
            y1 整形数: 左上角Y坐标
            x2 整形数: 右下角X坐标
            y2 整形数: 右下角Y坐标
            file 字符串: 图片文件名,图像格式基本都支持
            quality 整形数: 图像品质,取值范围(1-100或者250) 当此值为250时,会截取无损bmp图像数据
        返回值:
            整形数: 图像句柄
        """
        return self._dm.FaqCaptureFromFile(x1, y1, x2, y2, file, quality)

    def FaqCaptureString(self, str_content):
        """
        函数简介:
            从给定的字符串获取此句柄 (此接口必须配合答题器v30以后的版本)
        函数原型:
            long FaqCaptureString(str)
        参数定义:
            str 字符串: 文字类型的问题
        返回值:
            整形数: 文字句柄
        """
        return self._dm.FaqCaptureString(str_content)

    def FaqFetch(self):
        """
        函数简介:
            获取由FaqPost发送后,由服务器返回的答案
        函数原型:
            string FaqFetch()
        返回值:
            字符串:
            如果此函数调用失败,返回"Error:错误描述"
            如果函数调用成功,返回"OK:答案"
            根据FaqPost中 request_type取值的不同,返回值不同:
            0: 答案格式为"x,y"
            1: 答案格式为"1" "2" "3" "4" "5" "6"
            2: 答案就是要求的答案如"李白"
            3: 答案格式为"x1,y1|..|xn,yn"
            如果返回空字符串,表示FaqPost还未处理完毕,或者没有调用过FaqPost
        """
        return self._dm.FaqFetch()

    def FaqGetSize(self, handle):
        """
        函数简介:
            获取句柄所对应的数据包的大小,单位是字节
        函数原型:
            long FaqGetSize(handle)
        参数定义:
            handle 整形数: 由FaqCapture返回的句柄
        返回值:
            整形数: 数据包大小
        """
        return self._dm.FaqGetSize(handle)

    def FaqIsPosted(self):
        """
        函数简介:
            用于判断当前对象是否有发送过答题(FaqPost)
        函数原型:
            long FaqIsPosted()
        返回值:
            整形数:
            0: 没有
            1: 有发送过
        """
        return self._dm.FaqIsPosted()

    def FaqPost(self, server, handle, request_type, time_out):
        """
        函数简介:
            发送指定的图像句柄到指定的服务器,并立即返回(异步操作)
        函数原型:
            long FaqPost(server, handle, request_type, time_out)
        参数定义:
            server 字符串: 服务器地址以及端口,格式为(ip:port),例如"192.168.1.100:12345"
            handle 整形数: 由FaqCapture获取到的句柄
            request_type 整形数: 取值定义如下
                0: 要求获取坐标
                1: 要求获取选项,比如(ABCDE)
                2: 要求获取文字答案
                3: 要求获取N个坐标
            time_out 整形数: 表示等待多久,单位是毫秒
        返回值:
            整形数:
            0: 失败,一般情况下是由于上个FaqPost还没有处理完毕(服务器还没返回)
            1: 成功
        """
        return self._dm.FaqPost(server, handle, request_type, time_out)

    def FaqSend(self, server, handle, request_type, time_out):
        """
        函数简介:
            发送指定的图像句柄到指定的服务器,并等待返回结果(同步等待)
        函数原型:
            string FaqSend(server, handle, request_type, time_out)
        参数定义:
            server 字符串: 服务器地址以及端口,格式为(ip:port),例如"192.168.1.100:12345"
            handle 整形数: 由FaqCapture获取到的句柄
            request_type 整形数: 取值定义如下
                0: 要求获取坐标
                1: 要求获取选项,比如(ABCDE)
                2: 要求获取文字答案
                3: 要求获取N个坐标
            time_out 整形数: 表示等待多久,单位是毫秒
        返回值:
            字符串:
            如果此函数调用失败,返回"Error:错误描述"
            如果函数调用成功,返回"OK:答案"
            根据request_type取值的不同,返回值不同:
            0: 答案格式为"x,y"
            1: 答案格式为"1" "2" "3" "4" "5" "6"
            2: 答案就是要求的答案如"李白"
            3: 答案格式为"x1,y1|..|xn,yn"
        """
        return self._dm.FaqSend(server, handle, request_type, time_out)

    # 中文别名
    取消答题 = FaqCancel
    截取动画 = FaqCapture
    从文件截取图像 = FaqCaptureFromFile
    获取文字句柄 = FaqCaptureString
    获取答题结果 = FaqFetch
    获取数据包大小 = FaqGetSize
    是否已发送答题 = FaqIsPosted
    发送答题 = FaqPost
    同步发送答题 = FaqSend 