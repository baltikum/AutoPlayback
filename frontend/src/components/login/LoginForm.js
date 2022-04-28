import React from 'react'
import '../css/form-holder.css'



const LoginForm = (postSubmit) => {

    function handleSubmit(event) {
        postSubmit(event)
    }
    
    return (
        <div>
            <form onSubmit={handleSubmit}>

                        <div className="input-group input-group-lg">
                            <input type="text" name="user" className="form-control input-add" required></input>
                        </div>

                        <div className="input-group input-group-lg">
                            <input type="password" name="passw" className="form-control input-add" required></input>
                        </div>

                        <br></br>

                        <button type="submit" className="btn btn-info btn-lg">Login</button>
                        <button type="clear" className="btn btn-secondary btn-lg">Clear</button>

            </form>
        </div>
    )
}

export default LoginForm