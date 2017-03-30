# -*- coding: cp949 -*-
from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    #초기화용 변수
    def __init__(self):
        self.h_process = None   #프로세스 헨들
        self.pid    = None      # 프로세스 pid
        self.debugger_active    = False     #디버거 동작 유무
        pass

    def load(self, path_to_exe):
        #프로세스를 생성 할 때, 디버기 형태로 생성할 것인가
        #설정 CREATE_NEW_CONSOLE flag는 새창
        creation_flags = CREATE_NEW_CONSOLE

        #Struct to Object
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        #프로세스가 독릭접으로 실행되게
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        #cb 자신의 구조체 크기를 넣어줌
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print "[*] Launced the process!"
            print "[*] PID : %d " % process_information.dwProcessId

        else:
            print "[*]Error : 0x08x." % kernel32.GetLastError()

        
