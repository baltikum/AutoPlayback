import logging
import traceback
from onvif import ONVIFCamera
from datetime import datetime







"""






#Satta uppgifter
Manufacturer = 'Not available'
Model = 'Not available'
FirmwareVersion = 'XXXX'
SerialNumber = 'XXXX'


Hostname = 'Unnamed'
NTPServer = '0.0.0.0'
Date_set = {
            'Year': 0,
            'Month': 0,
            'Day': 0
        }
Time_set = {
            'Hour': 0,
            'Minute': 0,
            'Second': 0
        }
AllowedIP = []







#Initiera onvif instans
kamera = ONVIFCamera(camera_address,port,username,password,wsdl_dir="/home/baltikum/WebCv2/venv/lib/python3.8/site-packages/wsdl")
#device management instans på aktuell kamera
kamera_management = kamera.create_devicemgmt_service()
"""


"""
kamera_event = kamera.create_events_service()

response = kamera_event.GetEventProperties()
print('------------')
print(str(response))

#kamera_event.CreatePullPointSubscription()
#print(str(hej))
pullpoint = kamera.create_pullpoint_service()
print('------------')
#print(str(pullpoint))
pullpointsubscription = kamera_event.CreatePullPointSubscription()
print('------------')
print(str(pullpointsubscription))

req = response.

#req = pullpoint.create_type('PullMessages') # Exception: No element 'PullMessages' in namespace http://docs.oasis-open.org/wsrf/rw-2. Available elements are:  - 
#req.MessageLimit=100
#print(pullpoint.PullMessages(req))

"""
PORT = '80'

