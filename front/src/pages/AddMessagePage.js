import React, { useState } from 'react';

function AddMessagePage() {
  const [messageType, setMessageType] = useState('');
  const [messageContent, setMessageContent] = useState('');

  const submitMessage = (e) => {
    e.preventDefault();
    const newWindow = window.open("", "_blank", "width=400,height=300");
    newWindow.document.write(`<h1 style="font-family: Arial; color: #2c3e50;">Message Summary</h1>`);
    newWindow.document.write(`<p><strong>Message Type:</strong> ${messageType}</p>`);
    newWindow.document.write(`<p><strong>Message Content:</strong> ${messageContent}</p>`);

    // ניקוי שדות לאחר שליחה
    setMessageType('');
    setMessageContent('');
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
          <label htmlFor="messageContent" style={{ display: 'block', marginBottom: '5px' }}>Message Content:</label>
          <textarea
            id="messageContent"
            value={messageContent}
            onChange={(e) => setMessageContent(e.target.value)}
            placeholder="Enter message content..."
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box', height: '120px' }} // גובה מותאם ל-4 שורות לפחות
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>Submit and Open Message</button>
      </form>
    </div>
  );
}

export default AddMessagePage;
