import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';

export default function PostItem(props) {
    const [likeState, toggleLiked] = React.useState({
        liked: false,
        num_likes: props.likes
    });
    
    
    const likeIcon = {
        height: "20px",
        width: "20px"
    }
    
    function handleToggle() {
        let localLiked = likeState.liked; 
        localLiked = !localLiked
        toggleLiked({
            liked: localLiked,
            num_likes: (localLiked? likeState.num_likes+1 : likeState.num_likes-1)
        }); 
        
        //TODO: emit post_id and num_likes to update DB with num_likes for this post. 
    }

    var icon = (likeState.liked? "./static/heart-filled.png" : "./static/heart-outline.png")
    return (
        
        <div>
            <li key={props.id} className="post">
                <span className="username"> { props.username } </span> <br />
                <span className="text"> { props.text } </span> <br />
                <span className="time"> { props.time } </span> 
                <span className="likes" onClick={handleToggle}> <img style={likeIcon} src={icon}/> { likeState.num_likes } </span> <br />
            </li>
        </div>
    );
}
