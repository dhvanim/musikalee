import React from 'react';
import { Socket } from './Socket';
 


export default function UserProfile(){
    const [userData, setUserData] = React.useState([]);
    const [isCreator, setIsCreator] = React.useState(false);
    const [isUser, setIsUser] = React.useState(false);
    const[users, setUsers] = React.useState("");
    const[profileType, setProfileType] = React.useState("");
    const[topArtists, setTopArtists] = React.useState([]);
    const[followers, setFollowers] = React.useState([]);
    const[currSong, setCurrSong] = React.useState("");
    const[topTracks, setTopTracks] = React.useState([]);
    const[numListeners, setNumListeners] = React.useState(0);
    
    
    
    function newItem() {
        React.useEffect(() => {
            Socket.on('emit user data', updateUserData);
            
            return () => {
                Socket.off('emit user data', updateUserData);
            };
        });
    }
    
    function updateUserData(data) {
        return setUserData(() => {
            
           
            
            if(data['profileType'] == "artist")
                {
                    setIsCreator(prevState => true);
                    setUsers(prevState => data['username']);
                    setProfileType(prevState => data['profileType']);
                    setTopTracks(prevState => data['topTracks']);
                    setNumListeners(prevState => data['numListeners']);
                    setFollowers(prevState => data['following']);
                    return users, profileType, topTracks, numListeners, followers;
                }
                
                else
                {
                    setIsUser(prevState => true);
                    setUsers(prevState => data['username']);
                    setProfileType(prevState => data['profileType']);
                    setTopArtists(prevState => data['topArtists']);
                    setFollowers(prevState => data['following']);
                    setCurrSong(prevState => data['currentSong']);
                    return users, profileType, topArtists, followers, currSong;
                }
                

            
        });
    }
    
 
    
    newItem();
    
    return (
       <div className="page">
          <div style={{
          display:"flex",
          justifyContent:"center",
          margin:"18px 0px",
          borderBottom:"1px solid grey"
          }}>
            <div>
                <img style={{width:"120px",height:"120px",borderRadius:"60px"}} src="./static/defaultPfp.png"/>
            </div>
            <div>
                <h1 id="test">{users}</h1>
                <div>
                    <h4>@{users} {profileType}</h4>
                </div>
            </div>
            <div>
                <button> following </button>
                
                <ul>
                    { followers.map( (followers, index) => (
                        <li key={index} className="F">
                            <span className="followers"> { followers } </span> <br />
                        </li>
                        ))
                    }
                </ul>
                
            </div>
          </div>
          {isUser?
                <div>
                    <h1>Currently listening to:</h1>
                    <p>{currSong}</p>
                    <h1> Top artists here:</h1>
                     
                    <ul className="artistList">
                        { topArtists.map( (artists, index) => (
                            <li key={index} className="AL">
                                <img style={{width:"90px",height:"90px",borderRadius:"45px"}} src="./static/defaultPfp.png"/><br/>
                                <span className="artists"> { artists } </span> <br/>
                            </li>
                            ))
                        }
                    </ul>
                </div>
                :
                <div>
                </div>
            }
            
            {isCreator?
                <div>
                    <h1>Number of monthly listeners:</h1>
                    <p>{numListeners}</p>
                    
                    <ul className="trackList">
                        { topTracks.map( (tracks, index) => (
                            <li key={index} className="TL">
                                <img style={{width:"90px",height:"90px",borderRadius:"45px"}} src="./static/defaultCoverArt.png"/><br/>
                                <span className="artists"> { tracks } </span> <br/>
                            </li>
                            ))
                        }
                    </ul>
                </div>
                :
                <div></div>
            }
       </div>
    );
    
    
}