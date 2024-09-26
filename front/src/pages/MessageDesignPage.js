import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import useIP from './ipGetter'; 

/**
 * Component for designing and sending messages to recipients.
 */
function MessageDesignPage() {
  /**
   * States for managing recipients, message types, and the selected message type.
   */
  const [recipients, setRecipients] = useState([]);
  const [messageTypes, setMessageTypes] = useState([]);
  const [selectedMessageType, setSelectedMessageType] = useState('');
  const navigate = useNavigate();
  const ipv4 = useIP(); 

  /**
   * Fetch recipients from local storage and message types from the server.
   */
  useEffect(() => {
    const storedRecipients = JSON.parse(localStorage.getItem('selectedRecipients')) || [];
    setRecipients(storedRecipients);

    const fetchMessageTypes = async () => {
      try {
        const response = await axios.get(`http://${ipv4}:5000/message-types`);
        setMessageTypes(response.data);
      } catch (error) {
        console.error("Error fetching message types:", error);
      }
    };

    fetchMessageTypes();
  }, [ipv4]);

  /**
   * Sends the selected message to the chosen recipients.
   */
  const sendMessage = async () => {
    try {
      await axios.post(`http://${ipv4}:5000/send-emails`, {
        user_names: recipients,
        message_types: [selectedMessageType]
      });
      alert("Emails sent successfully!");
      navigate('/');
    } catch (error) {
      console.error("Error sending emails:", error);
      alert("An error occurred while sending emails.");
    }
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
        <select
          id="messageType"
          className="dropdown"
          value={selectedMessageType}
          onChange={(e) => setSelectedMessageType(e.target.value)}
        >
          <option value="" disabled>Select a message type</option>
          {messageTypes.map((type, index) => (
            <option key={index} value={type}>{type}</option>
          ))}
        </select>
      </div>
      <button className="btn" onClick={sendMessage}>Send and Return to Main</button>
    </div>
  );
}

export default MessageDesignPage;
