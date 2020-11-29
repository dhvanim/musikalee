import React from 'react';
 
import { NavLink } from 'react-router-dom';
import { Socket } from './Socket';

const imgStyle =  {
    display: "block",
    height: "50px",
    width: "50px",
    padding: "10px 0px 10px 0px",
    margin: "auto",
};

const containerStyle ={
    float: "left",
    display: "flex",
    justifyContent: "center",
    flexDirection: "column",
    width:"10%",
    position:"fixed",
    left:"10px",
    top:"30%",
    zIndex:"10",
    padding:"0",
    backgroundColor: "#fff",
    border: "1px solid #476e3b",
    borderRadius: "15px",
};
 
function getPosts(){
    Socket.emit("user logged in", true);
}

function getProfile() {
    Socket.emit("get profile", true);
}

export function Navigation(){
    return (
       <div style={containerStyle}>
       <div className="navigation">
          <NavLink to="/" onClick={getPosts}><img src="./static/timeline.png" style={imgStyle}/></NavLink>
          <NavLink to="/profile" onClick={getProfile}><img src="./static/profile.png" style={imgStyle}/></NavLink>
          <NavLink to="/messaging"><img src="./static/messaging.png" style={imgStyle}/></NavLink>
       </div>
       </div>
    );
}
 
export default Navigation;