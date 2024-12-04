import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    onSearch(query);
  };

  return (
    <div className="my-3 d-flex flex-column align-items-center">
      <input 
        type="text"
        className="form-control w-75"
        placeholder="Search for a keyword in videos..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="btn btn-info mt-2 w-50" onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchBar;
  