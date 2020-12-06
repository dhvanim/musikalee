import React from 'react';

import { NavLink } from 'react-router-dom';
import { Socket } from './Socket';

function getPosts(){
    //TODO - emit get local storage
    Socket.emit("get local storage", true);
}

function getProfile() {
  Socket.emit('get profile', true);
}

export default function Navigation(){
    return (
       <div className="navigation">
       <div className="innernavigation">
        <ul>
          <li><NavLink to="/" onClick={getPosts}> <i className="fas fa-home"></i> </NavLink></li>
          <li><NavLink to="/profile" onClick={getProfile}> <i className="fas fa-user-circle"></i> </NavLink></li>
          <li><NavLink to="/ticket"> <i className="fas fa-ticket-alt"></i> </NavLink></li>
        </ul>
       </div> 
       <div className="aboutlink">
       <NavLink to="/about"> About Us. </NavLink>
       </div>
       </div>
    );
}
