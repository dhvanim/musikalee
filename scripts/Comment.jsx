import * as React from 'react';
import PropTypes from 'prop-types';

export default function Comment(props) {
    const comment= props.comment;
    
    return (
        <div className="comment">
            <p> <b>{comment.username}</b> <i>{comment.datetime}</i><br/>
                {comment.text} 
            </p>
        </div>
    );
}

Comment.propTypes = {
  comment: PropTypes.any.isRequired,
};
