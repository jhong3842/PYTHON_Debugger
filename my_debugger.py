# -*- coding: cp949 -*-
from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    #�ʱ�ȭ�� ����
    def __init__(self):
        self.h_process = None   #���μ��� ���
        self.pid    = None      # ���μ��� pid
        self.debugger_active    = False     #����� ���� ����
        pass

    def load(self, path_to_exe):
        #���μ����� ���� �� ��, ����� ���·� ������ ���ΰ�
        #���� CREATE_NEW_CONSOLE flag�� ��â
        creation_flags = CREATE_NEW_CONSOLE

        #Struct to Object
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        #���μ����� ���������� ����ǰ�
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        #cb �ڽ��� ����ü ũ�⸦ �־���
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

        
