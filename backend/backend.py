

from pack import app

from datetime import datetime
import cv2, uuid, json, logging

from pack.sys_variables import Sys_variables
from pack.db_models import User,Recordings,CameraConfigs
from pack.presence import Presence
from pack.camera import Camera

from concurrent.futures import ThreadPoolExecutor


#import os, re, time,traceback






configured_cameras = []
capturing_cameras = []
presence_active = False
executor = ThreadPoolExecutor()


video_playback_entrys = [{'id':0,'name':'Vardagsrum', 'time':'20220422','file':'filnamn.mp4'}]
archived_video_playback = [] #Should be written to database

#Load the camera configurations and start captures
def load_cameras():
    global configured_cameras
    try:
        with open('/home/pi/AutoPlayback/backend/camera_configurations.ini', 'r') as file:
            jsonData = file.read()
            
        json_cameras = json.loads(jsonData)
        list_of_cameras= json_cameras['cameras']
        print(f'Loaded Cameras: {list_of_cameras}')
        
        for entry in list_of_cameras:
            configured_cameras.append(Camera(int(entry.get('id')), entry.get('ip'), entry.get('name'), entry.get('username'),
                                          entry.get('password'),entry.get('settings'),SYSTEM_HOST,
                                          SYSTEM_GW,SYSTEM_NTP))
        res = True
    except:
        logging.exception('Camera configuration did not load.')
        res = False
        
    return res   
def configure_cameras():
    global configured_cameras
    for entry in configured_cameras:
        entry.configure_camera()
    return True
def start_cameras():
    global configured_cameras,capturing_cameras
    for entry in configured_cameras:
        capture = cv2.VideoCapture(entry.url)
        capturing_cameras.append(capture)
        
    return True       
def record_camera(id):
    global configured_cameras, capturing_cameras,presence_active,video_playback_entrys
    camera = capturing_cameras[id]

    start_time = False
        
    recording_uuid = uuid.uuid4()
    fileName = f'{recording_uuid}_{configured_cameras[id].camera_name}.mp4'
    
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fileout = cv2.VideoWriter(fileName, codec, 20.0, (1024,  768))
  
    res, frame = camera.read()
    buffer = []
    buffer_max_size = configured_cameras[id].fps * 3 # 3 seconds * 18fps max images 3*18*1280*720 /8   /1000  /1000 ~ 6.2 MB buffer per cam
    
    record = 0
    recording_started_at = ''
    
    while(True):
        
        res, frame = camera.read()
        buffer.append(frame)
        
        record += 1
        
        
        if not res or record > 200 or presence_active:
            break
        else:      
            #Requires camera_motion to be stable 
            #from motion til x seconds after motion
            if configured_cameras[id].camera_motion :
                
                if not start_time:
                    now = datetime.now()
                    format = "%Y%m%d_%H%M%S"
                    recording_started_at = now.strftime(format)
                    start_time = True
                    
                fileout.write(buffer.pop(0)) #Write
            else:
                if not start_time:
                    if len(buffer) >= buffer_max_size:
                        buffer.pop(0) #Discard
                else:
                    #Add delay here, ex record some seconds after motion
                    break
        

        
    #camera.release() Not needed anymore
    now = datetime.now()
    format = "%Y%m%d_%H%M%S"
    recording_ended_at = now.strftime(format)
    
    fileout.release()
    
    #Add to playback
    video_playback_entry = {
        'video_uuid': recording_uuid,
        'video_start_time': recording_started_at,
        'video_end_time': recording_ended_at,
        'video_camera_id': id,
        'video_file': fileName
        }
    video_playback_entrys.append(video_playback_entry)
    
    #Call itself to reinitiate a buffer session and new file
    if not presence_active:
        read_captures(id)
   
   

if __name__ == '__main__':
      
      SYSTEM_SETTINGS = Sys_variables()


      if load_cameras():
            #if configure_cameras():
            if start_cameras():
                  logging.info('Camera configuration loaded.')
                  #record_camera(0)
            else:
                  logging.error('Cameras could not be started.')
                  
            #else:
                  #logging.error('Cameras could not be configured')
      else:
            logging.error('Cameras could not be loaded from configuration file.')
            
            
            
            

    
    app.run(host='localhost',port=PORT,debug=True,threaded=True)
    
