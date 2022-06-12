import React, { useEffect, useState } from "react";
import ReactPlayer from 'react-player'


import axios from 'axios'
import '../components/css/container.css'
import '../components/css/video-holder.css'



const Live = () => {

    const [allSources,setAllSources] = useState([])
    const [sourceIndex, setSourceIndex ] = useState(0)

    const nextSource = (event) => {
        const max = allSources.length;
        if (sourceIndex === (max-1)) {
            setSourceIndex(0);
        } else {
            setSourceIndex((sourceIndex+1))
        }
    }

    const fetchLiveSources = async () => {

        axios.get('/live/sources').then(
              (response) => {
                    setAllSources(response.data.live)
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

            <ReactPlayer 
                className='player-wrapper'
                url={allSources[sourceIndex]} 
                width='50%'
                height='50%'
                playing={true}  
                controls={false} 
                muted 
                onClick={nextSource} 
            />

            <button 
                type="button" 
                className="btn btn-info btn-lg" 
                onClick={nextSource}>
                    Next
            </ button>

		</div>

        

	</div>
);

};

export default Live;
