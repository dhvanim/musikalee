import * as React from 'react';
import SpotifyLogin from 'react-spotify-login';
import { Socket } from './Socket';

const onSuccess = (response) => {
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
        redirectUri="https://ba2b92cae00441b99d7f2c060261fb76.vfs.cloud9.us-east-1.amazonaws.com/"
        onSuccess={onSuccess}
        scope="user-read-email user-top-read user-follow-read user-read-currently-playing"
        className="spotifybutton"
      />
    </div>
  );
}
