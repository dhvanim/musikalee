import * as React from 'react';
import PropTypes from 'prop-types';

export default function PostMusic(props) {
  const { music } = props;
  const { musicType } = props;

  if (musicType === 'song') {
    return (
      <div className="postmusic">
        <span>
          <a href={music.external_link} target="_blank" rel="noreferrer">
            <img src={music.album_art} className="album_art" alt={music.album} />
          </a>
          <b>
            { music.song }
          </b>
          <br />
          { music.album }
          <br />
          { music.artist }
          <br />
          { music.preview_url != null
            ? (
              <audio controls name="media">
                <source src={music.preview_url} type="audio/mpeg" />
              </audio>
            )
            : <div />}
        </span>
      </div>
    );
  }

  if (musicType === 'artist') {
    return (
      <div className="postmusic">
        <span>
          <a href={music.external_link} target="_blank" rel="noreferrer">
            <img src={music.artist_icon} className="album_art" alt={music.artist_name} />
          </a>
          <h3>
            { music.artist_name }
          </h3>
        </span>
      </div>
    );
  }

  if (musicType === 'album') {
    return (
      <div className="postmusic">
        <span>
          <a href={music.external_link} target="_blank" rel="noreferrer">
            <img src={music.album_art} className="album_art" alt={music.album} />
          </a>
          <b>
            { music.album_name }
          </b>
          <br />
          { music.artists }
          <br />
          <br />
          { music.total_tracks }
          
          Tracks || Released:
          { music.release_date }
        </span>
      </div>
    );
  }

  if (musicType === 'playlist') {
    return (
      <div className="postmusic">
        <span>
          <a href={music.external_link} target="_blank" rel="noreferrer">
            <img src={music.playlist_art} className="album_art" alt={music.playlist_name} />
          </a>
          <b>
            { music.playlist_name }
          </b>
          
          <br />
          <i>
            { music.playlist_desc }
          </i>
          
          by
          { music.playlist_owner }
          
          <br />
          <br />
          { music.followers }
          Followers
        </span>
      </div>
    );
  }

  return (
    <div> </div>
  );
}

PostMusic.propTypes = {
  music: PropTypes.node.isRequired,
  musicType: PropTypes.string.isRequired,
};
