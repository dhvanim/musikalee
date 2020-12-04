import React from 'react';
 
import { NavLink } from 'react-router-dom';
import { Socket } from './Socket';

function getPosts(){
    //TODO - emit get local storage
    Socket.emit("get local storage", true);
}

function getProfile() {
    Socket.emit("get profile", true);
}

export function Navigation(){
    return (
       <div className="navigation">
       <div className="innernavigation">
        <ul>
          <li><NavLink to="/" onClick={getPosts}> <i class="fas fa-home"></i> </NavLink></li>
          <li><NavLink to="/profile" onClick={getProfile}> <i class="fas fa-user-circle"></i> </NavLink></li>
          <li><NavLink to="/ticket"> <i class="fas fa-ticket-alt"></i> </NavLink></li>
        </ul>
       </div> 
       </div>
    );
}
 
export default Navigation;