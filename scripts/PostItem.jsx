import * as React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';
import { useHistory } from "react-router-dom";

import { Socket } from './Socket';
import CommentsSection from './CommentsSection';
import PostMusic from './PostMusic';


export default function PostItem(props) {
    const id= props.id;
    const num_likes = props.likes;

    const triggerStyle={
        float:"right",
    };

    const icon = {
        height: "20px",
        width: "20px",
    };
    
    function handleToggle() {
        Socket.emit('like post', {
            id: id,
            num_likes: (props.is_liked? num_likes-1 : num_likes+1) 
        });
    }
    
    const history = useHistory();

    function goToUser(){
        console.log(props.username);
        Socket.emit("get profile", props.username);
        history.push("/profile");
    }

    var likeIcon = (props.is_liked? "./static/heart-filled.png" : "./static/heart-outline.png");

    const likeButton = () => <span style={{float:"right"}}onClick={handleToggle}> <img style={icon} src={likeIcon}/> { num_likes } </span>;
    
    function hasMusic(music_type) {
        if (music_type == "default" || music_type == null) {
            return <div></div>;
        }
        return <div> <PostMusic music={ props.music } musicType={props.music_type}/> <br /> </div>;
    }
    
    return (
        <div>
            <li key={props.id} className="post">
                <span className="pfp"> <img src={ props.pfp } /> </span> <br />
                <span className="username" onClick={goToUser}> { props.username } </span> <br /> <p> </p>
                { hasMusic( props.music_type) } 
                <span className="text"> { props.text } </span> <br />
                <span className="time"> { props.time } </span> 
                <div className="iconsContainer">
                
                    <Collapsible trigger={<span> <img style={icon} src={"./static/comments.png"}/> { props.comments.length } </span>} open={props.isCommentsOpen}triggerStyle={triggerStyle} overflowWhenOpen="auto" triggerSibling={likeButton}>
                        <CommentsSection post_id={id} comments={props.comments}/>
                    </Collapsible>
                        
                </div>
            </li>
        </div>
    );
}
