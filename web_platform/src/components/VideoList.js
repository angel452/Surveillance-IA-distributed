// src/components/VideoList.js
import React from 'react';
import VideoItem from './VideoItem';

const VideoList = ({ searchQuery, videoURLs, onRightClick }) => {
  const videos = videoURLs.map((url, index) => ({
    id: index + 1,
    name: `Video ${index + 1}`,
    url: url,
  }));

  const filteredVideos = videos.filter((video) =>
    video.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div style={{ maxHeight: '500px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px', borderRadius: '8px' }}>
      {filteredVideos.length > 0 ? (
        filteredVideos.map((video) => (
          <div className="col-md-6 col-lg-4" key={video.id}>
            <VideoItem video={video} onRightClick={onRightClick} />
          </div>
        ))
      ) : (
        <div className="col-12 text-center">
          <p>No hay videos</p>
        </div>
      )}
    </div>
  );
};

export default VideoList;
