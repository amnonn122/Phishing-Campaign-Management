import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; 
import useIP from './ipGetter';  

/**
 * Component to add new employees to the system.
 */
function AddEmployeePage() {
  /**
   * States to hold employee name & email and to handle errors
   */ 
  const [name, setName] = useState(''); 
  const [email, setEmail] = useState('');  
  const [error, setError] = useState(null);  
  const navigate = useNavigate(); 
  const ipv4 = useIP(); 

  /**
   * Handles form submission to add a new employee.
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); 
    try {
      if (ipv4) {
        // Post new employee data to the backend API
        await axios.post(`http://${ipv4}:5000/employees`, { name, email });
        alert('Employee added successfully'); 
        // Reset the form fields
        setName('');
        setEmail('');
        setError(null);
        navigate('/'); // Redirect to the home page
      } else {
        setError('Failed to retrieve server IP'); // Handle error if IP retrieval fails
      }
    } catch (error) {
      console.error(error);
      setError(error.response?.data?.message || 'Failed to add employee'); // Set error message
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h1>Add Employee</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="name" style={{ display: 'block', marginBottom: '5px' }}>Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)} 
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)} 
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>Add Employee</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
}

export default AddEmployeePage;
