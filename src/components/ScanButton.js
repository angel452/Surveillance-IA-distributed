import React from 'react';
import axios from 'axios';

const ScanButton = ({ onScan, scanning, setScanning }) => {
  const handleScan = async () => {
    setScanning(true);
    try {
      const response = await axios.post('http://localhost:5000/api/videos/scan');

      console.log('Scan response:', response.data);

      if (response.data.results) {
        // Agregamos los nuevos resultados a los resultados existentes
        //onScan(prevResults => [...prevResults, ...response.data.results]);
        onScan(response.data.results);

        alert('Scanning completed successfully');
      } else {
        alert('No results found.');
      }
    } catch (error) {
      console.error('Error during scan:', error);
      alert(error.response?.data?.message || 'Error scanning videos');
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="my-3 text-center">
      <button 
        className="btn btn-success" 
        onClick={handleScan}
        disabled={scanning}
      >
        {scanning ? 'Scanning...' : 'Scan Videos'}
      </button>
    </div>
  );
};

export default ScanButton;
