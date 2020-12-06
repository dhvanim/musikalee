import * as React from 'react';
import StatusBar from './StatusBar';
import Timeline from './Timeline';
import RightSideBar from './RightSideBar';
import Navigation from './Navigation';

export default function Home() {
  return (
    <div>
      <Navigation />
      <div className="content">
        <RightSideBar />
        <div className="middle">
          <StatusBar />
          <div id="spacer20"> </div>
          <Timeline />
        </div>

      </div>
    </div>
  );
}
