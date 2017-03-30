# -*- coding: cp949 -*-
from ctypes import *


#ctypes 형태의 타입을 MS 타입으로 매핑
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
HANDLE = c_void_p
LONG = c_long

###########dwContinueStatus######
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
DBG_REPLY_LATER = 0x40010001
#################################

#상수
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010
INFINITE              = 0xFFFFFFFF


#DEBUG_EVNET_IMM
EXCEPTION_DEBUG_EVENT = 0x1
CREATE_THREAD_DEBUG_EVENT = 0x2
CREATE_PROCESS_DEBUG_EVENT = 0x3
EXIT_THREAD_DEBUG_EVENT =   0x4
EXIT_PROCESS_DEBUG_EVENT = 0x5
LOAD_DLL_DEBUG_EVENT = 0x6
UNLOAD_DLL_DEBUG_EVENT = 0x7
OUPUT_DEBUG_STRING_EVENT = 0x8
RIP_EVENT = 0x9

#CreateProcess Struct

class STARTUPINFO(Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPTSTR),
        ("lpDesktop", LPTSTR),
        ("lpTitle", LPTSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAtribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput",  HANDLE),
        ("hStdError", HANDLE),
        ]
    
    
class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hprocess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
        ]



class EXCEPTION_RECORD(Structure):
    pass

EXCEPTION_RECORD.fields = [
        ("ExceptionCode", DWORD),
        ("ExceptionFlags", DWORD),
        ("ExceptionRecord",POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",c_void_p),
        ("NumberParameters", DWORD),
        ("ExceptionInformation[EXCEPTION_MAXIMUM_PARAMETERS]", c_ulong),
        ]


class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD),
        ("dwFirstChance", DWORD),
        ]



class DEBUG_EVENT_UNION(Union):
    _fields_ = [
        ("Exceptioin",EXCEPTION_DEBUG_INFO),
        #("CreateThread", )

        ]




class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode",DWORD),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
        ("u", DEBUG_EVENT_UNION)        
        ]
