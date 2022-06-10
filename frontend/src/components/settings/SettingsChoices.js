import React, {useState} from 'react'

import AddCamera from './AddCamera'
import EditCamera from './EditCamera'
import AddUser from './AddUser'
import EditUser from './EditUser'

import axios from 'axios'

import '../css/form-holder.css'

const SettingsChoices = () => {


    const [choice, setChoice] = useState(false)
    const [content, setContent ] = useState()


    const postNewCamera = async (event) => {

        event.preventDefault();
        var { camera_name, camera_username, camera_password, camera_address } = document.forms[0];

        
        axios.post('/add_camera', {'name': camera_name.value,'username':camera_username.value,'password':camera_password.value,'address':camera_address.value} ).then(
            (response) => {
                console.log(response);
            },
            (error) => {
                  console.log(error);
            }
        );
    }
    const postEditCamera = async (event) => {

        event.preventDefault();
        var { camera_id, camera_name, camera_username, camera_password, camera_address } = document.forms[0];

        axios.post(('/edit_camera/' + camera_id.value), {'name': camera_name.value,'username':camera_username.value,'password':camera_password.value,'address':camera_address.value} ).then(
            (response) => {
                console.log(response);
            },
            (error) => {
                  console.log(error);
            }
        );
    }

    const postNewUser = async (event) => {

        event.preventDefault();
        var { user_name, user_username, user_password, user_email,user_device } = document.forms[0];
        user_password = bcrypt.hashSync(user_password, 'autoplayback_salt')
        
        axios.post('/add_user', {'name': user_name.value,'username':user_username.value,'password':user_password.value,'email':user_email.value,'device':user_device.value} ).then(
            (response) => {
                console.log(response);
            },
            (error) => {
                  console.log(error);
            }
        );
    }
    const postEditUser = async (event) => {

        event.preventDefault();
        var { user_id, user_name, user_username, user_password, user_email, user_device } = document.forms[0];

        
        axios.post(('/edit_user/' + user_id.value), {'name': user_name.value,'username':user_username.value,'password':user_password.value,'email':user_email.value,'device':user_device.value} ).then(
            (response) => {
                console.log(response);
            },
            (error) => {
                  console.log(error);
            }
        );
    }





    const generateAddCamera = (event) => {
        setChoice(true)
        setContent(<AddCamera postNewCamera={postNewCamera} setChoice={setChoice} />)
    }
    const generateEditCamera = (event) => {
        setChoice(true)
        setContent(<EditCamera postNewCamera={postEditCamera} setChoice={setChoice} />)
    }
    const generateAddUser = (event) => {
        setChoice(true)
        setContent(<AddUser postNewUser={postNewUser} setChoice={setChoice} />)
    }
    const generateEditUser = (event) => {
        setChoice(true)
        setContent(<EditUser postEditUser={postEditUser} setChoice={setChoice} />)
    }

   



    const settingsForm = (
        <>
            <h1>Settings <i className="bi-gear-fill"></i></h1>
            <h6>Choose setting</h6>
            <button onClick={generateAddCamera} type="button" className="btn btn-info btn-lg button-add">Add Camera</button>
            <button onClick={generateEditCamera} type="button" className="btn btn-info btn-lg button-add">Edit Camera</button>
            
            <button onClick={generateAddUser} type="button" className="btn btn-info btn-lg button-add">Add User</button>
            <button onClick={generateEditUser} type="button" className="btn btn-info btn-lg button-add">Edit User</button>

            <button type="button" className="btn btn-info btn-lg button-add">Network Settings</button>
        </>
      );

    return (
        <>
            
        {choice ? content : settingsForm  }

        </>
    )
}

export default SettingsChoices