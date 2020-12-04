import * as React from 'react';
import StatusBar from './StatusBar';
import Timeline from './Timeline';
import RightSideBar from './RightSideBar';

export default function Home() {
  return (
    <div className="home">
      <StatusBar />
      <RightSideBar />
      <Timeline />

    </div>
  );
}
