import React, { Component } from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
 
import Timeline from './Timeline';
import UserProfile from './UserProfile';
import Messaging from './Messaging';
import Navigation from './Navigation';
 
export default function Router(){
    return (      
       <HashRouter>
        <div>
          <Navigation />
            <Switch>
             <Route path="/" component={Timeline} exact/>
             <Route path="/profile" component={UserProfile}/>
             <Route path="/messaging" component={Messaging}/>
            <Route component={Error}/>
           </Switch>
        </div> 
      </HashRouter>
    );
}
 