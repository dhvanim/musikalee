import * as React from 'react';
import { Socket } from './Socket';

export default function RightSideBar() {
    
    const [trending, setTrending] = React.useState([]);
    const [recommended, setRecommended] = React.useState([]);
    
    function getTrending() {
        React.useEffect( () => {
            Socket.on('trending channel', updateTrending);
            return () => {
                Socket.off('trending channel', updateTrending);
            };
        });
    }
    
    function updateTrending(data) {
        setTrending( data );
    }
    
    function getRecommend() {
        React.useEffect( () => {
            Socket.on('recommended channel', updateRecommended);
            return () => {
                Socket.off('recommended channel', updateRecommended);
            };
        });
    }
    
    function updateRecommended(data) {
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
                            <span className="song"> { trend.song } </span> <br />
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
                        <li key={index} className="trend">
                            <span className="song"> { rec.song } </span> <br />
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