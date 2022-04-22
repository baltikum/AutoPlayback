import React from 'react'

const SettingsChoices = ( ) => {
    return (



<h1>Add Camera <i class="bi-plus-circle-fill"></i></h1>
<h6>Enter IP address and credentials</h6>

<form id="new-camera-settings" action="#" method="POST" >

<!-- camera ip address-->
<div class="input-group input-group-lg">
    <input id="camera-ip" class="form-control inputadd" type="text" id ="camera-ip-adress" maxlength="15" 
        pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" placeholder="192.168.0.0" required>
</div>

<!-- camera username-->
<div class="input-group input-group-lg">
    <input id="camera-username"class="form-control inputadd" type="text" placeholder="Username" required>
</div>

<!-- camera password-->
<div class="input-group input-group-lg">
    <input id="camera-password" class="form-control inputadd" type="password" placeholder="Password" required>
</div>
<br>

<!-- add and clear buttons-->
<button id="submit" type="button" class="btn btn-info btn-lg">Add</button>
<a href="generalsettings.html"><button type="button" class="btn btn-secondary btn-lg">Return</button></a>


<!-- status spinner ( show on submit )
<div class="spinner-border text-secondary" role="status">
    <span class="visually-hidden">Loading...</span>
</div>-->




</form>
)
}

export default SettingsChoices