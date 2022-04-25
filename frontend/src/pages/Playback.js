import React from "react";

import '../components/css/container.css'
import '../components/css/form-holder.css'

const Playback = () => {
return (
	<div className="container">
		<div className="form-holder">
			<h1>Playback</h1>
			<video autoPlay muted>
				<source src="http://localhost:5000/videos" type="video/mp4" />
			</video>
		</div>
	</div>
);

};

export default Playback;