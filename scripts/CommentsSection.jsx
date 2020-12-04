import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';
import Comment from './Comment';

export default function CommentsSection(props) {
  const { comments, postId } = props;

  function getUserInfo() {
    const data = window.localStorage.getItem('userinfo');
    return JSON.parse(data);
  }

  function postComment(event) {
    const comment = document.getElementById(postId);
    const user = getUserInfo();
    Socket.emit('post comment', {
      comment: comment.value,
      post_id: props.postId,
      username: user.username,
    });

    comment.value = '';
    event.preventDefault();
  }
  return (

    <div className="commentsSection">
      <form onSubmit={postComment}>
        <input type="text" id={postId} maxLength="256" />
        <input type="submit" name="Comment" />
      </form>
      {
                comments.map((comment, index) => (
                  <Comment key={index} comment={comment}> </Comment>
                ))
            }
    </div>
  );
}

CommentsSection.propTypes = {
  postId: PropTypes.node.isRequired,
  comments: PropTypes.any.isRequired,
};
