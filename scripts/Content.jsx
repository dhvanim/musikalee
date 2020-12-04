import * as React from 'react';
import { Socket } from './Socket';

import Router from './Router';
import SpotifyButton from './SpotifyButton';


export function Content() {
    
    const [loggedIn, setLoggedIn] = React.useState(false);
    
    function getLoggedStatus() {
        React.useEffect( () => {
            let isMounted = true;
            Socket.on('login success', (data) => {
                if (isMounted) {
                    let status = data['status'];
                    let userinfo = data['userinfo'];
                    setLoggedIn( status );
                    window.localStorage.setItem('userinfo', JSON.stringify(userinfo));
                    Socket.emit("user logged in", true);
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
            { loggedIn == false ?
            <SpotifyButton />
            : 
            <Router/>
            }
        </div>
    );
}