import React from 'react'


const handleSubmit = (event) => {
    event.preventDefault()
}
const handleUsernameChange = (event) => {
}

const handlePasswordChange = (event) => {
}


const LoginForm = () => {
    return (
        <div>
            <form onSubmit={handleSubmit}>

                        <div className="input-group input-group-lg">
                            <input type="text" className="form-control inputadd"  onChange={handleUsernameChange} required></input>
                        </div>

                        <div className="input-group input-group-lg">
                            <input type="password" className="form-control input-adding" onChange={handlePasswordChange} required></input>
                        </div>

                        <br></br>

                        <button type="submit" className="btn btn-info btn-lg">Login</button>
                        <button type="clear" className="btn btn-secondary btn-lg">Clear</button>

            </form>
        </div>
    )
}

export default LoginForm