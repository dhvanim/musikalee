import * as React from 'react';

export default function PostItem(props) {
    const music = props.music;
    const music_type = props.music_type;
    
    if (music_type == "default" || music == null) {
        return "";
    }
    
    if (music_type == "song") {

        return (
            
            <div className="postmusic">
                   <span> 
                        <a href={music.external_link} target="_blank">
                            <img src={music.album_art} className="album_art" />
                        </a>
                        { music.song } <br />
                        { music.album } <br />
                        { music.artist } <br /> <br />
                        { music.preview_url != null ?
                        <audio controls name="media">
                                <source src={ music.preview_url } type="audio/mpeg" />
                        </audio>
                        :
                        <br />
                        }
                    </span>
                </div>
            );
    }
    
    if (music_type == "artist") {
        return (
            <div className="postmusic">
                <span>
                    <a href={music.external_link} target="_blank">
                        <img src={music.artist_icon} className="album_art" />
                    </a>
                    { music.artist_name }
                </span>
            </div>
        );
    }
    
    if (music_type == "album") {
        return (
            <div className="postmusic">
                <span> 
                        <a href={music.external_link} target="_blank">
                            <img src={music.album_art} className="album_art" />
                        </a>
                        { music.album_name } <br />
                        { music.artists } <br /> <br />
                        { music.total_tracks } Tracks || Released: { music.release_date }
                </span>
            </div>
        );
    }
    
    if (music_type == "playlist") {
        return (
            <div className="postmusic">
                <span> 
                        <a href={music.external_link} target="_blank">
                            <img src={music.playlist_art} className="album_art" />
                        </a>
                        { music.playlist_name } <br />
                        { music.playlist_desc } by { music.playlist_owner } <br /> <br />
                        { music.followers } Followers
                    </span>
            </div>
        );
    }
}