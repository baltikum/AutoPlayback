import React from 'react'
import '../css/form-holder.css'

function AddCamera ({postNewCamera, setChoice})  {


    function handleReturn(event) {
        setChoice(false)
    }
    function handleSubmit(event) {
        postNewCamera(event)
        setChoice(false)
    }

    return (
<>

    <h1>Add Camera <i class="bi-plus-circle-fill"></i></h1>
    <h6>Enter IP address and credentials</h6>

    <form onSubmit={handleSubmit} >

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_name" placeholder="Name" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_address" maxlength="15" 
                pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" placeholder="192.168.0.0" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="camera_username" placeholder="Username" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="password" name="camera_password"placeholder="Password" required />
        </div>


        <br />

        <button id="submit" type="submit" class="btn btn-info btn-lg">Add Camera</button>
        <button onClick={handleReturn} type="button" class="btn btn-secondary btn-lg">Back</button>

    </form>

</>

)
}

export default AddCamera;