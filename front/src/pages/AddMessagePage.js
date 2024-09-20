import React, { useState } from 'react';
import axios from 'axios';  // Ensure axios is installed and imported

function AddMessagePage() {
  const [messageType, setMessageType] = useState('');
  const [messageTitle, setMessageTitle] = useState('');
  const [messageContent, setMessageContent] = useState('');

  const submitMessage = async (e) => {
    e.preventDefault();

    // Prepare message data
    const messageData = {
      title: messageTitle,
      content: messageContent,
      message_type: messageType
    };

    // Send POST request to add the message
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/messages`, messageData);  // Adjust the URL if necessary
      alert("Message added successfully!");
    } catch (error) {
      console.error("There was an error adding the message:", error);
      alert("Failed to add the message.");
    }

    // Clear form fields after submission
    setMessageType('');
    setMessageContent('');
    setMessageTitle('');
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h1>Add Message Type</h1>
      <form onSubmit={submitMessage}>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="messageType" style={{ display: 'block', marginBottom: '5px' }}>Message Type:</label>
          <input
            type="text"
            id="messageType"
            value={messageType}
            onChange={(e) => setMessageType(e.target.value)}
            placeholder="Enter message type..."
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="messageTitle" style={{ display: 'block', marginBottom: '5px' }}>Message Title:</label>
          <input
            type="text"
            id="messageTitle"
            value={messageTitle}
            onChange={(e) => setMessageTitle(e.target.value)}
            placeholder="Enter message title..."
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="messageContent" style={{ display: 'block', marginBottom: '5px' }}>Message Content:</label>
          <textarea
            id="messageContent"
            value={messageContent}
            onChange={(e) => setMessageContent(e.target.value)}
            placeholder="Enter message content..."
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box', height: '120px' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>Submit Message</button>
      </form>
    </div>
  );
}

export default AddMessagePage;
