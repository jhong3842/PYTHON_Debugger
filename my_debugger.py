# -*- coding: cp949 -*-
from ctypes import *
from my_debugger_defines import *
from _multiprocessing import *



kernel32 = windll.kernel32

    
class debugger():
    #�ʱ�ȭ�� ����
    def __init__(self):
        self.h_process = None   #���μ��� ���
        self.pid    = None      # ���μ��� pid
        self.debugger_active    = False     #����� ���� ����      
        self.h_thread = None    #���μ����� ������
        self.context = None     #������ ����
        pass

    def load(self, path_to_exe):
        #���μ����� ���� �� ��, ����� ���·� ������ ���ΰ�
        #���� CREATE_NEW_CONSOLE flag�� ��â
        creation_flags = CREATE_NEW_CONSOLE | DEBUG_PROCESS

        #Struct to Object
        startupinfo = STARTUPINFO()
        #���μ��� ���� 
        process_information = PROCESS_INFORMATION()

        #���μ����� ���������� ����ǰ�
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        #cb �ڽ��� ����ü ũ�⸦ �־���
        startupinfo.cb = sizeof(startupinfo)
        
        if kernel32.CreateProcessA(path_to_exe, # process path
                                   None,        # parameter
                                   None,        # process security
                                   None,        # thread security
                                   None,        # enable handle inherite
                                   creation_flags, 
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print "[*] Launced the process!"
            print "[*] PID : %d " % process_information.dwProcessId

        else:
            print "[*]Error : 0x08x." % kernel32.GetLastError()

        #pid ����
        self.pid = process_information.dwProcessId
        #handle ����
        self.h_process = self.open_process(process_information.dwProcessId)

        
    #Get the handle of pid
    def open_process(self,pid):
        h_process = kernel32.OpenProcess(win32.PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        print "[*] PID : %d" % int(pid)
        #Change Controls of Debuggi to Debugger
        if kernel32.DebugActiveProcess(self.pid):
            self.debugger_active = True
            self.pid = int(pid)
        else:
            error = kernel32.GetLastError()
            print "[*] Unable to attach to the process %d" % error

    def run(self):
        #Debugger run
        while self.debugger_active == True:
            self.get_debug_event()


    def get_debug_event(self):

        #Debug Event Handler Pointer Structure
        debug_event = DEBUG_EVENT()
    
        #Not yet, Writing Code to handle Debug Event

        
        #Waiting occuring Debug Evnet
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            
            #����� �̺�Ʈ�� �߻��ϸ� debug_event�� ���� Ȯ��
            self.h_thread = self.open_thread(debug_event.dwThreadId)

            #�ռ� ���� thread handle�� �̿��ؼ� context get
            self.context = self.get_thread_context(self.h_thread)

            #print "Event Code : %d Thread Id : %d" %\
            #(debug_event.dwDebugEventCode, debug_event.dwThreadId)
            


            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                print "����ó�� ��ƾ"

            elif debug_event.dwDebugEventCode == CREATE_THREAD_DEBUG_EVENT:
                print "CREATE_THREAD"

            elif debug_event.dwDebugEventCode == CREATE_PROCESS_DEBUG_EVENT:
                print "CREATE_PROCESS"
                

            elif debug_event.dwDebugEventCode == EXIT_THREAD_DEBUG_EVENT:
                print "EXIT_THREAD"

            elif debug_event.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT:
                print "EXIT_PROCESS"
                exit(0)
                
            elif debug_event.dwDebugEventCode == LOAD_DLL_DEBUG_EVENT:
                print "LOAD_DLL"

            elif debug_event.dwDebugEventCode == UNLOAD_DLL_DEBUG_EVENT:
                print "UNLOAD_DLL"

            elif debug_event.dwDebugEventCode == OUTPUT_DEBUG_STRING_EVENT:
                print "OUTPUT_DEBUG_STRING_EVENT"

            elif debug_event.dwDebugEventCode == RIP_EVENT:
                print "RIP_EVENT"

                
            kernel32.ContinueDebugEvent(debug_event.dwProcessId,\
                debug_event.dwThreadId,\
                DBG_CONTINUE)


    def detach(self):
        #����ſ��� ����� �и�
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
                #���μ����� �ش��ϴ� Thread ã��
                if thread_entry.th32OwnerProcessID == self.pid:
                    #������ ����Ʈ �߰�
                    list_thread.append(thread_entry.th32ThreadID)
                    #���� ������
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
        
        #context ����ü �Ҵ�
        context = CONTEXT();
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        #�������� �ڵ��� ������ ��.
        hThread = self.open_thread(thread_id)
    
        #�������� ������ ������
        if kernel32.GetThreadContext(hThread, byref(context)):
            kernel32.CloseHandle(hThread)
            return context
        else:
            return False
        
    def error(self):
        print "GetLastError %08x" % kernel32.GetLastError()        









    
