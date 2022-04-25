import React from "react";
import '../components/css/container.css'
import '../components/css/form-holder.css'

/*const url = 'http://root:Examen2022?!@192.168.0.90/mjpg/video.mjpg'*/



const Live = () => {
return (
	<div className="container">
		<div className="form-holder">
			<h1>Live</h1>
			<video autoPlay muted>
				<source src="http://localhost:5000/videos" type="video/mp4" />
			</video>
			
		</div>
	</div>
);

};

export default Live;
