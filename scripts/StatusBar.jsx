import * as React from 'react';
import { Socket } from './Socket';

export default function StatusBar() {
    
    function submitPost(event) {
        let status = document.getElementById("text_status");
        console.log(status.value);
        
        status.value = '';
        event.preventDefault();
    }
    
    return (
        <div>
            <form onSubmit={submitPost}>
                <input type="text" id="text_status" placeholder="What are you listening to?" />
                <input type="submit" name="Send Post" />
            </form>
        </div>
    );
}