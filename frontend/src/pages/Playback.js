import React from "react";

import '../components/css/container.css'
import '../components/css/video-layout.css'

const Playback = (playbacks) => {
return (
	<div className="container">
		<div className="video-layout">
			<h1>Playback</h1>
			<VideoPlayback playbacks={playbacks} />
		</div>
	</div>
);

};

export default Playback;