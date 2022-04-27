import React from 'react'

export default function VideoPlayback(playback) {
  return (
      <>
            <video autoPlay muted>
                  <source src={'/video/' + playback.id} type="video/mp4" />
            </video>
      </>

  )
}
