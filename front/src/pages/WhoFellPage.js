import React, { useEffect, useState } from 'react';
import axios from 'axios';
import useIP from './ipGetter';

/**
 * WhoFellPage component displays employees who fell for phishing attempts.
 */
function WhoFellPage() {
  const [employees, setEmployees] = useState([]);
  const ipv4 = useIP(); // Get server IP address

   /**
   * useEffect hook to fetch employee data from the server when ipv4 changes.
   * This will retrieve the list of employees and their phishing counts.
   */
  useEffect(() => {
    if (ipv4) {
      axios.get(`http://${ipv4}:5000/employees`) // Fetch employee data
        .then(response => {
          const fetchedEmployees = response.data.map(employee => ({
            name: employee.name,
            falls: employee.phishing_count, // Extract name and phishing count
            email: employee.email // Add email to each employee object
          }));
          const sortedEmployees = fetchedEmployees.sort((a, b) => b.falls - a.falls); // Sort employees by falls
          setEmployees(sortedEmployees); // Update state
        })
        .catch(error => {
          console.error('Error fetching employees:', error);
        });
    }
  }, [ipv4]);

  /**
   * Send a warning email to an employee and reset their phishing count.
   * @param {string} email - The email address of the employee to notify.
   * @param {string} name - The name of the employee whose phishing count will be reset.
   */
  const sendWarningEmail = async (email, name) => {
    try {
        const response = await axios.post(`http://${ipv4}:5000/send-warning-email`, {
            email: email,
            name: name
        });
        alert("Warning email sent successfully!");

        // Reset phishing count to 0
        await axios.patch(`http://${ipv4}:5000/employees/${name}/reset-phishing-count`);
        
        // Update the local state to reflect this change
        setEmployees(prevEmployees => 
          prevEmployees.map(employee => 
            employee.name === name ? { ...employee, falls: 0 } : employee
          )
        );

    } catch (error) {
        console.error('Error sending email:', error);
    }
};

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Who Fell for the Phishing?</h1> {/* Page title */}
      <div style={{ maxHeight: '400px', overflowY: 'auto' }}> {/* Scrollable table */}
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Times Fell</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Send Warning Email</th>
            </tr>
          </thead>
          <tbody>
            {employees.slice(0, 10).map((employee, index) => ( // Display top 10 employees
              <tr key={index}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{employee.name}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{employee.falls}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  <button className="button" onClick={() => sendWarningEmail(employee.email, employee.name)}>Send Email</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default WhoFellPage;
