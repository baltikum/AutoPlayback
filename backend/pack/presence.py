import pickletools
import subprocess
from time import sleep
import cec,requests

class Presence():
    def __init__(self,mac,period,device_id=0):
        self.mac = mac
        self.period = period
        self.device_id = device_id
        self.device = False
        self.full_command
        
        MAC = '72:85:fd:64:a4:87' 
        self.mac = []
        self.mac.append(MAC)
        period = 10
      
      
      
    def configure_presence(self):
        full_command = f"arp-scan -l | grep " 
        length = len(self.mac)-1
        i = 0
        for entry in self.mac:
            add_arg = f"{entry}"
            i += 1
            if i == length:
                break
            add_pipe = "\|"
            
        self.full_command = full_command
        return True

    def run_presence(self):
            
        cec.init()
        self.device = cec.Device(0)
        
        while True:
            p = subprocess.Popen(self.full_command, stdout=subprocess.PIPE, shell=True)
            
            output, err = p.communicate()
            p_status = p.wait()
            
            if output:


                url = 'http://localhost:5000/presence/1'
                load = {'presence': 'active'}
                _res = requests.post(url, data = load)

                print('Online')
                cec.init()
                self.device = cec.Device(0)
                self.device.power_on()
                cec.set_active_source()

                self.period = 480
            else:
                print('Offline')
                cec.init()
                self.device = cec.Device(0)
                self.device.standby()
                self.period = 10
                
            sleep(self.period)