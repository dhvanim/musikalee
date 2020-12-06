import * as React from 'react';
import { NavLink } from 'react-router-dom';

const down = React.createRef();
const up = React.createRef();

function handleScrollDown(event) {
  if(down.current){
    down.current.scrollIntoView({ 
     behavior: "smooth", 
     block: "nearest"
    });
  }
}

function handleScrollUp(event) {
  if(up.current){
    up.current.scrollIntoView({ 
     behavior: "smooth", 
     block: "nearest"
    });
  }
}

function Heading() {
  return (
    <div>

      <h1 className="title"> Musikalee </h1>
      <h4>Created by:</h4>
      <ul>
        <li> 
          Joseph Cayemitte 
          <a href="https://github.com/reo464" target="_blank"><i class="fab fa-github"></i></a> 
          <a href="https://www.linkedin.com/in/joseph-cayemitte-04638b1a1/" target="_blank"><i class="fab fa-linkedin"></i></a>
        </li>
        <li>
          Justin Chow
          <a href="https://github.com/Ju3T1N" target="_blank"><i class="fab fa-github"></i></a> 
          <a href="https://www.linkedin.com/in/justin-chow-721066127/" target="_blank"><i class="fab fa-linkedin"></i></a>
        </li>
        <li>
          Catarina DeMatos
          <a href="https://github.com/catdematos98" target="_blank"><i class="fab fa-github"></i></a> 
          <a href="https://www.linkedin.com/in/dematoscatarina/" target="_blank"><i class="fab fa-linkedin"></i></a>
        </li>
        <li>
          Dhvani Mistry
          <a href="https://github.com/dhvanim" target="_blank"><i class="fab fa-github"></i></a> 
          <a href="https://www.linkedin.com/in/dhvanimistry/" target="_blank"><i class="fab fa-linkedin"></i></a>
        </li>
      </ul>
      
      <button onClick={handleScrollDown}> <i class="fas fa-angle-down"></i> </button>
    </div>
  );
}
function OurProduct() {
  return (
    <div>
      <h1>About Musikalee</h1>
      <i>Our product, called Musikalee, is a blog for all of your music needs. </i>
      <p>On our app you can:</p>
      <ul>
        <li>Share music (some of which can even be played), artists, albums or playlists</li>
        <li>Interact with other users by liking or commenting on their post</li>
        <li>Visit your profile page to see your current playing song and top artists</li>
        <li>
          Get a list of currently trending songs, and some reccomendations curated just for you
        </li>
      </ul>
    </div>
  );
}
function TechUsed() {
  return (
    <div>
      <h2>Technologies Used</h2>
      <br />
      <ul>
        <li>React.js for our frontend</li>
        <li>Python for our webserver</li>
        <li>Flask to act as our webserver</li>
        <li>FlaskSqlAlchemy to manipulate our database</li>
        <li>SocketIO to connect our front and backend</li>
        <li>PostgresSQL to store our data</li>
        <li>Heroku to deploy our app</li>
        <li>CircleCI for continuous testing</li>
        <li>Spotify API for login and music data/functionality</li>
        <li>Ticketmaster API to find shows near you</li>
      </ul>
    </div>
  );
}

function Link() {
  return (
    <NavLink to="/">
      Back to Musikalee :-)
    </NavLink>
  );
}

export default function Landing() {
  return (
    <div className="landing">

      <div ref={up} className="heading">
        { Heading() }
      </div>

      <div ref={down} className="contentlanding">
      
        <button onClick={handleScrollUp}> <i class="fas fa-angle-up"></i> </button>

        <div className="product">
          { OurProduct() }
        </div>
        <br />
        <div className="tech">
          { TechUsed() }
        </div>

        <div className="link">
          { Link() }
        </div>

      </div>

    </div>
  );
}
