import React, { useState } from 'react';

function AddEmployeePage() {
  // יצירת state עבור שם ואימייל
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  // פונקציה לטיפול במשלוח הטופס
  const handleSubmit = (e) => {
    e.preventDefault();

    // הודעה עם הפרטים
    alert(`Employee added: \nName: ${name}\nEmail: ${email}`);

    // ניתן גם לשלוח את הנתונים לשרת או להוסיף אותם לרשימה
    // ניקוי השדות לאחר ההוספה
    setName('');
    setEmail('');
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
      </form>
    </div>
  );
}

export default AddEmployeePage;
