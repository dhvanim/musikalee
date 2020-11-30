import React from 'react';
import { Socket } from './Socket';
 
export default function Ticket(){
    const [events, setEvents] = React.useState([]);
        
    function searchEvents(event) {
        let zipcode = document.getElementById("zip_code");
        let artist = document.getElementById("artist_search");

        Socket.emit('search ticketmaster', {"zipcode" :zipcode.value,
                                            "artist": artist.value
                    });
                    
        zipcode.value = '';
        artist.value = '';
        
        event.preventDefault();
    }
    
    function getEvents() {
        React.useEffect( () => {
            Socket.on('display events', (events) => {setEvents( events );});
            return () => {
                Socket.off('display events', true);
            };
        });
    }
    
    getEvents()
    
    return (
       <div className="page">
          <h1>Discover events near you!</h1>
          <form onSubmit={searchEvents}>
              <input type="text" id="zip_code" placeholder="Zipcode" maxLength="256" />
              <input type="text" id="artist_search" placeholder="Artist" maxLength="256" />
              <input type="submit" name="Search" />
          </form>
          
        <ul className="events">
            { 
                events.map( (event, index) => (
                    <p key={index}> {event.name} </p>
                ))    
            }
        </ul>
          
       </div>
    );
}
 