import * as React from 'react';
import { Socket } from './Socket';

export default function PostItem(props) {
    console.log("IN POSTITEM")
    console.log(props)
    return (
        <div>
            <li key={props.id} className="post">
                <span className="username"> { props.username } </span> <br />
                <span className="text"> { props.text } </span> <br />
                <span className="time"> { props.time } </span> 
                <span className="likes"> &hearts; { props.likes } </span> <br />
            </li>
        </div>
    );
}
