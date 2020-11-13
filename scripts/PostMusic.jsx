import * as React from 'react';

export default function PostItem(props) {
    const music = props.music;
    
    console.log(music);
    
    if (music == "") {
        return "";
    }

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