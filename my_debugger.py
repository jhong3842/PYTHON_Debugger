# -*- coding: cp949 -*-
from ctypes import *
from my_debugger_defines import *
from _multiprocessing import *
from Thread_defines import *

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
        #프로세스 정보 
        process_information = PROCESS_INFORMATION()

        #프로세스가 독릭접으로 실행되게
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        #cb 자신의 구조체 크기를 넣어줌
        startupinfo.cb = sizeof(startupinfo)
        print sizeof(startupinfo)
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

        #생성된 프로세스 핸들 저장
        self.pid = process_information.dwProcessId
        self.h_process = self.open_process(process_information.dwProcessId)
        
    #Get the handle of pid
    def open_process(self,pid):

        h_process = kernel32.OpenProcess(win32.PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        print "[*] PID : %d" % int(pid)
        #Change Controls of Debuggi to Debugger
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
        else:
            error = kernel32.GetLastError()
            print "[*] Unable to attach to the process %d" % error

    def run(self):
        #Debugger run
        while self.debugger_active == True:
            print "run"
            self.get_debug_event()


    def get_debug_event(self):

        #Debug Event Handler Pointer Structure
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        #Not yet, Writing Code to handle Debug Event

        
        #Waiting occuring Debug Evnet
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            raw_input("Press a key to continue...")
            self.debugger_active = False
            kernel32.ContinueDebugEvent(\
                debug_event.dwProcessId,\
                debug_event.dwThreadId,\
                continue_status)


    def detach(self):
        #디버거에서 디버기 분리
        if kernel32.DebugActiveProcessStop(self.pid):
            print "[*] Finished debugging. Exiting..."
            return True
        else:
            print "There was an error"
            return False


    #Gathering Thread ID , including process
    def enumerate_threads(self):
        print "[*] Getting Thread List"
        #Entry Object
        thread_entry = THREADENTRY32()
        
        #list thread
        list_thread = []
        
        #Curent Thread Snapshot
        hThread= kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)
        #hTread Get
        if hThread :
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(hThread, byref(thread_entry))      
            
            while success:
                #프로세스에 해당하는 Thread 찾기
                if thread_entry.th32OwnerProcessID == self.pid:
                    #맞으면 리스트 추가
                    list_thread.append(thread_entry.th32ThreadID)
                    #다음 쓰레드
                success = kernel32.Thread32Next(hThread, byref(thread_entry))
                
            
            kernel32.CloseHandle(hThread)
            return list_thread
        else:
            return False
        

    #Getthe Thread Handle using thread id
    def open_thread(self, thread_id):

        hThread = kernel32.OpenThread(THREAD_ALL_ACCESS, None ,thread_id)
        if hThread is not None:
            return hThread

        else:
            print "[*] Could not obtaion a valid thread handle"


    def get_thread_context(self, thread_id):
        
        #context 구조체 할당
        context = CONTEXT();
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        #쓰레드의 핸들을 가지고 옴.
        hThread = self.open_thread(thread_id)
    
        #쓰레드의 문맥을 가지고
        if kernel32.GetThreadContext(hThread, byref(context)):
            kernel32.CloseHandle(hThread)
            return context
        else:
            return False
        
    def error(self):
        print "GetLastError %08x" % kernel32.GetLastError()        









    
