import * as React from 'react';
import { Socket } from './Socket';

import Router from './Router';
import SpotifyButton from './SpotifyButton'


export function Content() {
    
    const [loggedIn, setLoggedIn] = React.useState(false);
   
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