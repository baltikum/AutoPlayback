import React, {useState} from "react";

import '../components/css/container.css'
import '../components/css/form-holder.css'

import LoginTop from '../components/login/LoginTop'
import LoginForm from '../components/login/LoginForm'
import LoginQuit from '../components/login/LoginQuit'




function Login ({setLoggedIn, setLoggedInUser, loginStatus }) {

    function handleLogin(value) {
      setLoggedIn(value)
    }

    function handleLoggedInUser(value) {
      setLoggedInUser(value)
    }
      const database = [
          {
            username: "user1",
            password: "pass1",
            privilege: "1",
            device: "123"
          },
          {
            username: "user2",
            password: "pass2",
            privilege: "2",
            device: "123456"
          }
        ];

        const [logState, setLoggedInState ] = useState(loginStatus)
        const [userData, setUserData ] = useState({})



        const postSubmit = (event) => {
          
          event.preventDefault();
        
          var { uname, pass } = document.forms[0];
          console.log(uname.value)
          console.log(pass)

          const userData = database.find((user) => user.username === uname.value);
        
          if (userData) {
            if (userData.password === pass.value) {

              localStorage.setItem('username', userData.username )
              localStorage.setItem('privilege', userData.privilege )
              localStorage.setItem('user', userData )

              handleLogin(true)
              handleLoggedInUser(userData)

              setLoggedInState(true)
              console.log(userData)
            };
          };

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