import * as React from 'react';
import { Socket } from './Socket';

import PostItem from "./PostItem"

export default function Timeline() {
    
    const [posts, setPosts] = React.useState(() => {
    const stickyValue = window.localStorage.getItem("posts");
    return stickyValue !== null
      ? JSON.parse(stickyValue)
      : [];
  });
    
    function getPosts() {
        React.useEffect( () => {
            Socket.on('emit posts channel', (posts) => {setPosts( posts );});
            window.localStorage.setItem("posts", JSON.stringify(posts));
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
                window.localStorage.setItem("posts", JSON.stringify(posts));

            });
            return () => {
                Socket.off('emit new post channel',true);
            };
        });
    }

    getNewPost() 

    function updateLikes() {
        React.useEffect( () => {
            let isMounted = true; // note this flag denote mount status to avoid "Can't perform a React state update on an unmounted component"
            Socket.on('like post channel', (data) => {
                if(isMounted){
                    const num_likes = {num_likes: data.num_likes};
                    const is_liked = {is_liked: data.is_liked};
                    let Newposts = posts.map(el => (el.id === data.post_id ? Object.assign({}, el, num_likes, is_liked) : el));
                    setPosts(
                     Newposts
                    );
                    window.localStorage.setItem("posts", JSON.stringify(posts));                    
                }
            });
            return () => {
                Socket.off('like post channel', true);
                isMounted = false;
            };
        });
    }
    
    updateLikes()
    
    function updateComments() {
        React.useEffect( () => {
            let isMounted = true; // note this flag denote mount status
            Socket.on('NEW COMMENT ON POST', (data) => {
                if (isMounted){
                    let Newposts = posts.map(el => (el.id === data.post_id ? Object.assign({}, el, {comments: [data.comment].concat(el.comments)}, {isCommentsOpen: true}) : el));
                    setPosts(
                     Newposts
                    );
                    window.localStorage.setItem("posts", JSON.stringify(posts));                    
                }

            })
            return () => {
                Socket.off('NEW COMMENT ON POST', true);
                isMounted = false;
            };
        });
    }
    
    updateComments()
    
    function getLocalStorage() {
        React.useEffect( () => {
            Socket.on('navigation change', (data) => {
                setPosts(window.localStorage.getItem("posts"));
            });
            return () => {
                Socket.off('navigation change', true);
            };
        });
    }

    getLocalStorage()
    return (
        <div>
        <ul className="timeline">
            { 
                posts.map( (post, index) => (
                    <PostItem key={index} id={post.id} username={post.username} text={post.message} time={post.datetime} likes={post.num_likes} is_liked={post.is_liked} comments={post.comments} isCommentsOpen={post.isCommentsOpen} pfp={post.pfp} music={post.music}/>
                ))    
            }
        </ul>
        </div>
    );
}
