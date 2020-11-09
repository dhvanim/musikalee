import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';

export default function PostItem(props) {
    const id= props.id;
    const num_likes = props.likes

    const [likeState, toggleLiked] = React.useState(false);

    const likeIcon = {
        height: "20px",
        width: "20px"
    }
    
    function handleToggle() {
        let localLiked = likeState; 
        localLiked = !localLiked
        toggleLiked(localLiked); 
        
        Socket.emit('like post', {
            id: id,
            num_likes: (localLiked? num_likes+1 : num_likes-1) 
        });
        
    }

    var icon = (likeState? "./static/heart-filled.png" : "./static/heart-outline.png")
    return (
        
        <div>
            <li key={props.id} className="post">
                <span className="username"> { props.username } </span> <br />
                <span className="text"> { props.text } </span> <br />
                <span className="time"> { props.time } </span> 
                <span className="likes" onClick={handleToggle}> <img style={likeIcon} src={icon}/> { num_likes } </span> <br />
            </li>
        </div>
    );
}
