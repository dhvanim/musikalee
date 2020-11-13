import * as React from 'react';
import SpotifyLogin from 'react-spotify-login';
import { Socket } from './Socket';

const onSuccess = (response) => {
  console.log( response );
  Socket.emit('new spotify user', {
    token: response.access_token,
  });
};

export default function SpotifyButton() {
  return (
    <div className="loginpage">
      <SpotifyLogin
        clientId="d1252102702f4ae4bbadc59e907a87da"
        /* redirectUri={process.env.uri} */
        redirectUri="https://63493edfefe54691b206383fc43f796b.vfs.cloud9.us-east-1.amazonaws.com"
        onSuccess={onSuccess}
        scope="user-read-email user-top-read user-follow-read user-read-currently-playing"
        className="spotifybutton"
      />
    </div>
  );
}
