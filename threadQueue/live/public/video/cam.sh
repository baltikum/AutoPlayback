#!/bin/bash

VIDSOURCE="rtsp://onvif:onvif@192.168.0.90/onvif-media/media.amp"
VIDEO_OPTS="-s 800x600 -c:v libx264 -b:v 800000"
OUTPUT_HLS="-hls_time 10 -hls_list_size 10 -start_number 1"
ffmpeg -i "$VIDSOURCE" -y $VIDEO_OPTS $OUTPUT_HLS liveStream.m3u8