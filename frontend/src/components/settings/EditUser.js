import React, {useState, useEffect} from 'react'
import axios from 'axios'

import '../css/form-holder.css'


function EditUser ({postEditUser, setChoice})  {

    function handleReturn() {
        setChoice(false)
    }
    function handleSubmit(event) {
        postEditUser(event)
        setChoice(false)
    }
    const [ userId, setUserId ] = useState('')
    const [ userName, setUserName ] = useState('')
    const [ userDevice, setUserDevice ] = useState('')
    const [ userUsername, setUserUsername ] = useState('')
    const [ userPassword, setUserPassword ] = useState('')

    const [ configuredUsers, setConfiguredUsers] = useState([])

    const fetchConfiguredUsers = async () => {
        axios.get('/get_users').then(
              (response) => {
                    setConfiguredUsers(response.data.users);
                    console.log(response.data);
              },
              (error) => {
                    console.log(error);
              }
        ); 
    }
    useEffect(() => {
        fetchConfiguredUsers();
    },[]);

    function selectUser(event) {
        let index = event.target.selectedIndex;
        let temp = configuredUsers[index]
        setUserId(temp.id)
        setUserName(temp.name)
        setUserDevice(temp.device)
        setUserUsername(temp.username)
        setUserPassword(temp.password)
    }

    return (
<>

    <h1>Edit User <i class="bi-person-lines-fill"></i></h1>
    <h6>Don't forget to save</h6>

    <form onSubmit={handleSubmit} >

        <div className="input-group input-group-lg">
            <select onChange={selectUser} className="form-control" name="user-choice">
                {configuredUsers.map( (users,index)=>
                        (
                            <option value={index}>{users.name}</option>
                        )
                    )
                }
            </select>
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_id" placeholder={userId} required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_name" placeholder={userName} required />
        </div>


        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="text" name="user_username" placeholder={userUsername} required />
        </div>

        <div className="input-group input-group-lg">
            <input className="form-control input-add" type="password" name="user_password" placeholder={userPassword} required />
        </div>


        <br />

        <h6>Presence Device MAC Address <i class="bi-wifi"></i></h6>
        <div class="input-group input-group-lg">
            <input id="device" class="form-control" type="text" placeholder={userDevice} maxlength="17"
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