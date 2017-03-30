import my_debugger

debugger = my_debugger.debugger()

debugger.load("C:\\Windows\\System32\\calc.exe")
#pid = raw_input("Input PID : ")

debugger.attach(debugger.pid)

thread_list = debugger.enumerate_threads()

for thread in thread_list:

    thread_context = debugger.get_thread_context(thread)

    print "[*] Thread id 0x%08x" % thread
    print "[**] EIP : 0x%08x" % thread_context.Eip
    print "[**] ESP : 0x%08x" % thread_context.Esp
    print "[**] EBP : 0x%08x" % thread_context.Ebp
    print "[**] EAX : 0x%08x" % thread_context.Eax
    print "[**] EBX : 0x%08x" % thread_context.Ebx
    print "[**] ECX : 0x%08x" % thread_context.Ecx
    print "[**] EDX : 0x%08x" % thread_context.Edx
    
    
debugger.run()
