import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const [selectedRecipients, setSelectedRecipients] = useState([]);
  const navigate = useNavigate(); 

  const handleRecipientChange = (e) => {
    const options = Array.from(e.target.selectedOptions).map(option => option.value);
    setSelectedRecipients(options);
  };

  const goToMessageDesign = () => {
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients));
    navigate('/message-design');
  };

  const goToAddMessageType = () => {
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients));
    navigate('/add-message'); 
  };

  return (
    <div className="container">
      <h1>Phishing Campaign Management</h1>
      <div className="flex">
        <div className="box">
          <button className="btn" onClick={goToAddMessageType}>Add Message Type</button>
        </div>
        <div className="box">
          <button className="btn">Message History</button>
        </div>
      </div>
      <div className="box">
        <h3>Users who fell for the last message:</h3>
        <p>No data available yet.</p>
      </div>
      <div className="box">
        <label htmlFor="recipient">Select recipients for message:</label>
        <select id="recipient" className="dropdown" multiple size="3" onChange={handleRecipientChange}>
          <option value="bar">Bar</option>
          <option value="everyone">Everyone</option>
          <option value="amnon">Amnon</option>
        </select>
        <button className="btn" onClick={goToMessageDesign}>Go to Message Design</button>
      </div>
      <button className="btn">Sign Out</button>
    </div>
  );  
}

export default HomePage;
