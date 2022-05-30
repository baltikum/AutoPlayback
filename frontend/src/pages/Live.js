import React from "react";

import ReactPlayer from 'react-player'
import '../components/css/container.css'
import '../components/css/video-holder.css'

/*const url = 'http://root:Examen2022?!@192.168.0.90/mjpg/video.mjpg'*/
//'http://localhost:666/liveStream.m3u8'


const Live = () => {
return (
	<div className="container">
		<div className="video-holder">
			<h1>Live</h1>
            <ReactPlayer url='http://localhost:666/liveStream.m3u8' width='100%' height={800} playing={true}  controls={true} muted />
		</div>
	</div>
);

};

export default Live;
