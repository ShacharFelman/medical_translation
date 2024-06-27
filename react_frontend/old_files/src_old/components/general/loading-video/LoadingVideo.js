import React from 'react';
import gif from './loading_gif.gif'

const LoadingVideo = () => {
  return (
    <div style={{
       width:"7rem" 
    }}>
      <img src={gif} alt="loading..."  style={{
        height:"100%",
        width:"100%"
      }}/>
    </div>
  );
};

export default LoadingVideo;
