import * as React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';

import { Socket } from './Socket';
import CommentsSection from './CommentsSection';
import PostMusic from './PostMusic';


export default function PostItem(props) {
    const id= props.id;
    const num_likes = props.likes

    const triggerStyle={
        float:"right",
    }

    const icon = {
        height: "20px",
        width: "20px",
    }
    
    function handleToggle() {
        Socket.emit('like post', {
            id: id,
            num_likes: (props.is_liked? num_likes-1 : num_likes+1) 
        });
        
    }
    
    var likeIcon = (props.is_liked? "./static/heart-filled.png" : "./static/heart-outline.png")

    const likeButton = () => <span style={{float:"right"}}onClick={handleToggle}> <img style={icon} src={likeIcon}/> { num_likes } </span>;
    
    return (
        
        <div>
            <li key={props.id} className="post">
                <span className="pfp"> <img src={ props.pfp } /> </span> <br />
                <span className="username"> { props.username } </span> <br /> <p> </p>
                <PostMusic music={ props.music } /> <br />
                <span className="text"> { props.text } </span> <br />
                <span className="time"> { props.time } </span> 
                <div className="iconsContainer">
                
                    <Collapsible trigger={<span> <img style={icon} src={"./static/comments.png"}/> { props.comments.length } </span>} triggerStyle={triggerStyle} overflowWhenOpen="auto" triggerSibling={likeButton}>
                        <CommentsSection post_id={id} comments={props.comments}/>
                    </Collapsible>
                        
                </div>
            </li>
        </div>
    );
}
