import React from 'react'
import '../css/form-holder.css'



function LoginQuit({userLogout}) {

    function handleSubmit(event) {
        userLogout(event)
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <button type="submit" className="btn btn-info btn-lg">Logout</button>
            </form>
        </div>
    )
}

export default LoginQuit
