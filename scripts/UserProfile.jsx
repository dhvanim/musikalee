import React from 'react';
import {
  Tab, Tabs, TabList, TabPanel,
} from 'react-tabs';
import { Follow } from './Follow';
import { Socket } from './Socket';
// import 'react-tabs/style/react-tabs.css';

export default function UserProfile() {
  const [isCreator, setIsCreator] = React.useState(false);
  const [isUser, setIsUser] = React.useState(false);
  const [users, setUsers] = React.useState('');
  const [profileType, setProfileType] = React.useState('');
  const [topArtists, setTopArtists] = React.useState([]);
  const [followers, setFollowers] = React.useState([]);
  const [isFollowed, setIsFollowed] = React.useState(false);
  const [currSong, setCurrSong] = React.useState('');
  const [topTracks, setTopTracks] = React.useState([]);
  const [numListeners, setNumListeners] = React.useState(0);

  function updateUserData(data) {
    if (data.profileType === 'artist') {
      setIsCreator((prevState) => true);
      setUsers((prevState) => data.username);
      setProfileType((prevState) => data.profileType);
      setTopTracks((prevState) => data.topTracks);
      setNumListeners((prevState) => data.numListeners);
      setFollowers((prevState) => data.following);
      window.localStorage.setItem('User Data', JSON.stringify(data));
      return users, profileType, topTracks, numListeners, followers;
    }
    setIsUser((prevState) => true);
    setUsers((prevState) => data.username);
    setProfileType((prevState) => data.profileType);
    setTopArtists((prevState) => data.topArtists);
    setFollowers((prevState) => data.following);
    setCurrSong((prevState) => data.currentSong);
    window.localStorage.setItem('User Data', JSON.stringify(data));
    return users, profileType, topArtists, followers, currSong;
  }

  function newItem() {
    React.useEffect(() => {
      Socket.on('emit user data', updateUserData);

      return () => {
        Socket.off('emit user data', updateUserData);
      };
    });
  }

  function getProfilePic() {
    const data = window.localStorage.getItem('userinfo');
    const user = JSON.parse(data);
    return user.pfp;
  }

  newItem();

  function updateFollowerData(data) {
    setIsFollowed((prevState) => data.isFollowing);
    setFollowers((prevState) => data.followers);
    window.localStorage.setItem('Follower Data', JSON.stringify(data));
  }

  function followerData() {
    React.useEffect(() => {
      Socket.on('emit follower data', updateFollowerData);

      return () => {
        Socket.off('emit follower data', updateFollowerData);
      };
    });
  }

  followerData();

  return (
    <div className="page">
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        margin: '18px 0px',
        borderBottom: '1px solid grey',
      }}
      >
        <div>
          <img style={{ width: '120px', height: '120px', borderRadius: '60px' }} src={getProfilePic()} />
        </div>
        <div>
          <h1 id="test">{users}</h1>
          <div>
            <h4>
              @
              {users}
              {' '}
              {profileType}
            </h4>
          </div>
        </div>
        <div>
          <Follow isFollowed={isFollowed} />
        </div>
      </div>
      {isUser
        ? (
          <div>
            <Tabs>
              <TabList className="tabsUser">
                <Tab>User Info</Tab>
                <Tab>Followers</Tab>
              </TabList>

              <TabPanel>
                <h1>Currently listening to:</h1>
                <p>{currSong}</p>
                <h1> Top artists:</h1>

                <ul className="artistList">
                  { topArtists.map((artists, index) => (
                    <li key={index} className="AL">
                      <img style={{ width: '90px', height: '90px', borderRadius: '45px' }} src="./static/defaultPfp.png" />
                      <br />
                      <span className="artists">
                        {' '}
                        { artists }
                        {' '}
                      </span>
                      {' '}
                      <br />
                    </li>
                  ))}
                </ul>
              </TabPanel>

              <TabPanel>
                <ul>
                  { followers.map((followers, index) => (
                    <li key={index} className="F">
                      <span className="followers">
                        {' '}
                        { followers }
                        {' '}
                      </span>
                      {' '}
                      <br />
                    </li>
                  ))}
                </ul>
              </TabPanel>
            </Tabs>
          </div>
        )
        : <div />}

      {isCreator
        ? (
          <div>
            <TabList className="tabsArtist">
              <Tab>User Info</Tab>
              <Tab>Followers</Tab>
            </TabList>

            <TabPanel>
              <h1>Number of monthly listeners:</h1>
              <p>{numListeners}</p>

              <ul className="trackList">
                { topTracks.map((tracks, index) => (
                  <li key={index} className="TL">
                    <img style={{ width: '90px', height: '90px', borderRadius: '45px' }} src="./static/defaultCoverArt.png" />
                    <br />
                    <span className="artists">
                      {' '}
                      { tracks }
                      {' '}
                    </span>
                    {' '}
                    <br />
                  </li>
                ))}
              </ul>
            </TabPanel>

            <TabPanel>
              <ul>
                { followers.map((followers, index) => (
                  <li key={index} className="F">
                    <span className="followers">
                      {' '}
                      { followers }
                      {' '}
                    </span>
                    {' '}
                    <br />
                  </li>
                ))}
              </ul>
            </TabPanel>
          </div>
        )
        : <div />}
    </div>
  );
}
