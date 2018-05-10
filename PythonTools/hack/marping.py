import subprocess
import sys
import time
from threading import Thread

def arping(ip):
    try:
        subprocess.check_output('arping -c 1 '+str(ip), shell=True)
        time.sleep(0.1)
        print ip,"is alive"
        return
    except:
        return

def main():
    host = str(sys.argv[1]).strip()
    addrs = host.split(".")
    ip = addrs[0] +"."+ addrs[1] +"."+ addrs[2]
    for i in range(1,255):
        ip = addr+str(i)
        t = Thread(target=arping, args=(ip,))
        t.start()

if __name__=='__main__':
    main()
