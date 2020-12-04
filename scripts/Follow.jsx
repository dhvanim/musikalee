import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';

export function Follow(props) {
    const isFollowed = props.isFollowed;
    
    
    function handleSubmit(event) {
        if(isFollowed){
            const element =  "Follow" ;
            ReactDOM.render(element, document.getElementById('f-button'));
            console.log("now Unfollowing");
            
            Socket.emit('recieve follower data');
        }
        
        else{
            const element = "Unfollow";
            ReactDOM.render(element, document.getElementById('f-button'));
            console.log("now Following");
            
            Socket.emit('recieve follower data');
        }
        
        event.preventDefault();
    }

        
    return (
        <form onSubmit={handleSubmit}>
            <button id="f-button"> follow </button>
        </form>
    );
}
