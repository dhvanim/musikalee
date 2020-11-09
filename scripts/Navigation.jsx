import React from 'react';
 
import { NavLink } from 'react-router-dom';

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
 
export function Navigation(){
    return (
       <div style={containerStyle}>
       <div className="innernavigation">
          <NavLink to="/"><img src="./static/timeline.png" style={imgStyle}/></NavLink>
          <NavLink to="/profile"><img src="./static/profile.png" style={imgStyle}/></NavLink>
          <NavLink to="/messaging"><img src="./static/messaging.png" style={imgStyle}/></NavLink>
       </div>
       </div>
    );
}
 
export default Navigation;