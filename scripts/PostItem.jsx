import * as React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';

import { Socket } from './Socket';
import CommentsSection from './CommentsSection';


export default function PostItem(props) {
    const id= props.id;
    const num_likes = props.likes

    const [likeState, toggleLiked] = React.useState(false);

    const icon = {
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
    
    var likeIcon = (likeState? "./static/heart-filled.png" : "./static/heart-outline.png")
    return (
        
        <div>
            <li key={props.id} className="post">
                <span className="username"> { props.username } </span> <br />
                <span className="text"> { props.text } </span> <br />
                <span className="time"> { props.time } </span> 
                <div className="iconsContainer">
                    <div className="comments">
                        <Collapsible trigger={<span> <img style={icon} src={"./static/comments.png"}/> { 0 } </span>}>
                            <CommentsSection comments={props.comments}/>
                        </Collapsible>
                    </div>
                    <span className="likes" onClick={handleToggle}> <img style={icon} src={likeIcon}/> { num_likes } </span> <br />
                </div>
            </li>
        </div>
    );
}
