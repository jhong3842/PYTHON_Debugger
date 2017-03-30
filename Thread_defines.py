# -*- coding: cp949 -*-
from ctypes import *


#ctypes 형태의 타입을 MS 타입으로 매핑
BYTE = c_ubyte
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
HANDLE = c_void_p
ULONG = c_ulong

######################
THREAD_GET_CONTEXT = 0x8

THREAD_IMPERSONATE = 0x100

THREAD_QUERY_INFORMATION = 0x40

THREAD_QUERY_LIMITED_INFORMATION = 0x800

THREAD_SET_CONTEXT = 0x10

THREAD_SET_INFORMATION = 0x20

THREAD_SET_LIMITED_INFORMATION =0x400

THREAD_SET_THREAD_TOKEN = 0x80

THREAD_SUSPEND_RESUME = 0x2

THREAD_TERMINATE = 0x1
########################

#############SNAPSHOT#################
TH32CS_SNAPHEAPLIST = 0x00000001

TH32CS_SNAPPROCESS  = 0x00000002

TH32CS_SNAPTHREAD   = 0x00000004

TH32CS_SNAPMODULE   = 0x00000008

TH32CS_INHERIT      = 0x80000000

#######################################

#OpenThread 
THREAD_ALL_ACCESS   = 0x001F03FF

# Context flags for GetThreadContext()

CONTEXT_FULL                   = 0x00010007

CONTEXT_DEBUG_REGISTERS        = 0x00010010

#Thread Structure
class THREADENTRY32(Structure):
    _fields_ =[
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ThreadID", DWORD),
        ("th32OwnerProcessID",DWORD),
        ("tpBasePri",DWORD),
        ("tpDeltaPri",DWORD),
        ("dwFlags", DWORD)
        ]
    
class _FLOATING_SAVE_AREA(Structure):
    _fields_ = [
        ("ControlWorld", c_ulong),
        ("StatusWord",  c_ulong),
        ("TagWord" , c_ulong),
        ("ErrorOffset", c_ulong),
        ("ErrorSelector",c_ulong),
        ("DataOffset", c_ulong),
        ("DataSelector" , c_ulong),
        ("RegisterArea", c_ubyte * 80),
        ("Cr0NpxState", c_ulong),
        ]

class CONTEXT(Structure):
    _pack_ = 1
    _fields_ =[
        ("ContextFlags", DWORD),
        ("Dr0", DWORD),
        ("Dr1", DWORD),
        ("Dr2", DWORD),
        ("Dr3", DWORD),
        ("Dr6", DWORD),
        ("Dr7", DWORD),
        ("FloatSave", _FLOATING_SAVE_AREA) ,
        ("SegGs",DWORD),
        ("SegFs",DWORD),
        ("SegEs",DWORD),
        ("SegEs",DWORD),
        ("SegDs",DWORD),
        ("Edi",DWORD),
        ("Esi", DWORD ),
        ("Ebx" , DWORD),
        ("Edx" , DWORD),
        ("Ecx" , DWORD),
        ("Eax" , DWORD),
        ("Ebp" , DWORD),
        ("Eip" , DWORD),
        ("SegCs", DWORD),
        ("EFlags", DWORD),
        ("Esp" , DWORD),
        ("SegSs", DWORD),
        ("ExtendedRegisters", BYTE * 512),
        ]







    
