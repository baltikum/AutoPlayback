import React from "react";

import '../components/css/container.css'
import '../components/css/form-holder.css'

import LoginTop from '../components/login/LoginTop'
import LoginForm from '../components/login/LoginForm'
import axios from 'axios'

const Login = () => {
	/* Login */
	const postSubmit = (event) => {
        event.preventDefault()
        const formData = new FormData();
        var { user, passw } = document.forms[0]
        console.log(user)
        console.log(passw)
        formData.append('username', user);
        formData.append('password', passw);

        axios.post("/login", formData).then(
            (response) => {
                console.log(response)
            },
            (error) => {
                console.log(error)
            }
        );
      }

return (
	<div className="container">
		<div className="form-holder">
			<LoginTop />
			<LoginForm postSubmit={postSubmit} />
		</div>
	</div>
);

};

export default Login;