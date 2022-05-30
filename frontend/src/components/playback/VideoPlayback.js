import React from 'react'
import ReactPlayer from 'react-player'

//'http://localhost:666/liveStream.m3u8'

export default function VideoPlayback(playback) {
  return (
      <>
            <ReactPlayer url={playback} playing={true}  controls={true} muted />
      </>

  )
}
