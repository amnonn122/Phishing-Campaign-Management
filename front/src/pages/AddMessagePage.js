import React, { useState } from 'react';

function AddMessagePage() {
  const [messageType, setMessageType] = useState('');
  const [messageContent, setMessageContent] = useState('');

  const submitMessage = () => {
    const newWindow = window.open("", "_blank", "width=400,height=300");
    newWindow.document.write(`<h1 style="font-family: Arial; color: #2c3e50;">Message Summary</h1>`);
    newWindow.document.write(`<p><strong>Message Type:</strong> ${messageType}</p>`);
    newWindow.document.write(`<p><strong>Message Content:</strong> ${messageContent}</p>`);
  };

  return (
    <div className="container">
      <h1>Add Message Type</h1>
      <label htmlFor="messageType">Message Type</label>
      <input 
        type="text" 
        id="messageType" 
        value={messageType}
        onChange={(e) => setMessageType(e.target.value)}
        placeholder="Enter message type..." 
      />
      <label htmlFor="messageContent">Message Content</label>
      <input 
        type="text" 
        id="messageContent" 
        value={messageContent}
        onChange={(e) => setMessageContent(e.target.value)}
        placeholder="Enter message content..." 
      />
      <button onClick={submitMessage}>Submit and Open Message</button>
    </div>
  );
}

export default AddMessagePage;
