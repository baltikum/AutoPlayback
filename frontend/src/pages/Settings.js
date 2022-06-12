import React from "react";

import '../components/css/container.css'
import '../components/css/form-holder.css'

import SettingsChoices from '../components/settings/SettingsChoices'

const Settings = () => {




	return (
		<div className="container">
			<div className="form-holder">
				<SettingsChoices />
			</div>
		</div>
	);

};

export default Settings;