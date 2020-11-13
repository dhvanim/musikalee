import React from 'react';
import { Socket } from './Socket';
 


export default function UserProfile(){
    const [userData, setUserData] = React.useState([]);
    const [isCreator, setIsCreator] = React.useState(false);
    const [isUser, setIsUser] = React.useState(false);
    
    
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
            return [data['username'], data['profileType'],  data['topArtists'], data['following'], data['currentSong']];
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
                <h1 id="test">{userData[0]}</h1>
                <div>
                    <h4>@{userData[0]} {userData[1]}</h4>
                </div>
            </div>
          </div>
          <h1>Currently listening to:</h1>
          <p>{userData[4]}</p>
          <h1> Top artists here:</h1>
          <p>{userData[2]}</p>
          <h1>following:</h1>
          <p>{userData[3]}</p>
       </div>
    );
    
    
}