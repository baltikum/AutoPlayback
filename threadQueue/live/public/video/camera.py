
import subprocess



url = '"rtsp://onvif:onvif@192.168.0.90/onvif-media/media.amp"'
video_options = "-s 1280x720 -c:v libx264 -b:v 800000"
output_settings = "-hls_time 1 -hls_list_size 1 -start_number 1"
full_command = f'ffmpeg -i {url} -y {video_options} {output_settings} /home/baltikum/Dokument/threadQueue/back/static/liveStream.m3u8'

print(full_command)

p = subprocess.Popen(full_command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

