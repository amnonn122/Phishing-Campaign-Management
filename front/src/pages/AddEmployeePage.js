import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // ייבוא useNavigate

function AddEmployeePage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState(null);

  const navigate = useNavigate(); // יצירת משתנה ניווט

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // שליחה לשרת Flask בכתובת הנכונה
      const response = await axios.post('http://localhost:5000/employees', { name, email });

      alert('Employee added successfully');

      // ניקוי השדות לאחר ההוספה
      setName('');
      setEmail('');
      setError(null);

      // ניווט ל-HomePage אחרי הוספה מוצלחת
      navigate('/');
    } catch (error) {
      console.error(error);
      setError(error.response?.data?.message || 'Failed to add employee');
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
