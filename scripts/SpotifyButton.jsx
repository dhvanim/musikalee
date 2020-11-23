import * as React from 'react';
import SpotifyLogin from 'react-spotify-login';
import { Socket } from './Socket';

const onSuccess = (response) => {
  //console.log( response );
  Socket.emit('new spotify user', {
    token: response.access_token,
  });
};

export default function SpotifyButton() {
  return (
    <div className="loginpage">
      <SpotifyLogin
        clientId="803918090e2d4726a922c0f05862e6e7"
        /* redirectUri={process.env.uri} */
        redirectUri="https://musikalee.herokuapp.com"
        onSuccess={onSuccess}
        scope="user-read-email user-top-read user-follow-read user-read-currently-playing"
        className="spotifybutton"
      />
    </div>
  );
}
