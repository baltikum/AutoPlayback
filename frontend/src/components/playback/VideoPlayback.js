import React, { useState, useEffect } from 'react'
import ReactPlayer from 'react-player'

//'http://localhost:666/liveStream.m3u8'



export default function VideoPlayback(playbacks) {
    const [playing, setPlaying] = useState(true)

    useEffect(() => {
        setPlaying(true)
    },[playbacks]);  
  return (
      
      <>
            

      </>

  )
}
