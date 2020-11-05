import * as React from 'react';
import { Socket } from './Socket';

export default function StatusBar() {
    
    function submitPost(event) {
        let status = document.getElementById("text_status");
        
        Socket.emit('user post channel', status.value);
        
        status.value = '';
        event.preventDefault();
    }
    
    return (
        <div className="statusbar">
            <form onSubmit={submitPost}>
                <input type="text" id="text_status" placeholder="What are you listening to?" maxLength="256"/>
                <input type="submit" name="Send Post" />
            </form>
        </div>
    );
}