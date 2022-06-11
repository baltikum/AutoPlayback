import React, { useState, useEffect } from 'react'
import ReactPlayer from 'react-player'

import axios from 'axios'
import '../components/css/container.css'
import '../components/css/video-holder.css'




const Playback = () => {
	const [playbacks,setPlayback] = useState(['http://192.168.0.5:5000/playback/0.mp4','http://192.168.0.5:5000/playback/1.mp4']);
    const [playing, setPlaying] = useState(true);
	const [playbackIndex, setPlaybackIndex ] = useState(0);

	const changePlayback = async () => {
		const max = playbacks.length;
        if (playbackIndex === (max-1)) {
            setPlaybackIndex(0);
        } else {
            setPlaybackIndex((playbackIndex+1));
        }
	}


	/* Fetches array with info about recordings files*/
	const fetchPlayback = async () => {
		  axios.get('/playback/fetch').then(
				(response) => {
					  setPlayback(response.data);
					  console.log(response.data);
				},
				(error) => {
					  console.log(error);
				}
		  ); 
	}


	useEffect(() => {
		  fetchPlayback();
	},[]);

    useEffect(() => {
        setPlaying(true)
    },[playbacks,playbackIndex]);  

	

	return (
		<div className="container">
			<div className="video-holder">

				<h1>Playback</h1>
				<div className='player-wrapper'>
					<ReactPlayer 
						className="react-player"
						url={playbacks[playbackIndex]}
						playing={playing}  
						controls={true} 
						width='75%'
						height='75%'
						muted
						onEnded={() => changePlayback()}
					/>
				</div>

			</div>
		</div>
	);

};

export default Playback;