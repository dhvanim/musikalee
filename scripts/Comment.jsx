import * as React from 'react';
import PropTypes from 'prop-types';

export default function Comment(props) {
  const { comment } = props;

  return (
    <div className="comment">
      <p>
        {comment.username}
        {comment.datetime}
        <br />
        {comment.text}
      </p>
    </div>
  );
}

Comment.propTypes = {
  comment: PropTypes.node.isRequired,
};
