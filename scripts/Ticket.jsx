import React from 'react';
import Pagination from 'react-bootstrap/Pagination';
import { Socket } from './Socket';
import EventItem from './EventItem';

export default function Ticket() {
  const [events, setEvents] = React.useState([]);
  const [page, setPage] = React.useState(0);
  const [pageItems, setPageItems] = React.useState([]);
  const [searchParams, setSearchParams] = React.useState({
    zipcode: '',
    artist: '',
  });

  function getEnteredValues(event) {
    let enteredZipcode = document.getElementById('zip_code').value;
    let enteredArtist = document.getElementById('artist_search').value;

    setSearchParams({ zipcode: enteredZipcode, artist: enteredArtist });
    setPage(0);
    setPageItems([]);

    Socket.emit('search ticketmaster', {
      zipcode: enteredZipcode,
      artist: enteredArtist,
      page: 0,
    });

    enteredZipcode = '';
    enteredArtist = '';

    event.preventDefault();
  }
  function searchEvents(zipcode, artist, currPage) {
    Socket.emit('search ticketmaster', {
      zipcode: searchParams.zipcode,
      artist: searchParams.artist,
      page: currPage,
    });
  }

  function getEvents() {
    React.useEffect(() => {
      Socket.on('display events', (events) => {
        setEvents(events);
        if (events.length !== 0) {
          const active = page;
          const items = [];
          for (let number = 1; number <= events[0].totalPages; number += 1) {
            items.push(
              <Pagination.Item className="pageItem" key={number} active={number === active}>
                {number}
              </Pagination.Item>,
            );
          }
          setPageItems(items);
        }
      });
      return () => {
        Socket.off('display events', true);
      };
    });
  }

  function pageChanged(e) {
    const clickedPage = e.target.text;

    if (clickedPage !== 'undefined') {
      setPage(clickedPage);
      searchEvents(searchParams.zipcode, searchParams.artist, clickedPage - 1);
    }
  }

  getEvents();
  return (
    <div className="page">
      <h1>Discover events near you!</h1>
      <form onSubmit={getEnteredValues}>
        <input type="text" id="zip_code" placeholder="Zipcode" maxLength="256" />
        <input type="text" id="artist_search" placeholder="Artist" maxLength="256" />
        <input type="submit" name="Search" />
      </form>

      <ul className="events">
        {
                events.map((event, index) => (
                  <EventItem
                    key={index}
                    name={event.name}
                    image={event.image}
                    url={event.url}
                    date={event.date}
                    venue={event.venue}
                  />
                ))
            }
      </ul>

      <div className="eventsPages">
        <Pagination onClick={pageChanged}>{pageItems}</Pagination>
      </div>
    </div>
  );
}
