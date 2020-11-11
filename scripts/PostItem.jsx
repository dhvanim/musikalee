import * as React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';

import { Socket } from './Socket';
import CommentsSection from './CommentsSection';


export default function PostItem(props) {
    const id= props.id;
    const num_likes = props.likes
    
    
    const triggerSiblingExample = () => <span style={{float:"right"}}onClick={handleToggle}> <img style={icon} src={likeIcon}/> { num_likes } </span>;

    
    const triggerStyle={
        float:"right",
    }

    const [likeState, toggleLiked] = React.useState(false);

    const icon = {
        height: "20px",
        width: "20px",
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
                
                    <Collapsible trigger={<span> <img style={icon} src={"./static/comments.png"}/> { props.comments.length } </span>} triggerStyle={triggerStyle} overflowWhenOpen="auto" triggerSibling={triggerSiblingExample}>
                        <CommentsSection post_id={id} comments={props.comments}/>
                    </Collapsible>
                        
                    </div>
                <br />
            </li>
        </div>
    );
}
