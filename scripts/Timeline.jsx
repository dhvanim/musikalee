import * as React from 'react';
import { Socket } from './Socket';

import PostItem from './PostItem';

export default function Timeline() {
  const [posts, setPosts] = React.useState(() => {
    const stickyValue = window.localStorage.getItem('posts');
    return stickyValue !== null
      ? JSON.parse(stickyValue)
      : [];
  });

  function getPosts() {
    React.useEffect(() => {
      let isMounted = true;
      Socket.on('emit posts channel', (data) => {
        if (isMounted) {
          setPosts(data);
        }
      });
      window.localStorage.setItem('posts', JSON.stringify(posts));
      return () => {
        Socket.off('emit posts channel', true);
        isMounted = false;
      };
    });
  }

  getPosts();

  function getNewPost() {
    React.useEffect(() => {
      let isMounted = true;
      Socket.on('emit new post channel', (newPost) => {
        if (isMounted) {
          setPosts([newPost].concat(posts));
          window.localStorage.setItem('posts', JSON.stringify(posts));
        }
      });
      return () => {
        Socket.off('emit new post channel', true);
        isMounted = false;
      };
    });
  }

  getNewPost();

  function updateLikes() {
    React.useEffect(() => {
      // flags notes mount status to avoid
      // "can't perform a React state update on an unmounted component"
      let isMounted = true;
      Socket.on('like post channel', (data) => {
        if (isMounted) {
          const numLikes = { num_likes: data.num_likes };
          const isLiked = { is_liked: data.is_liked };
          const Newposts = posts.map((el) => (
            el.id === data.post_id ? ({ ...el, ...numLikes, ...isLiked }) : el));
          setPosts(
            Newposts,
          );
          window.localStorage.setItem('posts', JSON.stringify(posts));
        }
      });
      return () => {
        Socket.off('like post channel', true);
        isMounted = false;
      };
    });
  }

  updateLikes();

  function updateComments() {
    React.useEffect(() => {
      let isMounted = true; // note this flag denote mount status
      Socket.on('NEW COMMENT ON POST', (data) => {
        if (isMounted) {
          const Newposts = posts.map((el) => (
            el.id === data.post_id ? (
              { ...el, comments: [data.comment].concat(el.comments), isCommentsOpen: true }
            ) : el));
          setPosts(
            Newposts,
          );
          window.localStorage.setItem('posts', JSON.stringify(posts));
        }
      });
      return () => {
        Socket.off('NEW COMMENT ON POST', true);
        isMounted = false;
      };
    });
  }

  updateComments();

  function getLocalStorage() {
    React.useEffect(() => {
      let isMounted = true;
      Socket.on('navigation change', () => {
        if (isMounted) {
          setPosts(window.localStorage.getItem('posts'));
        }
      });
      return () => {
        Socket.off('navigation change', true);
        isMounted = false;
      };
    });
  }

  getLocalStorage();

  return (
    <div>
      <ul className="timeline">
        {
                posts.map((post, index) => (
                  <PostItem
                    key={index}
                    id={post.id}
                    username={post.username}
                    text={post.text}
                    time={post.datetime}
                    likes={post.num_likes}
                    isLiked={post.is_liked}
                    comments={post.comments}
                    isCommentsOpen={post.isCommentsOpen}
                    pfp={post.pfp}
                    music={post.music}
                    musicType={post.music_type}
                  />
                ))
            }
      </ul>
    </div>
  );
}
