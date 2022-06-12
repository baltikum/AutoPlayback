import React, {useState,useEffect} from 'react'
import axios from 'axios'

import '../css/form-holder.css'


function EditCamera ({postEditCamera, setChoice})  {



    const [ cameraId, setCameraId ] = useState('')
    const [ cameraName, setCameraName ] = useState('')
    const [ cameraAddress, setCameraAddress ] = useState('')
    const [ cameraUsername, setCameraUsername ] = useState('')
    const [ cameraSetting, setCameraSetting ] = useState(0)

    const [ configuredCameras, setConfiguredCameras] = useState([])


    function handleSubmit(event) {
        postEditCamera(event)
        setChoice(false)
    }
    function handleReturn() {
        setChoice(false)
    }


	const fetchConfiguredCameras = async () => {
        axios.get('/get_cameras').then(
              (response) => {
                    setConfiguredCameras(response.data.cameras);
                    console.log(response.data);
              },
              (error) => {
                    console.log(error);
              }
        ); 
  }

	useEffect(() => {
        fetchConfiguredCameras();
  },[]);



    function selectCamera(event) {
        let index = event.target.selectedIndex;
        let temp = configuredCameras[index]
        setCameraId(temp.id)
        setCameraName(temp.name)
        setCameraAddress(temp.address)
        setCameraUsername(temp.username)
        setCameraSetting(temp.setting)
    }

    return (
<>

    <h1>Edit Camera <i class="bi-gear-fill"></i></h1>
    <h6>Choose camera</h6>

    <form onSubmit={handleSubmit} >
        <div className="input-group input-group-lg">
            <select onChange={selectCamera} className="form-control" name="camera-choice">
                {configuredCameras.map( (camera,index)=>
                        (
                            <option value={index}>{camera.name}</option>
                        )
                    )
                }
            </select>
        </div>

        <br />
        <h6>Update IP address or credentials</h6>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_id" placeholder={cameraId} value={cameraId} required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_name"placeholder={cameraName} value={cameraName} required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_address" maxlength="15" 
                pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" placeholder={cameraAddress} required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_username" placeholder={cameraUsername} required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="password" name="camera_password"placeholder="Password" required />
        </div>

        <div className="input-group input-group-lg">
            <select className="form-control" name="setting-choice" value={cameraSetting}>
                <option value="0">1280x720@25FPS</option>
                <option value="1">1280x720@18FPS</option>
                <option value="2">1280x720@8FPS</option>
            </select>
        </div>

        <br />

        <button id="submit" type="submit" class="btn btn-info btn-lg">Edit Camera</button>
        <button onClick={handleReturn} type="button" class="btn btn-secondary btn-lg">Back</button>

    </form>

</>

)
}

export default EditCamera;