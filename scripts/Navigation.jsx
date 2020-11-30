import React from 'react';
 
import { NavLink } from 'react-router-dom';
import { Socket } from './Socket';

const imgStyle =  {
    display: "block",
    height: "50px",
    width: "50px",
    padding: "15px"
};

const containerStyle ={
    float: "left",
    display: "flex",
    justifyContent: "center",
    flexDirection: "column",
    height: "100%",
    width:"25%",
    zIndex:"10"
};
 
function getPosts(){
    //TODO - emit get local storage
    Socket.emit("get local storage", true);
}

function getProfile() {
    Socket.emit("get profile", true);
}

export function Navigation(){
    return (
       <div style={containerStyle}>
       <div className="innernavigation">
          <NavLink to="/" onClick={getPosts}><img src="./static/timeline.png" style={imgStyle}/></NavLink>
          <NavLink to="/profile" onClick={getProfile}><img src="./static/profile.png" style={imgStyle}/></NavLink>
          <NavLink to="/ticket"><img src="./static/ticket.png" style={imgStyle}/></NavLink>
       </div>
       </div>
    );
}
 
export default Navigation;