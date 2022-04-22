import React from 'react'

const SettingsChoices = ( ) => {
    return (
        <div>
            <h1>Settings <i class="bi-gear-fill"></i></h1>
            <h6>Choose setting</h6>

            <a href="addcamera.html"><button id="add-camera" type="button" class="btn btn-info btn-lg">Add Camera</button></a>
            <a href="editcamera.html"><button id="edit-camera" type="button" class="btn btn-secondary btn-lg">Edit Camera</button></a>
            
            <a href="adduser.html"><button id="add-user"type="button" class="btn btn-info btn-lg">Add User</button></a>
            <a href="edituser.html"><button id="edit-user"type="button" class="btn btn-secondary btn-lg">Edit User</button></a>

            <a href="addlayout.html"><button id="add-layout"type="button" class="btn btn-info btn-lg">Add Layout</button></a>
            <a href="editlayout.html"><button id="edit-layout"type="button" class="btn btn-secondary btn-lg">Edit Layout</button></a>

            <a href="storage.html"><button id="edit-storage" type="button" class="btn btn-info btn-lg">Storage Settings</button></a>
            <a href="network.html"><button id="edit-network"type="button" class="btn btn-info btn-lg">Network Settings</button></a>


                {/* SMTP */}
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" />
                    <label class="form-check-label" for="flexSwitchCheckDefault">SMTP Notifications</label>
                </div>

                {/* Presence startup */}
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" />
                    <label class="form-check-label" for="flexSwitchCheckDefault">Automatic Playback </label>
                </div>

            <a href="index.html"><button id="close" type="button" class="btn btn-secondary btn-lg">Return</button></a>
        </div>
    )
}

export default SettingsChoices