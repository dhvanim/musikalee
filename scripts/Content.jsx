import * as React from 'react';
import { Socket } from './Socket';

import Router from './Router';
import SpotifyButton from './SpotifyButton'


export function Content() {
    
    const [loggedIn, setLoggedIn] = React.useState(false);
    
    function getLoggedStatus() {
        React.useEffect( () => {
            Socket.on('login success', updateLoggedStatus);
            return () => {
                Socket.off('login success', updateLoggedStatus);
            };
        });
    }
    
    function updateLoggedStatus(data) {
        setLoggedIn( data );
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