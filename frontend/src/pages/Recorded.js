import React from "react";

import VideoPlayback from '../components/playback/VideoPlayback'
import '../components/css/container.css'
import '../components/css/video-holder.css'

const Recorded = () => {
return (
	<div className="container">
		<div className="video-holder">
			<h1>Recorded</h1>

            <VideoPlayback />
		</div>
	</div>
);

};

export default Recorded;