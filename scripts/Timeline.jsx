import * as React from 'react';
import { Socket } from './Socket';

import PostItem from "./PostItem"

export default function Timeline() {
    
    const [posts, setPosts] = React.useState([]); 
    
    function getPosts() {
        React.useEffect( () => {
            Socket.on('emit posts channel', updatePosts);
            return () => {
                Socket.off('emit posts channel', updatePosts);
            };
        });
    }
    
    function updatePosts(data) {
        setPosts( [data].concat(posts) );
        console.log( [data].concat(posts) );
    }
    
    getPosts();
    
    return (
        <div>
        <ul className="timeline">
            { posts.map( (post, index) => (
                <PostItem key={index} id={post.id} username={post.username} pfp={post.pfp} text={post.text} time={post.time} likes={post.num_likes} />
            ))}
        </ul>
        </div>
    );
}
