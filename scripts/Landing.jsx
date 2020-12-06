import * as React from 'react';

export function WhoAreWe() {
  return (
    <div>
      <h2>Who We Are:</h2>
      <ul>
        <li>Joseph Cayemitte</li>
        <li>Justin Chow</li>
        <li>Catarina DeMatos</li>
        <li>Dhvani Mistry</li>
      </ul>
    </div>
  );
}
export function OurProduct() {
  return (
    <div>
      <h2>About Our Product</h2>
      <p>Our product, called Musikalee is a blog for all of your music needs.</p>
      <p>On our App you Can:</p>
      <ul>
        <li>Post music (some of whcich can even be played), albums or a playlist</li>
        <li>Interact with other people&#39;s posts by liking or commenting on their post</li>
        <li>Visit your profile pae to see your current songs</li>
        <li>Get a list of currently trending songs, and even some reccomendations just for you</li>
      </ul>
    </div>
  );
}
export function TechUsed() {
  return (
    <div>
      <h2>Technologies Used</h2>
      <p>In our product we used these technologies:</p>
      <ul>
        <li>React.js for our frontend</li>
        <li>Python for our webserver</li>
        <li>Flask to act as our webserver</li>
        <li>FlaskSqlAlchemy to manipulate our database</li>
        <li>SocketIO to connect our react and python</li>
        <li>PostgresSQL to store our data</li>
        <li>Heroku to deploy our app</li>
        <li>CircleCI for continuous testing</li>
        <li>Spotify API for login and also music functionality</li>
        <li>Ticketmaster API to find shows near you</li>
      </ul>
    </div>
  );
}

export function Link() {
  return (
    <a href="https://musikalee.herokuapp.com/">
      Link to our app, though you are already here
    </a>
  );
}
