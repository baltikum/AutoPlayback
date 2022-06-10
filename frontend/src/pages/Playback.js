import React, { useState, useEffect } from 'react'
import ReactPlayer from 'react-player'

import axios from 'axios'
import '../components/css/container.css'
import '../components/css/video-holder.css'



//onEnded={() => setNextSource()}




const Playback = () => {
	const [playbacks,setPlayback] = useState([])
    const [playing, setPlaying] = useState(true)
    const [videoSource, setVideoSource ] = useState('/playback/0.mp4')

	/* Fetches array with info about recordings files*/
	const fetchPlayback = async () => {
		  axios.get('/playback/fetch').then(
				(response) => {
					  setPlayback(response.data)
                      
				},
				(error) => {
					  console.log(error);
				}
		  ); 
	}


	useEffect(() => {
		  fetchPlayback()
	},[]);

    useEffect(() => {
        setPlaying(true)
    },[playbacks,videoSource]);  

	

	return (
		<div className="container">
			<div className="video-holder">

				<h1>Playback</h1>

				<ReactPlayer 
					url={videoSource}
					playing={playing}  
					controls={true} 
					muted
					onReady={() => console.log('VIDEO ready')} 
					onStart={() => console.log('VIDEO start')} 
					onEnded={() => setVideoSource('/playback/1.mp4')}
				/>

			</div>
		</div>
	);

};

export default Playback;