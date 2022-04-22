import pickletools
import subprocess
from time import sleep
import cec



MAC = '72:85:fd:64:a4:87'

res = cec.init()
pi = cec.Device(0)
while True:
    sleep(1)
    p = subprocess.Popen(f"arp-scan -l | grep {MAC}", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    if output:
        print('Online')
        pi.power_on()
        cec.set_active_source()
    else:
        print('Offline')
        pi.standby()