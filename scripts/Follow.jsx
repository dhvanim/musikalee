import * as React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import { Socket } from './Socket';

export default function Follow(props) {
  const { isFollowed } = props;

  function handleSubmit(event) {
    if (isFollowed) {
      const element = 'Follow';
      ReactDOM.render(element, document.getElementById('f-button'));

      Socket.emit('recieve follower data');
    } else {
      const element = 'Unfollow';
      ReactDOM.render(element, document.getElementById('f-button'));

      Socket.emit('recieve follower data');
    }

    event.preventDefault();
  }

  return (
    <form onSubmit={handleSubmit}>
      <button id="f-button" type="button"> follow </button>
    </form>
  );
}

Follow.propTypes = {
  isFollowed: PropTypes.bool.isRequired,
};
