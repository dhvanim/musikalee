import React from 'react';
import { Socket } from './Socket';
 


export default function UserProfile(){
    const [userData, setUserData] = React.useState({}); 
    
    
     function newItem() {
        var newitem;
         React.useEffect(() => {
            Socket.on('emit user data', (data) => {
                 console.log(data['username'])
                 setUserData(data);
            });
        });
       
}

    // function getUserData() {
    //     React.useEffect( () => {
    //         Socket.on('emit user data', {
    //     console.log(data['username']);
    //     setUserData(data);
    // });
    //         return () => {
    //             Socket.off('emit user data', {
    //     console.log(data['username'])
    //     setUserData(data);
    // });
    //         };
    //     });
    // }
    
    // function updateUserData(data) {
    //     //console.log("Got user data");
    //     console.log(data['username'])
    //     setUserData(data);
    // }
    
   //getUserData();   
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
                <h1>@jan3apples</h1>
                <div>
                    <h4>@jan3apples  (profile type goes here)</h4>
                </div>
            </div>
          </div>
          <h1> Posts go here </h1>
       </div>
    );
    
    
}