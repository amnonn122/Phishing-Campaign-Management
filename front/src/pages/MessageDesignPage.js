import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function MessageDesignPage() {
  const [recipients, setRecipients] = useState([]);
  const [messageTypes, setMessageTypes] = useState([]);
  const [selectedMessageType, setSelectedMessageType] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Load recipients from localStorage
    const storedRecipients = JSON.parse(localStorage.getItem('selectedRecipients')) || [];
    setRecipients(storedRecipients);

    // Fetch message types from the backend
    const fetchMessageTypes = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/message-types`);  // Adjust URL if needed
        console.log('Fetched message types:', response.data); // Debugging
        setMessageTypes(response.data);
      } catch (error) {
        console.error("Error fetching message types:", error);
      }
    };

    fetchMessageTypes();
  }, []);

  const sendMessage = async () => {
    try {
      console.log('Selected message type:', selectedMessageType); // Debugging

      // Call backend to send emails
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/send-emails`, {
        user_names: recipients,
        message_types: [selectedMessageType]
      });

      if (response.data.success) {
        alert("Emails sent successfully!");
      } else {
        alert("Failed to send emails.");
      }

      // Navigate back to the main page
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
          onChange={(e) => {
            console.log('Changed message type:', e.target.value); // Debugging
            setSelectedMessageType(e.target.value);
          }}
        >
          <option value="" disabled>Select a message type</option> {/* Default option */}
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
