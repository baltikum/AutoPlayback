

from pack import app

from datetime import datetime, timedelta
import cv2, uuid, logging, traceback

from pack.sys_variables import Sys_variables
from pack.db_models import User,Recordings,CameraConfigs
from pack.presence import Presence
from pack.load_cameras import Load_Cameras

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue

#import os, re, time,traceback






configured_cameras = []
capturing_cameras = []
presence_active = False


video_playback_entrys = [{'id':0,'name':'Vardagsrum', 'time':'20220422','file':'filnamn.mp4'}]
archived_video_playback = [] #Should be written to database

  


def start_recording(msg_queue,camera):

	motion_at = datetime.now() - timedelta(hours = 1)

	capture = cv2.VideoCapture(camera.url)
	
	buffer = []
	buffer_max_size = camera.fps * 3
	
	#Buffer awaiting motion
	while True:
		_ , frame = capture.read()
		buffer.append(frame)

		if len(buffer) > buffer_max_size :
			buffer.pop(0)

		try:
			temp = msg_queue.get_nowait()
			if temp :
				motion_at = temp
		except:
			motion_at = motion_at

		if (datetime.now() - motion_at) < 5 :
			break
	
	#Start new file
	format = "%Y%m%d_%H%M%S"
	recording_started_at = motion_at.strftime(format)
	fileName = f'{recording_started_at}_{camera.camera_name}.mp4'
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	#Edit for camera settings!!! when implemented
	fileout = cv2.VideoWriter(fileName, codec, 20.0, (1024,  768))


	#The recording, perhaps need extending when further motion is detected
	while ( datetime.now() - motion_at < 10 ):
		_ , frame = capture.read()
		if len(buffer) > 0 :
			fileout.write(buffer.pop(0)) 
		else:
			fileout.write(frame)

		try:
			temp = msg_queue.get_nowait()
			if temp :
				motion_at = temp
		except:
			motion_at = motion_at

	fileout.release()

	#Create recording entry
	ended_at = datetime.now()
	recording_ended_at = ended_at.strftime(format)
	video_playback_entry = {
		'video_start_time': recording_started_at,
        'video_end_time': recording_ended_at,
        'video_camera_id': id,
        'video_file': fileName
    }

	return video_playback_entry

	


if __name__ == '__main__':
	thread_pool = ThreadPoolExecutor()

	SYSTEM_SETTINGS = Sys_variables()
	system_cameras = Load_Cameras(SYSTEM_SETTINGS)
	
	if not SYSTEM_SETTINGS.cameras_configured :
		try:
			for camera in system_cameras.loaded_cameras:
				camera.configure_camera()
				
			SYSTEM_SETTINGS.cameras_configured = True
		except:
			traceback.print_exc()
	

	
	for index, camera in enumerate(system_cameras.loaded_cameras):
		camera.msg.queue = Queue()
		thread_pool.submit(start_recording, (camera.msg_queue, camera) )

          
	app.run(host='localhost', port=SYSTEM_SETTINGS.FLASK_PORT, debug=True, threaded=True)
    
