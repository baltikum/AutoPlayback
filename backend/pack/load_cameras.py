import json, logging
from pack.camera import Camera

class Load_Cameras():
      def _init__(self, SYSTEM_SETTINGS):
                  try:
                        with open('camera_configurations.ini', 'r') as file:
                              jsonData = file.read()
                        
                        json_cameras = json.loads(jsonData)
                        list_of_cameras = json_cameras['cameras']
                  
                        configured_cameras = []
                        for entry in list_of_cameras:
                              configured_cameras.append(Camera(int(entry.get('id')), entry.get('ip'), entry.get('name'), entry.get('username'),
                                                            entry.get('password'),entry.get('settings'),SYSTEM_SETTINGS.SYSTEM_HOST,
                                                            SYSTEM_SETTINGS.SYSTEM_GW,SYSTEM_SETTINGS.SYSTEM_NTP))
                        self.loaded_cameras = configured_cameras
                  
                  except:
                        logging.exception('Camera configuration did not load.')
      
      def __repr__(self):
            return f'{self.loaded_cameras}'