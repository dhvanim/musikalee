import * as React from 'react';
import { Socket } from './Socket';

import PostItem from "./PostItem"

export default function Timeline() {
    
    const [posts, setPosts] = React.useState([]);
//     => {
//     const stickyValue = window.localStorage.getItem("posts");
//     return stickyValue !== null
//       ? JSON.parse(stickyValue)
//       : [];
//   });
    
    function getPosts() {
        React.useEffect( () => {
            Socket.on('emit posts channel', (posts) => {setPosts( posts );});
            return () => {
                Socket.off('emit posts channel', true);
            };
        });
    }
    
    
    getPosts();
    
    function getNewPost() {
        React.useEffect( () => {
            Socket.on('emit new post channel', (new_post) => {
                setPosts([new_post].concat(posts));
                console.log("NEW POST",new_post)
            });
            return () => {
                Socket.off('emit new post channel',true);
            };
        });
    }

    getNewPost() 

    function updateLikes() {
        React.useEffect( () => {
            Socket.on('like post channel', (data) => {
                const num_likes = {num_likes: data.num_likes};
                const is_liked = {is_liked: data.is_liked};
                console.log(data);
                let Newposts = posts.map(el => (el.id === data.post_id ? Object.assign({}, el, num_likes, is_liked) : el));
                console.log(Newposts);
                setPosts(
                 Newposts
                );
            });
            return () => {
                Socket.off('like post channel', true);
            };
        });
    }
    
    updateLikes()

    return (
        <div>
        <ul className="timeline">
            { 
                posts.map( (post, index) => (
                    <PostItem key={index} id={post.id} username={post.username} text={post.message} time={post.datetime} likes={post.num_likes} is_liked={post.is_liked} comments={post.comments} pfp={post.pfp} music={post.music}/>
                ))    
            }
        </ul>
        </div>
    );
}
