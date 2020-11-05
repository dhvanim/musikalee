import * as React from 'react';
import { Socket } from './Socket';
import StatusBar from './StatusBar';
import Timeline from './Timeline'

export default function Home() {
    
    return (
        <div>
            <StatusBar />
            
            <Timeline />
        </div>
    );
}