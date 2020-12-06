import React from 'react';
import PropTypes from 'prop-types';

export default function EventItem(props) {
  const {
    image, name, venue, date, url,
  } = props;

  return (
    <div>
      <div className="eventItem">
        <button className="buyLink" onClick={() => window.open(url, '_blank')} type="button"> Buy Tickets</button>
        <img src={image} className="image" alt={image} />
        <span className="title">

          {name}

        </span>

        <br />
        <span className="location">

          {venue}

        </span>

        <br />
        <span className="datetime">

          {date}

        </span>

        <br />
      </div>
      <div id="spacer5" />
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
