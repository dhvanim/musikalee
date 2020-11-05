import * as React from 'react';
import { Socket } from './Socket';
import StatusBar from './StatusBar';
import Timeline from './Timeline'

export function Content() {
   
    return (
        <div>
            <StatusBar />
            
            <Timeline />
        </div>
    );
}