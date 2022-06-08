from concurrent.futures import ProcessPoolExecutor


import shlex

import os




#os.spawnl(os.P_NOWAIT, command)


def live_scamera():
    os.system(command)
 
args = shlex.split(command)


p_pool = ProcessPoolExecutor()

for i in range(4):
    command = (f"ffmpeg -i rtsp://onvif:onvif@192.168.0.90/onvif-media/media.amp" +
 " -fflags flush_packets -max_delay 5 -flags -global_header -hls_time 2 " + 
f"-hls_list_size 3 -vcodec copy -y /var/tmp/video/{i}.m3u8"

    p_pool.submit(live_scamera)