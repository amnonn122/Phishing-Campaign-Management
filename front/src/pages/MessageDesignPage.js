import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function MessageDesignPage() {
  const [recipients, setRecipients] = useState([]);
  const navigate = useNavigate(); 

  useEffect(() => {
    const storedRecipients = JSON.parse(localStorage.getItem('selectedRecipients')) || [];
    setRecipients(storedRecipients);
  }, []);

  const sendMessage = () => {
    navigate('/'); 
  };

  return (
    <div className="container">
      <h1>Design Your Message</h1>
      <div className="box">
        <h3>Selected Recipients:</h3>
        <div style={{ maxHeight: '200px', overflowY: 'auto', border: '1px solid #ccc', padding: '8px', borderRadius: '4px' }}>
          <ul style={{ margin: 0, padding: 0, listStyleType: 'none' }}>
            {recipients.map((recipient, index) => (
              <li key={index} style={{ padding: '4px 0' }}>{recipient}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="box">
        <label htmlFor="messageType">Choose Message Type:</label>
        <select id="messageType" className="dropdown">
          <option value="typeA">Type A</option>
          <option value="typeB">Type B</option>
          <option value="typeC">Type C</option>
        </select>
      </div>
      <button className="btn" onClick={sendMessage}>Send and Return to Main</button>
    </div>
  );
}

export default MessageDesignPage;
