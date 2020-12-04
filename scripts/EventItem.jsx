import React from 'react';
import PropTypes from 'prop-types';

export default function EventItem(props) {
  const { image, name, venue, date, url } = props;

  return (
    <div className="eventItem">
      <img alt=".png" src={image} className="album_art" />
      <p className="title">
        {name}
      </p>
      <p className="location">
        {venue}
      </p>
      <p className="datetime">
        {date}
      </p>
      <button type="button" className="buyLink" onClick={() => window.open(url, '_blank')}> Buy Tickets</button>

    </div>
  );
}

EventItem.propTypes = {
  image: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  venue: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};
