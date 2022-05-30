import React, { useEffect, useState } from "react";
import ReactPlayer from 'react-player'


import axios from 'axios'
import '../components/css/container.css'
import '../components/css/video-holder.css'

/*const url = 'http://root:@192.168.0.90/mjpg/video.mjpg'*/
//'http://localhost:666/liveStream.m3u8'


const Live = () => {

    const [allSources, setAllSources] = useState([])
    const [liveSource,setLiveSource] = useState('http://localhost:666/liveStream.m3u8')
    const nextSource = (event) => {
        setLiveSource('http://localhost:666/live.m3u8' )
        console.log('NEXT SOURCE')
    }

    const fetchLiveSources = async () => {
        axios.get('/live/sources').then(
              (response) => {
                    setAllSources(response.data)
              },
              (error) => {
                    console.log(error);
              }
        ); 
    }

	useEffect(() => {
        fetchLiveSources()
    },[]);

return (
	<div className="container">
		<div className="video-holder">
			<h1>Live</h1>
            <ReactPlayer url='http://localhost:666/0.m3u8' width='100%' height={800} playing={true}  controls={true} muted />
            <button type="button" className="btn btn-info btn-lg" onClick={nextSource}>Next</ button>
		</div>

        

	</div>
);

};

export default Live;
