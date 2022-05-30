import React from "react";

import '../components/css/container.css'
import '../components/css/video-holder.css'

const Recorded = () => {
return (
	<div className="container">
		<div className="video-holder">
			<h1>Recorded</h1>
            <video autoPlay muted>
                  <source src='http://localhost:5000/playback' type="video/mp4" />
            </video>
		</div>
	</div>
);

};

export default Recorded;