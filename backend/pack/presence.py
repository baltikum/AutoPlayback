#import pickletools
import errno
import subprocess
from time import sleep
import cec,requests,traceback,logging

class Presence():
    def __init__(self,mac,period,device_id=0):
        self.period = period
        self.device_id = device_id
        self.device = False
        self.full_command = ''
        self.mac = []
        self.mac.append(mac)

    def __repr__(self):
        return f'{self.mac}'

    def configure_presence(self):
        trace = ''
        command = []
        try:
            command.append("sudo arp-scan -l -r 5 | grep ")

            for index, entry in enumerate(self.mac):
                command.append(f"'{entry}'")
                if index == (len(self.mac)-1):
                    break
                command.append("\|")

            self.full_command = ''.join(command)
            res = True
        except:
            res = False
            trace = traceback.format_exc()
        return res, trace

    def run_presence(self):

        #cec.init()
        #self.device = cec.Device(0)
        sleep(2)

        previous = False
        message = True
        count = 0
        while True:
            try:
                p = subprocess.Popen(self.full_command, stdout=subprocess.PIPE, shell=True)

                output, err = p.communicate()
                p_status = p.wait()

                if output:

                    count = 0
                    if previous != output:
                        previous = output

                        header = { "Content-Type" : "application/json" }
                        url = 'http://localhost:5000/presence'
                        load = '{ "presence" : "active" }'
                        _res = requests.post(url, headers=header, data = load)

                        print(f'Status:[Online] for {output}')
                        try:
                            cec.init()
                            self.device = cec.Device(0)
                            self.device.power_on()
                            cec.set_active_source()
                            p = subprocess.Popen('firefox http://localhost:3000/playback & sleep 5 && xdotool key F11', stdout=subprocess.PIPE, shell=True)

                        except:
                            logging.error('Connect a compatible hdmi device')



                    #self.period = 30
                else:

                    count += 1
                    if count > 2:
                        count = 0
                        print('Status:[Offline]')
                        if previous != output:
                            previous = output
                            header = { "Content-Type" : "application/json" }
                            url = 'http://localhost:5000/presence'
                            load = '{ "presence" : "inactive" }'
                            _res = requests.post(url, headers=header, data = load)
                            try:
                                cec.init()
                                self.device = cec.Device(0)
                                self.device.standby()
                                self.period = 3
                                p = subprocess.Popen('pkill -f firefox', stdout=subprocess.PIPE, shell=True)

                            except:
                                logging.error('Connect a compatible hdmi device')

                sleep(self.period) #self.period
            except:
                traceback.print_exc()

if __name__ == '__main__' :
    #Presence controller thread
    pre = Presence('72:85:fd:64:a4:87', 1)
    res, trace = pre.configure_presence()
    pre.run_presence()
