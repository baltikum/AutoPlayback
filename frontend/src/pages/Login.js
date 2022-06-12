import React, {useState} from "react";

import '../components/css/container.css'
import '../components/css/form-holder.css'

import LoginTop from '../components/login/LoginTop'
import LoginForm from '../components/login/LoginForm'
import LoginQuit from '../components/login/LoginQuit'

import axios from 'axios'
//import bcrypt from 'bcryptjs'


function Login ({setLoggedIn, setLoggedInUser, loginStatus }) {

    function handleLogin(value) {
      setLoggedIn(value)
    }

    function handleLoggedInUser(value) {
      setLoggedInUser(value)
    }
      

    const [logState, setLoggedInState ] = useState(loginStatus)
    const [userData, setUserData ] = useState({})



    const postSubmit = (event) => {
      event.preventDefault();
      
      var { uname, pass } = document.forms[0];
      
      axios.post('/query_user_salt', {'username': uname.value } ).then(
            (response) => {
              console.log('fan')
              console.log(response.data)
              console.log(response.data.salt)

              if ( response.data.status ) {
                pass = pass.value
                //pass = bcrypt.hashSync(pass.value, response.data.salt)
                axios.post('/login', {'username': uname.value, 'password': pass } ).then(
                  (response) => {
                    console.log(response.data)
                    console.log(response.data.username)
                    localStorage.setItem('username', response.data.username )
                    localStorage.setItem('privilege', response.data.privilege )
                    localStorage.setItem('user', response.data )    
                    handleLogin(true)
                    handleLoggedInUser(response.userData)
                    setLoggedInState(true)     
    
    
                  },
                  (error) => {
                        console.log(error);
                  }
              );
              
              } else {
                return 'User not found'
              }
            },
            (error) => {
                  console.log(error);
            }
          );

        };



        const userLogout = (event) => {
          handleLogin(false)
          handleLoggedInUser({})

          setLoggedInState(false)
          localStorage.clear();
        };
     
      

      const loggedOutForm = (
        <>
          <LoginTop />
          <h6>Enter credentials to login <i className="bi-key-fill"></i></h6>
          <LoginForm postSubmit={postSubmit}/>
        </>
      );
      
      const loggedInForm = (
        <>
          <LoginTop  />
          <h6>Logged in as {localStorage.getItem('username')}<br></br> Your privilege is set to {localStorage.getItem('privilege')}</h6>
          <LoginQuit userLogout={userLogout}/>
        </>
      );


  return (
    <div className="container">
      <div className="form-holder">
        {logState ? loggedInForm : loggedOutForm }
      </div>
    </div>
  );

};

export default Login;