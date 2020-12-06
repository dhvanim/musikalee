import * as React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import { Socket } from './Socket';

import SpotifyButton from './SpotifyButton';
import Home from './Home';
import UserProfile from './UserProfile';
import Ticket from './Ticket';

import Landing from './Landing';

export default function Content() {
  const [loggedIn, setLoggedIn] = React.useState(false);

  function getLoggedStatus() {
    React.useEffect(() => {
      let isMounted = true;
      Socket.on('login success', (data) => {
        if (isMounted) {
          const status = true;
          const { userinfo } = data;
          setLoggedIn(status);
          window.localStorage.setItem('userinfo', JSON.stringify(userinfo));
          window.localStorage.setItem('userstatus', true);
          Socket.emit('user logged in', true);
        }
      });
      return () => {
        Socket.off('login success', true);
        isMounted = false;
      };
    });
  }

  getLoggedStatus();

  return (
    <div>
      <HashRouter>
        <Switch>
          <div>
            <Route exact path="/">
              {loggedIn ? <Home /> : <SpotifyButton />}
            </Route>
            <Route path="/about" component={Landing} />
            <div className="content">
              <Route path="/profile" component={UserProfile} />
              <Route path="/ticket" component={Ticket} />
            </div>
          </div>
        </Switch>
      </HashRouter>
    </div>
  );
}
