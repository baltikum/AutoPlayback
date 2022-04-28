import React from "react";
import '../components/css/container.css'
import '../components/css/video-holder.css'

/*const url = 'http://root:Examen2022?!@192.168.0.90/mjpg/video.mjpg'*/



const Live = () => {
return (
	<div className="container">
		<div className="video-holder">
			<h1>Live</h1>
			<img src={'/live/0'} alt="Live Video"/>
			
		</div>
	</div>
);

};

export default Live;
