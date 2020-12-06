import * as React from 'react';
import PropTypes from 'prop-types';

export default function PostMusic(props) {
  const { music, musicType } = props;

  if (musicType === 'song') {
    return (
      <div className="postmusic">
        <span>
          <a href={music.external_link} target="_blank" rel="noreferrer">
            <img src={music.album_art} className="album_art" alt={music.album} />
          </a>
          <h3>

            { music.song }

          </h3>
          <span>
            { music.album }

            <br />
            { music.artist }
          </span>
          {' '}
          <br />
          { music.preview_url != null
            ? (
              <div className="audio">
                <audio controls name="media">
                  <source src={music.preview_url} type="audio/mpeg" />
                </audio>
              </div>
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
          <h1>

            { music.artist_name }

          </h1>
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
          <h4>
            { music.album_name }
          </h4>
          <br />
          { music.artists }
          <br />
          { music.total_tracks }
          Tracks || Released:
          {' '}
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
          <h3>
            { music.playlist_name }
          </h3>
          <i>
            { music.playlist_desc }
          </i>
          by
          {' '}
          { music.playlist_owner }
          <br />
          { music.followers }
          {' '}
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
  music: PropTypes.any.isRequired,
  musicType: PropTypes.string.isRequired,
};
