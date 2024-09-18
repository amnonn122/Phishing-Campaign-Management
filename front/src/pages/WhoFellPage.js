import React, { useState, useEffect } from 'react';

function WhoFellPage() {
  // Example data with more entries
  const [employees, setEmployees] = useState([
    { name: 'John Doe', falls: 5 },
    { name: 'Jane Smith', falls: 3 },
    { name: 'Amnon', falls: 7 },
    { name: 'Bar', falls: 4 },
    { name: 'Everyone', falls: 2 },
    { name: 'Alice', falls: 1 },
    { name: 'Bob', falls: 6 },
    { name: 'Charlie', falls: 8 },
    { name: 'David', falls: 9 },
    { name: 'Eva', falls: 0 },
    { name: 'Frank', falls: 10 },
    { name: 'Grace', falls: 11 },
    { name: 'Hannah', falls: 12 },
  ]);

  // Sort employees by the number of times they fell for the phishing (descending order)
  useEffect(() => {
    const sortedEmployees = [...employees].sort((a, b) => b.falls - a.falls);
    setEmployees(sortedEmployees);
  }, [employees]);

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
