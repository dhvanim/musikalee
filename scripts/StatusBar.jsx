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
    
    function dropdownselect() {
        var dropdown = document.getElementById("option");
        var song = document.getElementById("song");
        var artist = document.getElementById("artist");
        var album = document.getElementById("album");
        var playlist = document.getElementById("playlist");
        
        if (dropdown.value == "default") {
            song.style.display = "none";
            artist.style.display = "none";
            album.style.display = "none";
            playlist.style.display = "none";
        }
        
        if (dropdown.value == "song") {
            song.style.display = "block";
            artist.style.display = "block";
            album.style.display = "none";
            playlist.style.display = "none";
        }
        if (dropdown.value == "artist") {
            song.style.display = "none";
            artist.style.display = "block";
            album.style.display = "none";
            playlist.style.display = "none";
        }
        if (dropdown.value == "album") {
            song.style.display = "none";
            artist.style.display = "block";
            album.style.display = "block";
            playlist.style.display = "none";
        }
        if (dropdown.value == "playlist") {
            song.style.display = "none";
            artist.style.display = "none";
            album.style.display = "none";
            playlist.style.display = "block";
        }
    }
    
    return (
        <div className="statusbar">
            <form onSubmit={submitPost}>
                <input type="text" id="text_status" placeholder="What are you listening to?" maxLength="256" required />
                <select id="option" name="option" onClick={dropdownselect}>
                    <option value="default"> Media Type </option>
                    <option value="song"> Song </option>
                    <option value="artist"> Artist </option>
                    <option value="album"> Album </option>
                    <option value="playlist"> Playlist </option>
                </select>
                
                <input type="text" id="song" placeholder="Enter Song" maxLength="500"/>
                <input type="text" id="artist" placeholder="Enter Artist" maxLength="500"/>
                <input type="text" id="album" placeholder="Enter Album" maxLength="500"/>
                <input type="text" id="playlist" placeholder="Enter Playlist Link" maxLength="500"/>
                
                <input type="submit" name="Send Post" />
            </form>
        </div>
    );
}