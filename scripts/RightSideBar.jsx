import * as React from 'react';
import { Socket } from './Socket';

export default function RightSideBar() {
    
    const [trending, setTrending] = React.useState(() => {
        const stickyValue = window.localStorage.getItem("trending");
        return stickyValue !== null
          ? JSON.parse(stickyValue)
          : [];
    });
    const [recommended, setRecommended] = React.useState(() => {
    const stickyValue = window.localStorage.getItem("recommended");
    return stickyValue !== null
      ? JSON.parse(stickyValue)
      : [];
  });
    
    function getTrending() {
        React.useEffect( () => {
            Socket.on('trending channel', updateTrending);
            return () => {
                Socket.off('trending channel', updateTrending);
            };
        }, [trending]);
    }
    
    function updateTrending(data) {
        window.localStorage.setItem("trending", JSON.stringify(data));
        setTrending( data );
    }
    
    function getRecommend() {
        React.useEffect( () => {
            Socket.on('recommended channel', updateRecommended);
            return () => {
                Socket.off('recommended channel', updateRecommended);
            };
        }, [recommended]);
    }
    
    function updateRecommended(data) {
        window.localStorage.setItem("recommended", JSON.stringify(data));
        setRecommended( data );
    }
    
    getTrending();
    
    getRecommend();
    
    
    return (
        <div className="rightsidebar">
            <div className="innerrightsidebar">
            <div className="trending">
                <h2> Trending </h2>
                
                <ul>
                    { trending.map( (trend, index) => (
                        <li key={index} className="trend">
                            <span className="song"> <i class="fas fa-fire-alt"></i> { trend.song } </span> <br />
                            <span className="artist"> { trend.artist } </span> <br />
                        </li>
                        ))
                    }
                </ul>
            </div>
            
            <div className="recommended">
                <h2> Recommended </h2>
                
                <ul>
                    { recommended.map( (rec, index) => (
                        <li key={index} className="rec">
                            <span className="song"> <i class="fas fa-heart"></i> { rec.song } </span> <br />
                            <span className="artist"> { rec.artist } </span> <br />
                        </li>
                        ))
                    }
                </ul>
            </div>
            </div>
        </div>
    );
}