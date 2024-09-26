import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import useIP from './ipGetter'; 

/**
 * HomePage component for managing phishing campaign recipients.
 */
function HomePage() {
  const navigate = useNavigate(); 
  const ipv4 = useIP(); 
  
  /**
   * States for selected recipients, "Select All" checkbox, recipient list, and error message.
   */
  const [selectedRecipients, setSelectedRecipients] = useState([]); 
  const [selectAll, setSelectAll] = useState(false); 
  const [recipients, setRecipients] = useState([]); 
  const [errorMessage, setErrorMessage] = useState(''); 

  /**
   * useEffect hook to fetch employee data from the server when ipv4 changes.
   * It fetches the list of employees and sets them in the recipients state.
   */
  useEffect(() => {
    if (ipv4) {
      // Fetch employee data from the server
      axios.get(`http://${ipv4}:5000/employees`)
        .then(response => {
          const employees = response.data.map(employee => ({
            value: employee.name, 
            label: employee.name // Display label for each recipient
          }));
          setRecipients(employees); 
        })
        .catch(error => {
          console.error('Error fetching employees:', error); 
        });
    }
  }, [ipv4]);

  /**
   * Handles changes in the recipient selection.
   * Updates the selected recipients state based on user selection.
   *
   * @param {Event} event - The change event triggered by the select element.
   */
  const handleRecipientChange = (event) => {
    const { options } = event.target;
    const selected = [];
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selected.push(options[i].value); // Add selected recipients to the array
      }
    }
    setSelectedRecipients(selected); 
    setSelectAll(selected.length === recipients.length); // Check if all recipients are selected
    setErrorMessage(''); 
  };

  /**
   * Handles changes to the "Select All" checkbox.
   * Toggles between selecting all recipients or deselecting them.
   */
  const handleSelectAllChange = () => {
    if (selectAll) {
      setSelectedRecipients([]); // Deselect all if currently selected
    } else {
      setSelectedRecipients(recipients.map(recipient => recipient.value)); // Select all recipients
    }
    setSelectAll(!selectAll); // Toggle select all state
    setErrorMessage(''); 
  };

   /**
   * Navigates to the message design page.
   * Validates that at least one recipient is selected before proceeding.
   */
  const goToMessageDesign = () => {
    if (selectedRecipients.length === 0) {
      setErrorMessage('Please select at least one recipient to proceed.'); // Set error message if no one selected
      return; 
    }
    
    localStorage.setItem('selectedRecipients', JSON.stringify(selectedRecipients)); // Store selected recipients in local storage
    navigate('/message-design'); // Navigate to message design page
  };

  return (
    <div className="container">
      <h1 className="header">Phishing Campaign Management</h1>
      <div className="button-container">
        <button className="button" onClick={() => navigate('/add-message')}>Add Message Type</button>
        <button className="button" onClick={() => navigate('/who-fell')}>Who Fell?</button>
        <button className="button" onClick={() => navigate('/add-employee')}>Add Employee</button>
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
          size="5" // Number of visible options
          onChange={handleRecipientChange} 
          value={selectedRecipients} 
        >
          {recipients.map(recipient => (
            <option key={recipient.value} value={recipient.value}>
              {recipient.label}
            </option>
          ))}
        </select>
        {errorMessage && ( 
          <p style={{ color: 'red', marginTop: '10px', fontWeight: 'bold' }}>{errorMessage}</p>
        )}
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
