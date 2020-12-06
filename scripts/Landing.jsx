import * as React from 'react';
import { NavLink } from 'react-router-dom';

function Heading() {
  return (
    <div>

      <h1 className="title"> Musikalee </h1>
      <h4>Created by:</h4>
      <ul>
        <li>Joseph Cayemitte</li>
        <li>Justin Chow</li>
        <li>Catarina DeMatos</li>
        <li>Dhvani Mistry</li>
      </ul>
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
        <li>Interact with other people by liking or commenting on their post</li>
        <li>Visit your profile page to see your current playing song</li>
        <li>
          Get a list of currently trending songs, and even some reccomendations curated just for you
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

      <div className="heading">
        { Heading() }
      </div>

      <div className="contentlanding">

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
