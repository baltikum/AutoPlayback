import React, { useState, useEffect} from "react";
import axios from 'axios'
import VideoPlayback from '../components/playback/VideoPlayback'
import '../components/css/container.css'
import '../components/css/video-holder.css'

const Playback = () => {
	const [playbacks,setPlayback] = useState([])


	/* Fetches array with info about recordings files*/
	const fetchPlayback = async () => {
		  axios.get('/playback/fetch').then(
				(response) => {
					  setPlayback(response.data)
					  console.log(response.data);
				},
				(error) => {
					  /*console.log(error);*/
				}
		  ); 
	}

	useEffect(() => {
		  fetchPlayback()
	},[]);

	return (
		<div className="container">
			<div className="video-holder">
				<h1>Playback</h1>
				<VideoPlayback playbacks={playbacks} />
			</div>
		</div>
	);

};

export default Playback;