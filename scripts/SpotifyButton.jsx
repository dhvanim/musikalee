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
    <SpotifyLogin
      clientId="803918090e2d4726a922c0f05862e6e7"
      redirectUri={process.env.uri}
      onSuccess={onSuccess}
      scope="user-read-email user-top-read user-follow-read"
    />
  );
}
