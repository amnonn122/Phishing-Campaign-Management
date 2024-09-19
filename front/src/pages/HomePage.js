import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // ייבוא axios
import './homepage.css';

function HomePage() {
  const navigate = useNavigate();

  const goToAddEmployee = () => {
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients));
    navigate('/add-employee');
  };

  const goToWhoFell = () => {
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients));
    navigate('/who-fell');
  };

  const goToAddMessageType = () => {
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients));
    navigate('/add-message');
  };

  // State to manage selected recipients and recipients fetched from the API
  const [selectedRecipients, setSelectedRecipients] = useState([]);
  const [selectAll, setSelectAll] = useState(false);
  const [recipients, setRecipients] = useState([]); // State עבור רשימת העובדים

  // שימוש ב-useEffect כדי למשוך את שמות העובדים מה-DB כאשר הקומפוננטה נטענת
  useEffect(() => {
    // שליפת הנתונים מה-API
    axios.get('http://localhost:5000/employees') // הנח שה-API שלך רץ על פורט 5000
      .then(response => {
        const employees = response.data.map(employee => ({
          value: employee.name,
          label: employee.name
        }));
        setRecipients(employees); // עדכון ה-state עם רשימת העובדים
      })
      .catch(error => {
        console.error('Error fetching employees:', error);
      });
  }, []); // הפונקציה תורץ פעם אחת כשיש טעינה

  const handleRecipientChange = (event) => {
    const { options } = event.target;
    const selected = [];
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selected.push(options[i].value);
      }
    }
    setSelectedRecipients(selected);
    setSelectAll(selected.length === recipients.length);
  };

  const handleSelectAllChange = () => {
    if (selectAll) {
      setSelectedRecipients([]);
    } else {
      setSelectedRecipients(recipients.map(recipient => recipient.value));
    }
    setSelectAll(!selectAll);
  };

  const goToMessageDesign = () => {
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients));
    navigate('/message-design');
  };

  return (
    <div className="container">
      <h1 className="header">Phishing Campaign Management</h1>
      <div className="button-container">
        <button className="button" onClick={goToAddMessageType}>Add Message Type</button>
        <button className="button" onClick={goToWhoFell}>Who Fell?</button>
        <button className="button" onClick={goToAddEmployee}>Add Employee</button>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <label htmlFor="recipient" className="select-all-label">
          Select recipients for message:
        </label>
        <div className="select-all-container">
          <input
            type="checkbox"
            id="selectAll"
            checked={selectAll}
            onChange={handleSelectAllChange}
            className="select-all-checkbox"
          />
          <label htmlFor="selectAll" className="select-all-label">Select All</label>
        </div>
        <select
          id="recipient"
          className="select"
          multiple
          size="5"
          onChange={handleRecipientChange}
          value={selectedRecipients}
        >
          {recipients.map(recipient => (
            <option key={recipient.value} value={recipient.value}>
              {recipient.label}
            </option>
          ))}
        </select>
        <button
          className="submit-button"
          onClick={goToMessageDesign}
        >
          Go to Message Design
        </button>
      </div>
    </div>
  );
}

export default HomePage;
