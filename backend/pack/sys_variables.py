import json,os

class Sys_variables():
      def __init__(self):
            with open('./pack/system_settings.ini', 'r' ) as file:
                  jsonData = file.read()
            sys_config = json.loads(jsonData)
            sys_config = sys_config.get('system_config')

            self.SYSTEM_HOST = sys_config.get('system_ip')
            self.FLASK_PORT = sys_config.get('flask_port')
            self.SYSTEM_GW = sys_config.get('system_gw')
            self.SYSTEM_NTP = sys_config.get('system_ntp')
            self.cameras_configured = sys_config.get('cameras_configured')

            


