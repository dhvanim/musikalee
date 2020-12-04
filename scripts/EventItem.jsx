import React from 'react';

export default function EventItem(props){

    return (
       <div>
       <div className="eventItem">
            <button className="buyLink" onClick={()=> window.open(props.url, "_blank")}> Buy Tickets</button>
            <img src={props.image} className="image" />
            <span className="title"> {props.name} </span> <br />
            <span className="location"> {props.venue} </span> <br />
            <span className="datetime"> {props.date} </span> <br />
       </div>
       <div id="spacer5"></div>
       </div>
    );
}
 