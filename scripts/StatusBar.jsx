import * as React from 'react';
import { Socket } from './Socket';

export default function StatusBar() {
    
    function submitPost(event) {
        let status = document.getElementById("text_status");
        let song = document.getElementById("song");
        let artist = document.getElementById("artist");
        
        Socket.emit('user post channel', {"text" :status.value,
                                            "song": song.value,
                                            "artist": artist.value
                    });
                    
        status.value = '';
        song.value = '';
        artist.value = '';
        
        event.preventDefault();
    }
    
    return (
        <div className="statusbar">
            <form onSubmit={submitPost}>
                <input type="text" id="text_status" placeholder="What are you listening to?" maxLength="256"/>
                <input type="text" id="song" placeholder="Enter Song" maxLength="500"/>
                <input type="text" id="artist" placeholder="Enter Artist" maxLength="500"/>
                <input type="submit" name="Send Post" />
            </form>
        </div>
    );
}