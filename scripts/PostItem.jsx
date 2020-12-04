import * as React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';
import { useHistory } from 'react-router-dom';

import { Socket } from './Socket';
import CommentsSection from './CommentsSection';
import PostMusic from './PostMusic';

export default function PostItem(props) {
  const {
    id, username, text, time, likes, isLiked, comments, isCommentsOpen, pfp, music, musicType,
  } = props;

  const triggerStyle = {
    float: 'right',
  };

  const icon = {
    height: '20px',
    width: '20px',
  };

  function handleToggle() {
    Socket.emit('like post', {
      id,
      num_likes: (isLiked ? likes - 1 : likes + 1),
    });
  }

  const history = useHistory();

  function goToUser() {
    Socket.emit('get profile', username);
    history.push('/profile');
  }

  const likeIcon = (isLiked ? './static/heart-filled.png' : './static/heart-outline.png');

  const likeButton = () => (
    <span style={{ float: 'right' }} onClick={handleToggle} onKeyDown={handleToggle}>
      {' '}
      <img style={icon} src={likeIcon} alt="" />
      {' '}
      { likes }
      {' '}
    </span>
  );

  function hasMusic(media) {
    if (media === 'default' || media === null) {
      return <div />;
    }
    return (
      <div>
        {' '}
        <PostMusic music={music} musicType={media} />
        {' '}
        <br />
        {' '}
      </div>
    );
  }

  return (
    <div>
      <li key={id} className="post">
        <span className="pfp">
          {' '}
          <img src={pfp} alt={username} />
          {' '}
        </span>
        {' '}
        <br />
        <h4 className="username" onClick={goToUser} onKeyDown={goToUser}> 
          {' '}
          { username }
          {' '}
        </h4>
        {' '}
        <div id="spacer5"></div>
        { hasMusic(musicType) }
        <div className="text">
          {' '}
          { text }
          {' '}
        </div>
        {' '}
        <br />
        <span className="time">
          {' '}
          { time }
          {' '}
        </span>
        <div className="iconsContainer">

          <Collapsible
            trigger={(
              <span>
                {' '}
                <img style={icon} src="./static/comments.png" alt="" />
                {' '}
                { comments.length }
                {' '}
              </span>
)}
            open={isCommentsOpen}
            triggerStyle={triggerStyle}
            overflowWhenOpen="auto"
            triggerSibling={likeButton}
          >
            <br/>
            <CommentsSection post_id={id} comments={comments} />
          </Collapsible>

        </div>
        <br />
      </li>
    </div>
  );
}

PostItem.propTypes = {
  id: PropTypes.any.isRequired,
  username: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  time: PropTypes.any.isRequired,
  likes: PropTypes.number.isRequired,
  isLiked: PropTypes.any.isRequired,
  comments: PropTypes.any.isRequired,
  isCommentsOpen: PropTypes.any.isRequired,
  pfp: PropTypes.string.isRequired,
  music: PropTypes.any.isRequired,
  musicType: PropTypes.any.isRequired,
};
