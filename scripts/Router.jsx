import React, { Component } from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
 
import Home from './Home';
import UserProfile from './UserProfile';
import Messaging from './Messaging';
import Navigation from './Navigation';
 
export default function Router(){
    return (      
       <HashRouter>
        <div>
          <Navigation />
            <Switch>
             <Route path="/" component={Home} exact/>
             <Route path="/profile" component={UserProfile}/>
             <Route path="/messaging" component={Messaging}/>
            <Route component={Error}/>
           </Switch>
        </div> 
      </HashRouter>
    );
}
 