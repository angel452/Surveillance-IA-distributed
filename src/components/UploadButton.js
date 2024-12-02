import React from 'react';
import axios from 'axios';

const UploadButton = ({ onUpload }) => {
  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await axios.post('http://localhost:5000/api/videos/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            alert(response.data.message);
            onUpload(file.name);
        } catch (error) {
            alert(error.response?.data?.message || 'Error uploading video');
        }
    }
  };


  return (
    <div className="my-3 text-center">
      <input
        type="file"
        accept="video/mp4,video/webm,video/ogg"
        style={{ display: 'none' }}
        id="upload-input"
        onChange={handleFileSelect}
      />
      <label htmlFor="upload-input" className="btn btn-primary">
        Upload Video
      </label>
    </div>
  );
};

export default UploadButton;
