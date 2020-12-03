import * as React from 'react';
import { Socket } from './Socket';

export default function StatusBar() {
  function getUserInfo() {
    const data = window.localStorage.getItem('userinfo');
    return JSON.parse(data);
  }

  function display(list) {
    for (let i = 0; i < list.length; i += 1) {
      list[i].style.display = 'block';
      list[i].required = true;
    }
  }

  function hide(list) {
    for (let i = 0; i < list.length; i += 1) {
      list[i].style.display = 'none';
      list[i].required = false;
    }
  }

  function submitPost(event) {
    const user = getUserInfo();
    const status = document.getElementById('text_status');

    const type = document.getElementById('option');
    const song = document.getElementById('song');
    const artist = document.getElementById('artist');
    const album = document.getElementById('album');
    const playlist = document.getElementById('playlist');

    Socket.emit('user post channel', {
      user: {
        username: user.username,
        pfp: user.pfp,
      },
      text: status.value,
      type: type.value,
      music: {
        song: song.value,
        artist: artist.value,
        album: album.value,
        playlist: playlist.value,
      },
    });

    status.value = '';
    song.value = '';
    artist.value = '';
    album.value = '';
    playlist.value = '';

    event.preventDefault();
  }

  function dropdownselect() {
    const dropdown = document.getElementById('option');
    const song = document.getElementById('song');
    const artist = document.getElementById('artist');
    const album = document.getElementById('album');
    const playlist = document.getElementById('playlist');

    if (dropdown.value === 'default') {
      hide([song, artist, album, playlist]);
    } else if (dropdown.value === 'song') {
      display([song, artist]);
      hide([album, playlist]);
    } else if (dropdown.value === 'artist') {
      display([artist]);
      hide([song, album, playlist]);
    } else if (dropdown.value === 'album') {
      display([artist, album]);
      hide([song, playlist]);
    } else if (dropdown.value === 'playlist') {
      display([playlist]);
      hide([song, artist, album]);
    }
  }

  return (
    <div className="statusbar">
      <form onSubmit={submitPost}>
        <input type="text" id="text_status" placeholder="What are you listening to?" maxLength="256" required />

        <br />

        <select id="option" name="option" onClick={dropdownselect}>
          <option value="default"> Attach Media </option>
          <option value="song"> Song </option>
          <option value="artist"> Artist </option>
          <option value="album"> Album </option>
          <option value="playlist"> Playlist </option>
        </select>

        <input type="text" id="song" placeholder="Enter Song" maxLength="500" />
        <input type="text" id="artist" placeholder="Enter Artist" maxLength="500" />
        <input type="text" id="album" placeholder="Enter Album" maxLength="500" />
        <input type="text" id="playlist" placeholder="Enter Playlist Link" maxLength="500" />

        <input type="submit" name="Send Post" />
      </form>
    </div>
  );
}
