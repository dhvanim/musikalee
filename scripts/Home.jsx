import * as React from 'react';
import StatusBar from './StatusBar';
import Timeline from './Timeline';
import RightSideBar from './RightSideBar';

export default function Home() {
    return (
        <div>
            <RightSideBar />
            <div className="middle">
                <StatusBar />     
                <div id="spacer20"> </div>
                <Timeline />
            </div>    
        </div>
    );
}
