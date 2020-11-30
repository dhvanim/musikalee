import React, { Component } from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
 
import Home from './Home';
import UserProfile from './UserProfile';
import Ticket from './Ticket';
import Navigation from './Navigation';
 
export default function Router(){
    return (      
       <HashRouter>
        <div>
          <Navigation />
            <Switch>
             <Route path="/" component={Home} exact/>
             <Route path="/profile" component={UserProfile}/>
             <Route path="/ticket" component={Ticket}/>
            <Route component={Error}/>
           </Switch>
        </div> 
      </HashRouter>
    );
}
 