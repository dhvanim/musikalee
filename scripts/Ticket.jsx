import React from 'react';
import { Socket } from './Socket';
 
const Ticket = () => {
    
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
    
    return (
       <div className="page">
          <h1>Discover events near you!</h1>
          <form onSubmit={searchEvents}>
              <input type="text" id="zip_code" placeholder="Zipcode" maxLength="256" />
              <input type="text" id="artist_search" placeholder="Artist" maxLength="256" />
              <input type="submit" name="Search" />
          </form>
          
       </div>
    );
}
 
export default Ticket