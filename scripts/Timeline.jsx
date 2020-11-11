import * as React from 'react';
import { Socket } from './Socket';

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
    }
    
    getPosts();
    
    return (
        <div className="timeline">
        <ul>
            { posts.map( (post, index) => (
                <li key={index} className="post">
                    <span className="pfp"> <img src={ post.pfp } /> </span> <br />
                    <span className="username"> { post.username } </span> <br />
                    <span className="text"> { post.text } </span> <br />
                    
                    <span className="time"> { post.time } </span> 
                    <span className="likes"> &hearts; { post.num_likes } </span> <br />
                
                </li>
                ))
            }
        </ul>
        </div>
    );
}
