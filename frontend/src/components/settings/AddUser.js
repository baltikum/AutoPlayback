import React from 'react'
import bcrypt from 'bcryptjs'
import '../css/form-holder.css'


function AddUser ({postNewUser, setChoice})  {


    function handleReturn() {
        setChoice(false)
    }
    function handleSubmit(event) {
        postNewUser(event)
        setChoice(false)
    }

    return (
<>

    <h1>Add User <i class="bi-person-plus-fill"></i></h1>
    <h6>Edit new user</h6>

    <form onSubmit={handleSubmit} >

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_name"placeholder="Name" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_email" maxlength="15" placeholder="mail@email.com" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_username" placeholder="Username" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="password" name="user_password" placeholder="Password" required />
        </div>

        <div className="input-group input-group-lg">
            <select className="form-control input-add" name="setting-choiceuser_privilege">
                <option value="0">Administrator</option>
                <option value="1">Live and Playback</option>
                <option value="2">Live</option>
            </select>
        </div>


        <br />

        <h6>Presence Device MAC Address <i class="bi-wifi"></i></h6>
        <div className="input-group input-group-lg">
            <input className="form-control" type="text" placeholder="01-23-45-67-89-AB" maxlength="17" name="user_device"
                pattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$" />
        </div>

        <br />
        <button id="submit" type="submit" class="btn btn-info btn-lg button-add">Add User</button>
        <button onClick={handleReturn} type="button" class="btn btn-secondary btn-lg button-add">Back</button>

    </form>

</>

)
}

export default AddUser;