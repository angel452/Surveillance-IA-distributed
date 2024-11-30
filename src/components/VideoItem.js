// src/components/VideoItem.js
import React from 'react';

const VideoItem = ({ video, onRightClick }) => {
  const handleContextMenu = (e) => {
    e.preventDefault();
    onRightClick(video, e); // Pasa también el evento `e` aquí
  };

  return (
    <div className="card my-2" onContextMenu={handleContextMenu} style={{ width: '80%', margin: 'auto' }}>
      <div className="card-body">
        <h5 className="card-title">{video.name}</h5>
        <video
          controls
          src={video.url}
          style={{ width: '100%', borderRadius: '8px', marginTop: '10px' }}
        />
      </div>
    </div>
  );
};

export default VideoItem;
