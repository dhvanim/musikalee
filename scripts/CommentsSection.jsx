import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';

export default function CommentsSection(props) {
    const comments= props.comments;

    return (
        
        <div>
            { comments.map( (comment, index) => (
                <p key = {index}> {comment.text} </p>
                ))    
            }
        </div>
    );
}
