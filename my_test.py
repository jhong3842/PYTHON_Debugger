import my_debugger

debugger = my_debugger.debugger()

#debugger.load("C:\\Windows\\System32\\calc.exe")

pid = raw_input("Enter the PID of the process to attach to: ")


#Attach Process 
debugger.attach(int(pid))


