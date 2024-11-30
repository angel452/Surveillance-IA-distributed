import React from 'react';
import axios from 'axios';

const ScanButton = ({ onScan }) => {
  const handleScan = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/videos/scan');
      if (response.data.results) {
        onScan(response.data.results);
        alert('Scanning completed successfully');
      } else {
        alert('No results found.');
      }
    } catch (error) {
      console.error('Error during scan:', error);
      alert(error.response?.data?.message || 'Error scanning videos');
    }
  };

  return (
    <div className="my-3 text-center">
      <button className="btn btn-success" onClick={handleScan}>
        Scan Videos
      </button>
    </div>
  );
};

export default ScanButton;
