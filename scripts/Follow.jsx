import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom'

export function Follow(props) {
    
    function handleSubmit(event) {
        
        console.log("now following"); 
        event.preventDefault();
    }

        
    return (
        <form onSubmit={handleSubmit}>
            <button id="f-button"> Follow </button>
        </form>
    );
}
