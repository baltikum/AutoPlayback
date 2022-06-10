import React from 'react'


import '../css/form-holder.css'


function EditUser ({postEditUser, setChoice})  {

    function handleReturn() {
        setChoice(false)
    }
    function handleSubmit(event) {
        postEditUser(event)
        setChoice(false)
    }

    return (
<>

    <h1>Edit User <i class="bi-person-lines-fill"></i></h1>
    <h6>Don't forget to save</h6>

    <form onSubmit={handleSubmit} >

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_id" placeholder="Id" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_name"placeholder="Name" required />
        </div>


        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_username" placeholder="Username" required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="password" name="user_password"placeholder="Password" required />
        </div>


        <br />

        <h6>Presence Device MAC Address <i class="bi-wifi"></i></h6>
        <div class="input-group input-group-lg">
            <input id="device" class="form-control" type="text" placeholder="01-23-45-67-89-AB" maxlength="17"
                pattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$" />
        </div>

    <br />

        <button id="submit" type="submit" class="btn btn-info btn-lg button-add">Save</button>
        <button onClick={handleReturn} type="button" class="btn btn-secondary btn-lg button-add">Back</button>

    </form>

</>

)
}

export default EditUser;