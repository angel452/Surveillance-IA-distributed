import React, { useState, useRef, useEffect } from 'react';
import Header from './components/Header';
import UploadButton from './components/UploadButton';
import ScanButton from './components/ScanButton';
import SearchBar from './components/SearchBar';
import VideoList from './components/VideoList';
import mockData from './mockData.json';
import VideoResults from './components/VideoResults';
import axios from 'axios';
 
const App = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [videoURLs, setVideoURLs] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [menuVisible, setMenuVisible] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
  const [videoData, setVideoData] = useState(null);
  const [containerWidth, setContainerWidth] = useState(500); // default width
  const [results] = useState(mockData);
  //const [setResults] = useState(mockData);
  const [videoPaths, setVideoPaths] = useState({}); // Stores loaded video paths
  const [scanResults, setScanResults] = useState([]); // Stores scan results from the backend
  const containerRef = useRef(null);
  const resizeRef = useRef(false);

  const [videos, setVideos] = useState([]); // Lista de videos escaneados
  const [loading, setLoading] = useState(true);

  const [finalResults, setFinalResults] = useState([]);

  const [scanning, setScanning] = useState(false); // Para saber si esta en proceso de escaneo

  const fetchVideos = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/videos/videos');
      setVideos(response.data.videos);
      setLoading(false);
    }
    catch (error) {
      console.error('Error fetching videos:', error);
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  const handleVideoUpload = (filePath, fileName) => {
    const videoNumber = Object.keys(videoPaths).length + 1; // Generate unique number for each video
    setVideoPaths((prevPaths) => ({
      ...prevPaths,
      [videoNumber]: filePath,
    }));
    setVideoURLs((prevURLs) => [...prevURLs, fileName]);
    alert(`Video uploaded: ${fileName} as Video ${videoNumber}`);
  };

  const handleRightClick = (video, e) => {
    e.preventDefault();
    setSelectedVideo(video);
    setMenuPosition({ x: e.pageX, y: e.pageY });
    setMenuVisible(true);
  };

  const handleOptionClick = (option) => {
    setMenuVisible(false);
    if (option === 'eliminar') {
      setVideoURLs((prevURLs) =>
        prevURLs.filter((_, index) => index !== selectedVideo.id - 1)
      );
      setVideoPaths((prevPaths) => {
        const updatedPaths = { ...prevPaths };
        delete updatedPaths[selectedVideo.id];
        return updatedPaths;
      });
    } else if (option === 'escanear') {
      setVideoData(`Generated description for ${selectedVideo.name}`);
    } else if (option === 'ver datos') {
      setVideoData(`Specific data for ${selectedVideo.name}`);
    }
  };

  //eslint-disable-next-line
  const handleClickOutside = (e) => {
    if (menuVisible && !containerRef.current.contains(e.target)) {
      setMenuVisible(false);
    }
  };

  const handleMouseDown = (e) => {
    if (e.target === resizeRef.current) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }
  };

  const handleMouseMove = (e) => {
    setContainerWidth((prevWidth) => Math.max(200, prevWidth + e.movementX)); // minimum width: 200px
  };

  const handleMouseUp = () => {
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  };

  const handleLinkClick = (time, videoNumber) => {
    const videoPath = videoPaths[videoNumber];
    if (!videoPath) {
      alert('This video has not been uploaded yet.');
      return;
    }

    // Open a new window with the correct video
    const newWindow = window.open('', '_blank', 'width=800,height=450');
    if (newWindow) {
      newWindow.document.write(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Video</title>
        </head>
        <body>
          <video controls autoplay style="width: 100%; height: 100%;">
            <source src="${videoPath}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
          <script>
            const videoElement = document.querySelector('video');
            videoElement.currentTime = ${time};
          </script>
        </body>
        </html>
      `);
    }
  };

  // const handleScanVideos = async () => {
  //   try {
  //     const response = await fetch('http://localhost:5000/api/videos/scan', {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify({
  //         videos: Object.values(videoPaths), // Asegúrate de enviar los videos correctamente
  //       }),
  //     });
  
  //     if (!response.ok) throw new Error('Error scanning videos..');
  //     const data = await response.json();
  //     setScanResults(data.results); // Asegúrate de que el backend devuelve resultados de la escaneo
  //     alert('Videos scanned successfully');
  //   } catch (error) {
  //     console.error('Error scanning videos...:', error);
  //     alert('Failed to scan videos. Check the backend.');
  //   }
  // };  

  useEffect(() => {
    fetchVideos();
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [menuVisible, handleClickOutside]);

  const renderSearchResults = () => {
    if (!searchQuery) return <p>No search results</p>;

    const filteredResults = results.filter((item) =>
      item.keyword.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return filteredResults.length ? (
      filteredResults.map((item, index) => (
        <div key={index}>
          <strong>{item.keyword}</strong> - {item.description} -{' '}
          <a
            href="/"
            onClick={() => handleLinkClick(item.time, item.video)}
            style={{ color: 'blue', textDecoration: 'underline' }}
          >
            Video {item.video}
          </a>
        </div>
      ))
    ) : (
      <p>No matches found</p>
    );
  };

  return (
    <div>
      {/* Header Component */}
      <Header />

      {/* Main Content */}
      <div className="container">
        {/* Upload, Scan, Search, Video List */}
        <UploadButton onUpload={handleVideoUpload} />

        <ScanButton 
          onScan={setScanResults} 
          setScanning={setScanning}
          scanning={scanning}
        />

        {/* <SearchBar onSearch={handleSearch} /> */}

        {/* Targetas */}
        <div className="row" style={{ display: 'flex' }}>

          {/* Video Results Buttons */}
          <div
            style={{
              border: '1px solid #ccc',
              padding: '10px',
              borderRadius: '8px',
              height: '500px',
              overflowY: 'auto',
            }}>

            <h5>Make Your Request</h5>
            <div className="makeRequest">
              {videos.length ? (
                videos.map((videoName, index) => (
                  <div key={index}>
                    <h5>Results for {videoName}</h5>
                    <VideoResults 
                      videoName={videoName}
                      setFinalResults={setFinalResults}
                      scanning={scanning}
                    />
                  </div>
                ))
              ) : (
                <p>No results found</p>
              )}
            </div>
          </div>

          
          {/* Video List: Lado izquierdo con la lista de todos los videos */}
          <div
            ref={containerRef}
            className="video-container"
            style={{
              width: `${containerWidth}px`,
              border: '1px solid #ccc',
              padding: '10px',
              borderRadius: '8px',
              overflowY: 'auto',
              resize: 'horizontal',
            }}
          >
            <VideoList
              searchQuery={searchQuery}
              videoURLs={videoURLs}
              onRightClick={handleRightClick}
            />
            <div
              ref={resizeRef}
              style={{
                width: '5px',
                cursor: 'ew-resize',
                position: 'absolute',
                top: 0,
                right: 0,
                bottom: 0,
              }}
              onMouseDown={handleMouseDown}
            />
          </div>

          {/* Muestra de los resutados */}
          <div
            className="col-md-4"
            style={{ flex: '1 1 auto', overflowY: 'auto' }}
          >
            {/* IA Result */}
            <div
              style={{
                border: '1px solid #ccc',
                padding: '10px',
                borderRadius: '8px',
                height: '500px',
                overflowY: 'auto',
              }}
            >            
              <p>
                {videoData || 'Select a video and scan to view the description'}
              </p>
            </div>

            {/* Search Results */}
            <div
              style={{
                border: '1px solid #ccc',
                padding: '10px',
                borderRadius: '8px',
                marginTop: '10px',
                height: '500px',
                overflowY: 'auto',
              }}
            >
              <h5>Search Results</h5>
                {/* {renderSearchResults()} */}
                {finalResults.length ? (
                  <ul>
                    {finalResults.map((item, index) => (
                      <li key={index}>{item.video_name}</li>
                    ))}
                  </ul>
                ) : (
                  <p>No results to display</p>
                )}
            </div>

            {/* Scan Results */}
            <div
              style={{
                border: '1px solid #ccc',
                padding: '10px',
                borderRadius: '8px',
                marginTop: '10px',
                height: '500px',
                overflowY: 'auto',
              }}
            >
              <h5>Scan Results</h5>
              {scanResults.length ? (
                scanResults.map((result, index) => (
                  <p key={index}>{result || 'No results found'}</p>
                ))
              ) : (
                <p>No scans yet.</p>
              )}
            </div>
          </div>
        </div>
        {menuVisible && (
          <div
            style={{
              position: 'absolute',
              top: menuPosition.y,
              left: menuPosition.x,
              backgroundColor: 'white',
              border: '1px solid #ccc',
              borderRadius: '4px',
              zIndex: 1000,
              boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.2)',
            }}
          >
            <div onClick={() => handleOptionClick('eliminar')} style={menuOptionStyle}>
              Delete
            </div>
            <div onClick={() => handleOptionClick('escanear')} style={menuOptionStyle}>
              Scan
            </div>
            <div onClick={() => handleOptionClick('ver datos')} style={menuOptionStyle}>
              View Data
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const menuOptionStyle = {
  padding: '8px 16px',
  cursor: 'pointer',
};

export default App;
