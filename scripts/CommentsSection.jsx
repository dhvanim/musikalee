import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';
import Comment from './Comment';

export default function CommentsSection(props) {
    const comments= props.comments;
    const post_id= props.post_id;
    
    function getUserInfo() {
        let data = window.localStorage.getItem("userinfo");
        return JSON.parse(data);
    }
    
    function postComment() {
        let comment = document.getElementById(post_id);
        let user = getUserInfo();
        Socket.emit('post comment', {
            comment: comment.value,
            post_id: props.post_id,
            'username':user['username']
        });
        
        comment.value = '';
        event.preventDefault();
    }
    return (
        
        <div className="commentsSection">
            <form onSubmit={postComment}>
                <input type="text" id={post_id}  maxLength="256"/>
                <input type="submit" name="Comment" value="Comment" />
            </form>
            { 
                comments.map( (comment, index) => (
                    <Comment key = {index} comment={comment}> </Comment>
                ))   
            }
    </div>
  );
}

CommentsSection.propTypes = {
  postId: PropTypes.any,
  comments: PropTypes.any,
};
