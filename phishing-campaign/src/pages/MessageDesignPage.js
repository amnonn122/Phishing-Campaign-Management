import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function MessageDesignPage() {
  const [recipients, setRecipients] = useState([]);
  const navigate = useNavigate(); // שינוי השם מ-history ל-navigate

  useEffect(() => {
    const storedRecipients = JSON.parse(localStorage.getItem('selectedRecipients')) || [];
    setRecipients(storedRecipients);
  }, []);

  const sendMessage = () => {
    navigate('/'); // שימוש ב-navigate במקום history.push
  };

  return (
    <div className="container">
      <h1>Design Your Message</h1>
      <div className="box">
        <h3>Selected Recipients:</h3>
        <ul>
          {recipients.map((recipient, index) => (
            <li key={index}>{recipient}</li>
          ))}
        </ul>
      </div>
      <div className="box">
        <label htmlFor="messageType">Choose Message Type:</label>
        <select id="messageType" className="dropdown">
          <option value="typeA">Type A</option>
          <option value="typeB">Type B</option>
          <option value="typeC">Type C</option>
        </select>
      </div>
      <div className="box">
        <label htmlFor="messageContent">Choose Message to Send:</label>
        <select id="messageContent" className="dropdown">
          <option value="message1">Message 1</option>
          <option value="message2">Message 2</option>
          <option value="message3">Message 3</option>
        </select>
      </div>
      <button className="btn" onClick={sendMessage}>Send and Return to Main</button>
    </div>
  );
}

export default MessageDesignPage;
