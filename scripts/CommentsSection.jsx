import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';

export default function CommentsSection(props) {
    const comments= props.comments;
    const post_id= props.post_id;

    function postComment() {
        let comment = document.getElementById(post_id);
        
        Socket.emit('post comment', {
            comment: comment.value,
            post_id: props.post_id
        });
        
        comment.value = '';
        event.preventDefault();
    }
    return (
        
        <div className="commentsSection">
            { comments.map( (comment, index) => (
                <p key = {index}> {comment.text} </p>
                ))    
            }
            <form onSubmit={postComment}>
                <input type="text" id={post_id}  maxLength="256"/>
                <input type="submit" name="Comment" />
            </form>
        </div>
    );
}
