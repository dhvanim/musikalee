import * as React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';

import { Socket } from './Socket';
import CommentsSection from './CommentsSection';


export default function PostItem(props) {
    const id= props.id;
    const num_likes = props.likes
    
    const triggerSiblingExample = () => <div className="Collapsible__custom-sibling">This is a sibling to the trigger which wont cause the Collapsible to open!</div>;

    
    const triggerStyle={
        float:"right",
        background: '#6821f3'
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
                
                    <Collapsible trigger={<span> <img style={icon} src={"./static/comments.png"}/> { 0 } </span>} triggerStyle={triggerStyle} overflowWhenOpen="scroll">
                        <CommentsSection post_id={id} comments={props.comments}/>
                    </Collapsible>
                
                    <span onClick={handleToggle}> <img style={icon} src={likeIcon}/> { num_likes } </span> <br />
                </div>
                <br />
            </li>
        </div>
    );
}