#Camera object for each camera.
class Camera():
    def __init__( self, camera_address ,camera_name ,username, password, settings,
                    system_host, system_gw, system_ntp ):

        self.status = False
        self.camera_address = camera_address
        self.camera_name = camera_name
        self.username = username
        self.password = password
        self.settings = settings
        self.system_host = system_host
        self.system_gw = system_gw
        self.system_ntp = system_ntp
        self.camera = ''
        self.camera_management = ''
        self.url = ''


    #Initiate configuratin of device hardware
    def configure_camera(self):
        try:
            

            self.camera = ONVIFCamera(self.camera_address,'80',self.username,self.password,wsdl_dir="/home/pi/python-onvif-zeep/wsdl")
            self.camera_management = self.camera.create_devicemgmt_service()
            self.status = True
            self.camera_name = self.set_hostname(self.camera_name)
            self.device_info = self.get_device_info()
            self.system_gw = self.set_gateway(self.system_gw)
            self.date_set = ''
            self.time_set = ''
            self.set_device_date_and_time()
            self.NTPServer = self.set_ntp_server(self.system_ntp)
            self.allowedIP = []
            self.configure_ip_filtering(self.system_host)
            
            self.create_streaming_profile()
            self.url = self.get_streaming_url()

            logging.info('Initiation complete')
            del self.camera_management
            logging.info('Removed management instance')
        except:
            traceback.print_exc()

    #Set hostname
    def set_hostname(self,hostname):
        try:
            setHostname = self.camera_management.create_type('SetHostname')
            setHostname.Name = hostname
            self.camera_management.SetHostname(setHostname)
            self.hostname = self.camera_management.GetHostname().Name
            logging.info(f'Hostname set to {self.hostname}')
            return str(self.hostname)
        except:
            logging.debug('Failed to set hostname')
            return "{'Exception': Failed to set hostname }"

    #Fetch device information
    def get_device_info(self):
        try:
            self.device_info = self.camera_management.GetDeviceInformation()
            logging.info(f'Device information {self.device_info}')
            return str(self.device_info)
        except:
            logging.debug('Failed to retrieve device information')
            return "{'Exception': Failed to retrieve device information}"

    #Set default gateway
    def set_gateway(self,camera_gateway):
        try:
            setGateway = self.camera_management.create_type('SetNetworkDefaultGateway')
            setGateway.IPv4Address = camera_gateway
            self.camera_management.SetNetworkDefaultGateway(setGateway)
            self.Gateway_set = self.camera_management.GetNetworkDefaultGateway().IPv4Address
            logging.info(f'Default gateway {self.Gateway_set}')
            return f'Default gateway {self.Gateway_set}'
        except:
            logging.debug('Failed to set Default gateway')
            return "{'Exception' : Failed to set Default gateway }"

    #Set NTP Server
    def set_ntp_server(self,ntp_server):
        try:
            setNTP = self.camera_management.create_type('SetNTP')
            setNTP.FromDHCP = False
            setNTP.NTPManual = [{'Type': 'IPv4','IPv4Address': ntp_server}]
            self.camera_management.SetNTP(setNTP)
            self.NTPServer = self.camera_management.GetNTP().NTPManual[0].IPv4Address
            logging.info(f'NTP server was set to {self.NTPServer}')
            return str(self.NTPServer)
        except:
            logging.info('Failed to set NTP server')
            return "{'Exception': Failed to set NTP Server}" 

    #Set devicedate and time
    def set_device_date_and_time(self):
        try:
            setCameraSystemTime = self.camera_management.create_type('SetSystemDateAndTime')
            setCameraSystemTime.DateTimeType = 'NTP'
            setCameraSystemTime.DaylightSavings = False
            setCameraSystemTime.TimeZone = {'TZ': 'CET-1CEST,M3.5.0,M10.5.0/3'}
            now = datetime.now()
            year = int(now.year)
            month = int(now.month)
            day = int(now.day)
            hour = int(now.hour)
            minute = int(now.minute)
            second = int (now.second)
            setCameraSystemTime.UTCDateTime = {
                    'Time': {
                        'Hour': hour,
                        'Minute': minute,
                        'Second': second
                    },
                    'Date': {
                        'Year': year,
                        'Month': month,
                        'Day': day
                    }
                }
            self.camera_management.SetSystemDateAndTime(setCameraSystemTime)
            self.date_set = self.camera_management.GetSystemDateAndTime().UTCDateTime.Date
            self.time_set = self.camera_management.GetSystemDateAndTime().UTCDateTime.Time
            logging.info(f'Date is set to {self.date_set.Year}/{self.date_set.Month}/{self.date_set.Day}' )
            logging.info(f'Time is set to {self.time_set.Hour}:{self.time_set.Minute}:{self.time_set.Second}' )
            return f'{self.date_set}{self.time_set}'
        except:
            logging.info('Failed to set date and time on device')
            return "{'Exception': Failed to set date and time on device }" 

    #Configure IP Filtering list
    def configure_ip_filtering(self,host_address):
        try:
            setIPAddressFilter = self.camera_management.create_type('AddIPAddressFilter')
            setIPAddressFilter.IPAddressFilter = {
                'Type':'Allow', 
                'IPv4Address': 
                    [
                        {
                            'Address': host_address,
                            'PrefixLength': 32
                        },
                        {
                            'Address': get_ip(),
                            'PrefixLength': 32
                        }
                    ]
            }       
            self.camera_management.SetIPAddressFilter(setIPAddressFilter)
            temp = self.camera_management.GetIPAddressFilter().IPv4Address
            for entry in temp:
                self.allowedIP.append(entry)
            logging.info(f'Allowed hosts are {self.allowedIP}')
            return f'Allowed hosts are {self.allowedIP}'
        except:
            logging.debug('Failed to set ip filtering')
            return "{'Exception' : Failed to set ip filtering }"

    #Fetch sreaming URL
    def get_streaming_url(self):
        media_service = self.camera.create_media_service()
        uri = media_service.GetStreamUri(
            {
                'StreamSetup':
                    {   
                        'Stream' : 'RTP-Unicast',
                        'Transport' : { 'Protocol' : 'UDP' } 
                    }, 
                'ProfileToken': media_service.GetProfiles()[0].token
            })
        return str(uri.Uri)

    def create_streaming_profile(self):
        try:
            media_service = self.camera.create_media_service()

            profile = media_service.GetProfiles()[1]

            profmall = media_service.create_type('CreateProfile')
            
            profmall.Name = 'autop_264'
            profmall.Token = 'autop_264'
            print(profmall)

            #resp = media_service.CreateProfile(profmall)
            #print(resp)

            print(self.camera.create_events_service().GetEventProperties())
            


            return ''
        except:
            traceback.print_exc()
