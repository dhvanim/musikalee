import React from 'react';
import { Socket } from './Socket';

export default function EventItem(props){

    return (
       <div className="eventItem">
            <img src={props.image} className="album_art" />
            <p className="title"> {props.name} </p>
            <p className="location"> {props.venue} </p>
            <p className="datetime"> {props.date} </p>
            <button className="buyLink" onClick={()=> window.open(props.url, "_blank")}> Buy Tickets</button>
          
       </div>
    );
}
 