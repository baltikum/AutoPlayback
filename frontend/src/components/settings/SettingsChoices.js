import React from 'react'

const SettingsChoices = ( ) => {
    return (
        <div>
            <h1>Settings <i className="bi-gear-fill"></i></h1>
            <h6>Choose setting</h6>

            <a href="addcamera.html"><button id="add-camera" type="button" className="btn btn-info btn-lg">Add Camera</button></a>
            <a href="editcamera.html"><button id="edit-camera" type="button" className="btn btn-secondary btn-lg">Edit Camera</button></a>
            
            <a href="adduser.html"><button id="add-user"type="button" className="btn btn-info btn-lg">Add User</button></a>
            <a href="edituser.html"><button id="edit-user"type="button" className="btn btn-secondary btn-lg">Edit User</button></a>

            <a href="addlayout.html"><button id="add-layout"type="button" className="btn btn-info btn-lg">Add Layout</button></a>
            <a href="editlayout.html"><button id="edit-layout"type="button" className="btn btn-secondary btn-lg">Edit Layout</button></a>

            <a href="storage.html"><button id="edit-storage" type="button" className="btn btn-info btn-lg">Storage Settings</button></a>
            <a href="network.html"><button id="edit-network"type="button" className="btn btn-info btn-lg">Network Settings</button></a>


                {/* SMTP for="flexSwitchCheckDefault"*/}
                <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="flexSwitchCheckDefault" />
                    <label className="form-check-label" >SMTP Notifications</label>
                </div>

                {/* Presence startup for="flexSwitchCheckDefault"*/}
                <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="flexSwitchCheckDefault" />
                    <label className="form-check-label" >Automatic Playback </label>
                </div>

            <a href="index.html"><button id="close" type="button" className="btn btn-secondary btn-lg">Return</button></a>
        </div>
    )
}

export default SettingsChoices