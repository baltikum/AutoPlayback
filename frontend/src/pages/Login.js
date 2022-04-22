import React from "react";

import '../components/css/container.css'
import '../components/css/form-holder.css'

import LoginTop from '../components/login/LoginTop'
import LoginForm from '../components/login/LoginForm'


const Login = () => {
return (
	<div className="container">
		<div className="form-holder">
			<LoginTop />
			<LoginForm />
		</div>
	</div>
);

};

export default Login;