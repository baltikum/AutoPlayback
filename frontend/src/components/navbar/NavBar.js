import React from "react";
import { Nav, NavLink, NavMenu } from "./NavBarElements";

const NavBar = () => {
	return (
		<>
		<Nav>
			<NavMenu>
			<NavLink to="/live">
				<i className="bi-play-fill"></i> Live
			</NavLink>
			<NavLink to="/recorded">
				<i className="bi-disc-fill"></i> Recorded
			</NavLink>
			<NavLink to="/settings">
				<i className="bi-sliders"></i> Settings
			</NavLink>
			<NavLink to="/login">
				<i className="bi-x-circle-fill"></i> Login
			</NavLink>
			</NavMenu>
		</Nav>
		</>
	);
};

export default NavBar;
