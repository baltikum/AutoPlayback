

from pack import app

from datetime import datetime, timedelta
import traceback

from pack.sys_variables import Sys_variables
from pack.db_models import User,Recordings,CameraConfigs
from pack.presence import Presence
from pack.load_cameras import Load_Cameras

import time
from queue import Queue


from concurrent.futures import ThreadPoolExecutor





configured_cameras = []
capturing_cameras = []
presence_active = False


video_playback_entrys = [{'id':0,'name':'Vardagsrum', 'time':'20220422','file':'filnamn.mp4'}]
archived_video_playback = [] #Should be written to database

  
def camera_controller(system_cameras,motion_lists):
    global thread_pool

    camera_queues = []


    def add_recorders_to_pool():
        for camera in system_cameras.loaded_cameras:
            camera.msg.queue = Queue()
            camera_queues.append(camera.msg.queue)
            thread_pool.submit(camera.start_recording, (camera.msg_queue, camera) )


    add_recorders_to_pool()
    
    while True:

        #Away loop to distribute motion alarms
        while not presence_active :
            for index, entry in enumerate(motion_lists):
                if len(entry) > 0:
                    try:
                        camera_queues[index].put(entry.pop(0))
                    except:
                        traceback.print_exc()

            time.sleep(1)

        #Stop all ques and recordings
        if presence_active:
            for q in camera_queues:
                try:
                    q.put('_stop')
                    q.task_done()
                except:
                    traceback.print_exc()
            break



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
	


    thread_pool.submit(presence_controller, system_cameras )
          
	app.run(host='localhost', port=SYSTEM_SETTINGS.FLASK_PORT, debug=True, threaded=True)
    
