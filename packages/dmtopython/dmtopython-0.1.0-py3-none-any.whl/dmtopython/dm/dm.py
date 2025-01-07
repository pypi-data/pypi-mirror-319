#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
大漠插件API完整封装
'''

import win32com.client
from .dm_ai import DmAi
from .dm_mouse import DmMouse
from .dm_keyboard import DmKeyboard
from .dm_window import DmWindow
from .dm_foobar import DmFoobar
from .dm_memory import DmMemory
from .dm_system import DmSystem
from .dm_ocr import DmOcr
from .dm_file import DmFile
from .dm_find import DmFind
from .dm_bg import DmBg

class DmSoft:
    def __init__(self,code,key):
        self._dm = None
        self.ai = None
        self.mouse = None
        self.keyboard = None
        self.window = None
        self.footbar = None
        self.memory = None
        self.system = None
        self.ocr = None
        self.file = None
        self.find = None
        self.bg = None
        self.code = code
        self.key = key

    def _check_dm(self):
        if not self._dm:
            raise Exception("未初始化 DM 对象,请先调用 create_dm()")

    def create_dm(self):
        """
        创建大漠对象
        """
        try:
            self._dm = win32com.client.Dispatch('dm.dmsoft')
  
            self.ai = DmAi(self._dm)
            self.mouse = DmMouse(self._dm)
            self.keyboard = DmKeyboard(self._dm)
            self.window = DmWindow(self._dm)
            self.footbar = DmFoobar(self._dm)
            self.memory = DmMemory(self._dm)
            self.system = DmSystem(self._dm)
            self.ocr = DmOcr(self._dm)
            self.file = DmFile(self._dm)
            self.find = DmFind(self._dm)
            self.bg = DmBg(self._dm)
            self.regstats=self._dm.Reg(self.code,self.key)
            if(self.regstats==1):
                return 1
            else:
                return self.regstats
        except Exception as e:
            print(f"Error creating DM object: {str(e)}")
            return 0

    def get_dm_count(self):
        """获取大漠对象个数"""
        try:
            self._check_dm()
            return self._dm.GetDmCount()
        except Exception as e:
            print(f"Error in get_dm_count: {str(e)}")
            return 0 
    def close(self):
        """关闭大漠对象"""
        try:
            self._check_dm()
            self._dm.UnBindWindow()
        except Exception as e:
            print(f"Error in close: {str(e)}")
