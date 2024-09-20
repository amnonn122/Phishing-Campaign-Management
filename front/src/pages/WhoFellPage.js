import React, { useState, useEffect } from 'react';
import axios from 'axios'; 

function WhoFellPage() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/employees`) 
      .then(response => {
        const fetchedEmployees = response.data.map(employee => ({
          name: employee.name,
          falls: employee.phishing_count, 
        }));
        const sortedEmployees = fetchedEmployees.sort((a, b) => b.falls - a.falls);
        setEmployees(sortedEmployees);
      })
      .catch(error => {
        console.error('Error fetching employees:', error);
      });
  }, []); 

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Who Fell for the Phishing?</h1>
      <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Times Fell</th>
            </tr>
          </thead>
          <tbody>
            {employees.slice(0, 10).map((employee, index) => (
              <tr key={index}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{employee.name}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{employee.falls}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default WhoFellPage;
